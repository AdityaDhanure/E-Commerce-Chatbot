from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q # <--- Import Q for complex queries

from django.conf import settings # <--- Import settings to access environment variables
import openai
import re # <--- Import regex for product name matching

# Initialize OpenAI client with your DeepSeek API key and base URL
try:
    openai_client = openai.OpenAI(
        api_key=settings.DEEPSEEK_API_KEY,
        base_url=settings.DEEPSEEK_BASE_URL
    )
except Exception as e:
    print(f"Failed to initialize OpenAI client for DeepSeek: {e}")
    openai_client = None # Set to None if initialization fails

from .models import ChatSession, ChatMessage
from products.models import Product, ProductCategory
from .serializers import ChatSessionSerializer, ChatMessageSerializer
from products.serializers import ProductSerializer

# --- Function to get product categories for the SYSTEM_PROMPT ---
def get_available_categories_for_prompt():
    """Fetches all product category names and formats them for the AI prompt."""
    categories = ProductCategory.objects.all().values_list('name', flat=True)
    if categories:
        return ", ".join(list(categories))
    return "various products" # Default if no categories are found

# --- Function to extract product names from AI's response and fetch them ---
def extract_and_recommend_products(ai_response_text, limit_per_category=5):
    """
    Parses the AI's response to find potential product names or categories
    and fetches corresponding Product objects from the database.
    This is a simple keyword matching approach. For better results,
    consider fine-tuning the AI or using more advanced NLP.
    """
    found_product_ids = set()
    recommended_products_list = [] # To store the actual Product objects

    # Convert AI response to lowercase for case-insensitive matching
    ai_response_lower = ai_response_text.lower()

    # --- Strategy 1: Find specific product names mentioned by the AI ---
    # Fetch all product names from the database
    # Using values() to get a list of dictionaries with 'id' and 'name'
    all_products_in_db = list(Product.objects.all().values('id', 'name'))
    
    # Create a mapping of product names to IDs for quick lookup
    product_name_to_id = {p['name'].lower(): p['id'] for p in all_products_in_db}
    
    # Sort product names by length in descending order to prioritize longer matches
    sorted_product_names_keys = sorted(product_name_to_id.keys(), key=len, reverse=True)

    for product_name_lower in sorted_product_names_keys:
        # Use regex to find whole word matches in the AI response
        # \b ensures word boundaries, re.escape handles special characters in names
        if re.search(r'\b' + re.escape(product_name_lower) + r'\b', ai_response_lower):
            product_id = product_name_to_id[product_name_lower]
            if product_id not in found_product_ids: # Avoid adding duplicates
                found_product_ids.add(product_id)

    # --- Strategy 2: Find category names mentioned by the AI ---
    # Fetch all category names from the database
    all_category_names_in_db = list(ProductCategory.objects.all().values_list('name', flat=True))
    
    # Sort category names by length in descending order for matching
    sorted_category_names_keys = sorted([name.lower() for name in all_category_names_in_db], key=len, reverse=True)

    for category_name_lower in sorted_category_names_keys:
        if re.search(r'\b' + re.escape(category_name_lower) + r'\b', ai_response_lower):
            # If a category name is found, fetch products from that category
            # Exclude already found products to avoid duplicates
            # Using Q objects to filter by category name, case-insensitive
            category_products = Product.objects.filter(
                Q(category__name__iexact=category_name_lower) | Q(category__name__icontains=category_name_lower)
            ).exclude(id__in=list(found_product_ids)).order_by('?')[:limit_per_category] # order_by('?') for random top N

            for p in category_products:
                found_product_ids.add(p.id)

    # --- Final Step: Fetch all unique Product objects found ---
    if found_product_ids:
        # Filter products by the found IDs and ensure uniqueness
        # Using distinct() to ensure no duplicates in case of multiple matches
        recommended_products_list = list(Product.objects.filter(id__in=list(found_product_ids)).distinct())
    
    return recommended_products_list # Return as a list of Product objects



# --- System Prompt Template for the AI ---
# This template is used to guide the AI's responses, ensuring it provides product recommendations
SYSTEM_PROMPT_TEMPLATE = (
    "You are an AI assistant for an e-commerce store. Your primary goal is to help users find products, "
    "answer questions about products, and assist with general inquiries about the store. "
    "Be helpful, concise, and friendly. "
    "Our available product categories are: {categories_list}. "
    "When a user asks for product recommendations or product types, always provide a clear textual response. "
    "Try to mention specific products by name from these categories if relevant to their query. "
    "If you recommend specific items, use their full name. "
    "You can also mention general product types or categories. "
    "If you do not find a suitable product, or if the user's query is outside the scope of product recommendations, "
    "always provide a helpful textual response, such as suggesting they browse our full catalog or contact support. "
    "**You must always provide a response, never an empty message or just whitespace.** "
    "You do not have real-time access to our specific product catalog, stock levels, or order details. "
    "Therefore, politely defer questions about specific product availability, prices, or order status "
    "by suggesting they check the website or contact customer support. "
    "Keep responses concise and to the point. Focus on recommending relevant products or categories."
)

User = get_user_model()

class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all().order_by('-created_at') # Order by most recently updated
    serializer_class = ChatSessionSerializer

    def get_queryset(self):
        """
        Custom queryset to filter sessions based on authentication.
        - Authenticated users see only their own active sessions.
        - Anonymous users should not be able to list/retrieve arbitrary sessions.
        """
        if self.request.user.is_authenticated:
            # Authenticated users can see their own active sessions.
            return self.queryset.filter(user=self.request.user, is_active=True)
        else:
            # Anonymous users should not see any sessions.
            # If the action is 'list', we return an empty queryset to prevent listing sessions.
            # This prevents anonymous users from listing sessions.
            if self.action == 'list':
                return ChatSession.objects.none()
            return self.queryset # For other actions, we allow access to sessions if they are anonymous.

    def get_permissions(self):
        """
        Configure permissions based on the action.
        - 'create': Allow any user (authenticated or anonymous) to create a session.
        - Other actions (retrieve, update, history, send_message, reset_session):
          Require either authentication and ownership, or be an anonymous session.
        """
        if self.action == 'create':
            # Allow any user to create a session (authenticated or anonymous).
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'history', 'send_message', 'reset_session']:
            # Require authentication for these actions, and ensure the user is the session owner
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSessionOwnerOrAnonymous]
        else:
            # For any other actions, default to authenticated users only
            self.permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """
        When creating a session:
        - If user is authenticated, associate the session with them.
        - If user is authenticated and already has active sessions, consider deactivating old ones
          (or adjust logic if multiple active sessions are desired).
        """
        user = self.request.user
        if user.is_authenticated:
            # For authenticated users, associate the session with them.
            # Optionally, deactivate any existing active sessions for this user.
            serializer.save(user=user, is_active=True)
        else:
            # For anonymous users, simply create the session.
            serializer.save(is_active=True)

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        Retrieves chat history for a specific session ID.
        Access is controlled by `get_object()` and `IsSessionOwnerOrAnonymous` permission.
        """
        try:
            session = self.get_object() # get_object() ensures the session exists and is accessible by the user.
            messages = session.messages.all()
            serializer = ChatMessageSerializer(messages, many=True)
            return Response(serializer.data)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Chat session not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": "You do not have permission to access this session."}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Sends a message to the chatbot within a specific session.
        Access is controlled by `get_object()` and `IsSessionOwnerOrAnonymous` permission.
        """
        try:
            session = self.get_object() # Get session instance, applying permissions
            user_message_text = request.data.get('message_text')
            if not user_message_text:
                return Response({"detail": "Message text is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Store user message immediately in the database
            ChatMessage.objects.create(session=session, sender='user', message_text=user_message_text)

            # --- AI Integration Logic ---
            if not openai_client:
                print("OpenAI client not initialized. Cannot make AI call.")
                return Response(
                    {'detail': 'AI service is currently unavailable due to initialization error.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE # Return an error status
                )
            
            try:
                # Fetch conversation history, ensuring system prompt is at the beginning
                conversation_history = ChatMessage.objects.filter(session=session).order_by('timestamp').values('sender', 'message_text')[:10]

                # Dynamically get categories for the system prompt
                categories_for_prompt = get_available_categories_for_prompt()
                system_prompt_content = SYSTEM_PROMPT_TEMPLATE.format(categories_list=categories_for_prompt)

                messages_for_ai = [
                    {"role": "system", "content": system_prompt_content} # Use the dynamic system prompt
                ]

                # Append historical messages, ensuring they don't exceed AI context window
                for msg in conversation_history:
                    if msg['sender'] == 'user':
                        messages_for_ai.append({"role": "user", "content": msg['message_text']})
                    elif msg['sender'] == 'chatbot':
                        messages_for_ai.append({"role": "assistant", "content": msg['message_text']})
                
                # Append the current user message
                messages_for_ai.append({"role": "user", "content": user_message_text})

                # Make the API call to DeepSeek
                response = openai_client.chat.completions.create(
                    model="deepseek/deepseek-r1:free", # Ensure the model is correctly specified
                    messages=messages_for_ai,
                    temperature=0.7,
                    max_tokens=500,
                    timeout=30.0 
                )
                
                chatbot_response_text = "I'm sorry, I couldn't get a valid response from the AI at this moment."
                if response.choices and response.choices[0].message and response.choices[0].message.content:
                    raw_ai_content = response.choices[0].message.content.strip() # Strip whitespace here

                    # Check if the content is empty after stripping
                    if raw_ai_content:
                        chatbot_response_text = raw_ai_content
                    else:
                        print("---DeepSeek API returned content that was empty after stripping whitespace.---")
                        chatbot_response_text = "I'm sorry, I couldn't generate a helpful response at this moment. Please try again."
                else:
                    # If the response structure is invalid or empty
                    print("DeepSeek API returned an empty or invalid message structure (no choices or message).")
                    return Response(
                        {'detail': 'The AI returned an invalid response structure. Please try again.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                # --- Extract and recommend products based on AI response ---
                # This function will parse the AI's response and return a queryset of recommended products
                recommended_products_qs = extract_and_recommend_products(chatbot_response_text)
                products_data = ProductSerializer(recommended_products_qs, many=True).data

                # --- ONLY SAVE CHATBOT MESSAGE IF AI CALL WAS SUCCESSFUL ---
                chatbot_message = ChatMessage.objects.create(session=session, sender='chatbot', message_text=chatbot_response_text)
                
                # Prepare response data, including products
                response_data = ChatMessageSerializer(chatbot_message).data
                response_data['products'] = products_data # <--- ADD PRODUCTS DATA HERE!

                return Response(response_data, status=status.HTTP_200_OK)

            # --- Error Handling for API Calls (RETURNS ERROR STATUS) ---
            except openai.APIConnectionError as e:
                print(f"DeepSeek API connection error: {e}")
                return Response(
                    {'detail': 'I\'m having trouble connecting to the AI. Please check your internet connection.'},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE # 503 Service Unavailable
                )
            except openai.RateLimitError as e:
                print(f"DeepSeek API rate limit exceeded: {e}")
                return Response(
                    {'detail': 'The AI service is currently very busy. Please try again in a few moments.'},
                    status=status.HTTP_429_TOO_MANY_REQUESTS # 429 Too Many Requests
                )
            except openai.APIStatusError as e:
                print(f"---DeepSeek API status error (Code: {e.status_code}): {e.response}")
                # Optional: Log the error details for debugging
                try:
                    error_details = e.response.json()
                    print(f"DeepSeek API Error Details: {error_details}")
                except (AttributeError, ValueError): # Handle cases where response is not JSON or has no content
                    pass

                if e.status_code == 401:
                    detail_message = "Authentication error with DeepSeek API. Please check your API key."
                    status_code = status.HTTP_401_UNAUTHORIZED
                elif e.status_code == 400: # Bad Request from DeepSeek
                    detail_message = "The AI request was malformed. Please try again."
                    status_code = status.HTTP_400_BAD_REQUEST
                else:
                    detail_message = "An error occurred with the AI service. Please try again later."
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR # Generic server error
                return Response(
                    {'detail': detail_message},
                    status=status_code
                )
            except openai.APITimeoutError as e:
                print(f"DeepSeek API request timed out: {e}")
                return Response(
                    {'detail': 'The AI took too long to respond. Please try again or ask a simpler question.'},
                    status=status.HTTP_504_GATEWAY_TIMEOUT # 504 Gateway Timeout
                )
            except Exception as e:
                print(f"Unexpected error during DeepSeek API call: {e}")
                return Response(
                    {'detail': 'An unexpected error occurred while processing your request. Please try again.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except ChatSession.DoesNotExist:
            return Response({"detail": "Chat session not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": "You do not have permission to send messages to this session."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"---Error in send_message: {e}") # Log the actual error for debugging
            return Response({"detail": "An internal server error occurred while processing your message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(detail=True, methods=['post'])
    def reset_session(self, request, pk=None):
        """
        Resets the current session by marking it inactive and creating a new one.
        Access is controlled by `get_object()` and `IsSessionOwnerOrAnonymous` permission.
        """
        try:
            old_session = self.get_object() # Get the session instance, applying permissions

            with transaction.atomic():
                # Mark the old session as inactive
                old_session.is_active = False
                old_session.save()

                # Create a new session. Link to user if authenticated, otherwise create anonymous.
                if request.user.is_authenticated:
                    new_session = ChatSession.objects.create(user=request.user, is_active=True)
                else:
                    new_session = ChatSession.objects.create(is_active=True)

                # Return the ID of the new session
                return Response({
                    "message": "Session reset successfully.",
                    "new_session_id": str(new_session.id)
                }, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response({"detail": "Session not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"detail": "You do not have permission to reset this session."}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"Error resetting session: {e}")
            return Response({"detail": "Failed to reset session."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Custom Permission to ensure users only access their own sessions or anonymous sessions
class IsSessionOwnerOrAnonymous(permissions.BasePermission):
    """
    Custom permission to allow:
    - Authenticated users to access their own sessions.
    - Anonymous users to access sessions that have no 'user' linked.
    """
    def has_object_permission(self, request, view, obj):

        # Check if the session has a user linked
        if obj.user is not None:
            # Only the linked user can access it.
            return request.user.is_authenticated and obj.user == request.user
        else:
            # Anonymous sessions can be accessed by any user.
            # This allows anonymous users to access sessions without a user linked.
            return True