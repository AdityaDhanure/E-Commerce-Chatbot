import os
from deepseek import Deepseek
import re

# Initialize Deepseek client
client = Deepseek(api_key=os.environ.get("DEEPSEEK_API_KEY"))

# Define a function to extract product names from AI's response text
def extract_product_names_from_text(text, all_products):
    found_product_names = set()
    # Sort product names by length in descending order to prioritize longer, more specific matches
    sorted_product_names = sorted([p.name for p in all_products], key=len, reverse=True)

    # Use regex to find whole word matches in the text
    # \b ensures whole word match, re.escape handles special characters in product names
    for product_name in sorted_product_names:
        # Create a regex pattern for whole word match, case-insensitive
        pattern = r'\b' + re.escape(product_name) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            found_product_names.add(product_name)
    
    # Convert found names back to product objects
    found_products = [p for p in all_products if p.name in found_product_names]
    return found_products


def get_deepseek_response(chat_history_objects, all_products_queryset):
    messages = []
    # Add system message to guide the AI
    # MODIFIED INSTRUCTION: Explicitly tell it NOT to suggest products for simple greetings
    system_message_content = (
        "You are an AI assistant for an e-commerce website. "
        "Your primary goal is to assist users with product inquiries and provide helpful information. "
        "When asked about products or product categories, recommend specific items available in our store, "
        "mentioning their key features (e.g., 'Dell XPS 13 Ultrabook (Lightweight, 4K display)'). "
        "Present recommended products in a numbered list format within your response. "
        "If the user's message is *only* a simple greeting (e.g., 'hello', 'hi', 'thank you', 'good morning', 'good evening', 'well done'), "
        "respond with a friendly, conversational message without mentioning or recommending *any* products. "
        "Do not list products unless the user is specifically asking for product recommendations or information related to products/categories. "
        "Your product recommendations must be from the following list:\n"
    )

    # Append available product names and a brief feature
    for product in all_products_queryset:
        # Ensure product has a name and description
        system_message_content += f"- {product.name} ({product.description})\n"
    
    messages.append({"role": "system", "content": system_message_content})

    # Add chat history
    for msg in chat_history_objects:
        messages.append({"role": msg.sender, "content": msg.message_text})

    try:
        # Make the API call
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False, # We need the full response to extract products
            max_tokens=250, # Adjust as needed
            temperature=0.7, # Adjust as needed
        )
        ai_response_text = response.choices[0].message.content
        
        # Extract products based on the AI's response text.
        # If the system prompt works as intended for greetings, ai_response_text
        # will not contain product names, and this function will correctly return an empty list.
        extracted_products = extract_product_names_from_text(ai_response_text, all_products_queryset)

        # Return the AI's text response and the list of extracted product objects
        return ai_response_text, extracted_products

    except Exception as e:
        print(f"Error getting Deepseek response: {e}")
        return "I apologize, but I'm currently unable to process your request.", []