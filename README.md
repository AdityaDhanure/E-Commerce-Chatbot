# E-commerce Sales Chatbot

## Project Overview

In the highly competitive e-commerce landscape, this project presents the development of a comprehensive, AI-powered sales chatbot specifically tailored for an e-commerce platform having various categories of products.The primary objective of this chatbot is to enhance the shopping experience by enabling efficient product search, exploration, and purchase processes. It aims to elevate customer interaction and streamline business operations by providing advanced, interactive, and user-centric assistance from initial product inquiries to purchase facilitation.

## Key Features

* **User Authentication:** Secure login and registration system for users, including session management to maintain user state throughout interactions.
* **Real-time Chat Interface:** A responsive and intuitive chatbot interface compatible with desktop, tablet, and mobile devices, utilizing modern JavaScript frameworks. Features include conversation reset buttons and session tracking with timestamps.
* **AI-Powered Product Recommendations:** Integrates with an LLM (Large Language Model) to understand user queries and recommend specific products from the store's inventory, along with their key features.
* **Intelligent Greeting Handling:** The chatbot intelligently distinguishes between simple greeting messages and product-related inquiries, responding conversationally to greetings without unsolicited product recommendations.
* **Persistent Chat History:** All chat interactions are stored effectively in the backend for later retrieval and analysis, ensuring session continuity.
* **Product Search Page:** A dedicated page allowing users to browse and search for products directly.
* **RESTful API Backend:** An API-driven backend system using Python with Django, capable of processing search queries and fetching relevant product data from a database. It handles a mock inventory via RESTful interactions.

## Technologies Used

### Frontend

* **React.js:** A JavaScript library for building user interfaces.
* **Vite:** A fast build tool that provides a rapid development experience for React applications.
* **React Router DOM:** For declarative routing within the single-page application.
* **Axios:** A promise-based HTTP client for making API requests to the backend.
* **jwt-decode:** A library for decoding JSON Web Tokens, useful for extracting user information from JWTs on the client-side.
* **Pure CSS:** For styling the application, ensuring a clean and responsive design.

### Backend

* **Django:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
* **Django REST Framework (DRF):** A powerful and flexible toolkit for building Web APIs.
* **PostgreSQL:** A powerful, open-source relational database system used for storing application data, including user information, chat sessions, messages, and product details.
* **djangorestframework-simplejwt:** Provides a simple way to implement JSON Web Token (JWT) authentication for Django REST Framework APIs.
* **django-filter:** Integrates filtering capabilities into Django REST Framework, allowing for easy creation of filtering backends for product and other list views.
* **django-cors-headers:** A Django application to handle Cross-Origin Resource Sharing (CORS) headers, essential for allowing frontend (React) to communicate with the backend (Django) on different origins during development and deployment.

### AI/LLM Integration

* **Deepseek API:** Utilized for advanced natural language understanding and generation, powering the chatbot's conversational capabilities and product recommendation logic.
* **Deepseek Python Client:** The official Python SDK for interacting with the Deepseek API.

## Setup and Installation

Follow these steps to get the E-commerce Sales Chatbot up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

* **Python:** Version 3.x (e.g., Python 3.13.0, is used in my environment).
* **Node.js:** A JavaScript runtime (LTS version recommended).
* **npm** (Node Package Manager): Comes with Node.js.
* **pip:** Python package installer (comes with Python).
* **PostgreSQL:** Ensure you have a PostgreSQL server running and configured for your project.

### Backend Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AdityaDhanure/E-Commerce-Chatbot.git
    cd E-Commerce-Chatbot/backend
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv

    # On Windows:
        ./venv/Scripts/activate
    # On macOS/Linux:
        source venv/bin/activate
    ```
3.  **Install backend dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up Environment Variables:**
    Create a `.env` file in your `backend` directory and add your environment variables.
    ```env
    # Environment variables for the backend application 
    # DEEPSEEK R1 free model, visit https://openrouter.ai/deepseek/deepseek-r1:free to create your own
    DEEPSEEK_API_KEY = <your-API-key> 
    DEEPSEEK_BASE_URL='https://openrouter.ai/api/v1'

    # For token-based authentication
    SECRET_KEY = <your-secret-key>

    # Database configuration
    DB_ENGINE = django.db.backends.postgresql
    DB_NAME = <your-db-name>
    DB_USER = <your-db-user-name>
    DB_PASSWORD = <your-db-password>
    DB_HOST = localhost
    DB_PORT = 5432
    ```
5.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a superuser (for Django Admin):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your admin account.
7.  **Populate initial product data:**
    Run your `populate_product.py` (path: 'backend/products/management/commands/populate_products.py') script to add mock product entries to the database.
    ```bash
    python manage.py shell < ../populate_product.py
    ```
8.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```
    The backend will typically run on `http://127.0.0.1:8000/`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd ../frontend
    ```
2.  **Install frontend dependencies:**
    ```bash
    npm install
    # Or if you use yarn:
    # yarn install
    ```
3.  **Start the React development server:**
    ```bash
    npm run dev
    # Or if you use yarn:
    # yarn dev
    ```
    The frontend will typically run on `http://localhost:5173/` (Vite's default).

## Project Structure

The project follows a modular structure, separating backend and frontend components.

```
4.E-COMMERCE-CHATBOT/
├── backend/
│   ├── accounts/                       # Django app for user authentication
│   │   ├── __pycache__/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── chat/                           # Django app for chatbot logic, sessions, and messages
│   │   ├── __pycache__/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── llm_integration.py          # AI (Deepseek) integration and prompt management
│   │   ├── models.py                   # ChatSession, ChatMessage models
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── chatbot_backend/                # Main Django project settings
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── serializers.py              # (Possibly global serializers or base serializer)
│   │   ├── settings.py                 # Project settings
│   │   ├── urls.py                     # Project-level URL routing
│   │   └── wsgi.py
│   ├── products/                       # Django app for product management
│   │   ├── __pycache__/
│   │   ├── management/commands/populate_products.py    # To store the data into your PostgresSQL Database tables
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py                   # ProductCategory, Product models
│   │   ├── serializers.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── venv/                           # Python virtual environment
│   ├── .env                            # Environment variables for Django
│   ├── .gitignore
│   └── manage.py                       # Django's command-line utility
├── frontend/                           # React.js application
│   ├── components/                     # Reusable React components
│   │   ├── ProductCard.jsx            
│   │   ├── TextWithLineBreaks.jsx     
│   │   └── ViewProductDetails.jsx     
│   ├── node_modules/                   # Installed Node.js packages
│   ├── pages/                          # Main application pages
│   │   ├── ChatbotPage.jsx            
│   │   ├── LoginPage.jsx              
│   │   └── ProductSearchPage.jsx      
│   ├── public/                         # Static assets served directly
│   ├── src/                            # Source code for the React app
│   │   ├── api/                        # API related configurations
│   │   │   └── axiosInstance.js        # Axios instance with CSRF interceptor
│   │   ├── assets/                     # Static assets (images, etc.)
│   │   ├── CSS-files/                  # Project-wide CSS styles
│   │   │   ├── App.css                
│   │   │   ├── ChatbotPage.css        
│   │   │   ├── LoginPage.css          
│   │   │   ├── ProductCard.css        
│   │   │   ├── ProductSearchPage.css  
│   │   │   └── ViewProductDetails.css 
│   │   ├── App.jsx                     # Main application component
│   │   ├── AuthContext.jsx             # Authentication context
│   │   ├── index.css                   # Global CSS styles
│   │   └── main.jsx                    # Entry point for React application
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## API Endpoints

The backend exposes the following key API endpoints:

* `/admin/`: Django administration interface.
* `/api/token/`: Obtain authentication tokens (for login).
* `/api/token/refresh/`: Refresh expired authentication tokens.
* `/api/register/`: Register a new user.
* `/api/products/`: Retrieve a list of all products.
* `/api/products/?search={query}`: Search for products by name or description.
* `/api/categories/`: Retrieve a list of product categories.
* `/api/chat/sessions/`: Create a new chat session.
* `/api/chat/sessions/{sessionId}/`: Retrieve or manage a specific chat session.
* `/api/chat/sessions/{sessionId}/history/`: Retrieve the message history for a specific session.
* `/api/chat/sessions/{sessionId}/send_message/`: Send a new message to the chatbot within a session.
* `/api/chat/sessions/{sessionId}/reset_session/`: Reset a chat session, clearing its history.

## Database Schema

The project uses a PostgreSQL database with the following main models:

### `ChatSession` (from `chat` app)

* `id` (UUIDField, Primary Key): Unique identifier for each chat session.
* `user` (ForeignKey to User, Nullable): Links the session to a user (allows anonymous sessions).
* `created_at` (DateTimeField): Timestamp of session creation.
* `updated_at` (DateTimeField): Timestamp of last session update.
* `is_active` (BooleanField): Indicates if the session is currently active.

### `ChatMessage` (from `chat` app)

* `session` (ForeignKey to ChatSession): Links the message to its parent chat session.
* `sender` (CharField): Indicates who sent the message ('user' or 'chatbot').
* `message_text` (TextField): The content of the message.
* `timestamp` (DateTimeField): The time the message was sent.
* `products` (JSONField, Nullable): Stores product data returned by the chatbot, allowing for flexible structure of recommended products within the message.

### `ProductCategory` (from `products` app)

* `name` (CharField, Unique): Name of the product category (e.g., 'Laptops', 'Smartphones').
* `description` (TextField, Nullable): Optional description for the category.

### `Product` (from `products` app)

* `name` (CharField): Name of the product.
* `description` (TextField): Detailed description of the product.
* `price` (DecimalField): Price of the product.
* `category` (ForeignKey to ProductCategory, Nullable): Links the product to its category.
* `stock_quantity` (IntegerField): Current quantity of the product in stock.
* `image_url` (URLField, Nullable): URL to the product's image.
* `sku` (CharField, Unique, Nullable): Stock Keeping Unit for the product.
* `is_available` (BooleanField): Indicates if the product is currently available.
* `created_at` (DateTimeField): Timestamp of product creation.
* `updated_at` (DateTimeField): Timestamp of last product update.

## Problems Faced and Resolutions

During the development of this project, several common challenges were encountered and successfully resolved, showcasing adaptability and problem-solving skills:

1.  **Markdown Bold (`**`) in AI Responses:**
    * **Problem:** The AI model (Deepseek) would include Markdown bold syntax (`**`) around product names in its text responses, which was not rendered correctly by the frontend, leading to an unprofessional look.
    * **Resolution:** Implemented a JavaScript function (`removeMarkdownBold`) within the `TextWithLineBreaks.jsx` component on the frontend. This function now explicitly strips the `**` characters from the AI's message text before it is rendered, ensuring proper display.

2.  **AI Unnecessarily Recommending Products for Greetings:**
    * [cite_start]**Problem:** The chatbot would sometimes offer product recommendations even when the user's input was solely a greeting (e.g., "Hello," "Thank you," "Good morning"), leading to an awkward user experience[cite: 9].
    * **Resolution:** Enhanced the system prompt sent to the Deepseek LLM in `llm_integration.py`. The prompt now explicitly instructs the AI to detect simple greeting messages and, in such cases, respond conversationally without mentioning or recommending any products. This leverages the LLM's intelligence to handle different user intents appropriately.

3.  **"Invalid Hook Call" Error on Logout:**
    * **Problem:** An `Invalid Hook Call` error occurred because a `useEffect` hook was incorrectly placed inside a regular JavaScript function (`handleLogout`) in `App.jsx`, violating React's Rules of Hooks. This prevented proper navigation after logout.
    * **Resolution:** The `useEffect` hook responsible for navigating to the login page after authentication state changes was moved to the top level of the `App` functional component. It now correctly monitors the `isAuthenticated` state from the `AuthContext` and triggers navigation when the user logs out.

4.  **Deepseek API Rate Limiting (429 Too Many Requests):**
    * **Problem:** During development and testing, frequent API calls to Deepseek sometimes resulted in `429 Too Many Requests` errors, indicating hitting API rate limits.
    * **Resolution:** The recommended solution involved implementing a retry mechanism with exponential backoff for API calls made via Axios. This approach, ideally implemented in `handleSendMessage` or globally via an Axios interceptor in `axiosInstance.js`, allows the application to automatically retry failed requests after a progressively longer delay, mitigating rate limit issues.

5.  **CSRF Token Handling for Django Backend:**
    * **Problem:** Requests from the React frontend to the Django backend (especially `POST` requests) require a CSRF token for security purposes, as enforced by Django's built-in protection. Without this token, requests would be rejected with a `403 Forbidden` error.
    * **Resolution:** The `getCookie` helper function was established to retrieve the `csrftoken` from the browser's cookies. This function is then integrated into an Axios request interceptor within `axiosInstance.js`. This ensures that the `X-CSRFToken` header is automatically attached to all relevant outgoing API requests, satisfying Django's security requirements.

## Future Enhancements

* Integration of a proper real-world product dataset rather than the specific mock data provided in `populate_products.py`.
* Further refinement of AI's understanding for more complex queries and follow-up questions.
* Implementation of advanced filtering and sorting options on the product search page.
* Adding user review and rating functionalities.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---