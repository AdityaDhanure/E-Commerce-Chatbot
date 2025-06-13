import React, { useState, useEffect, useRef, useCallback } from 'react';
import axiosInstance from '../src/api/axiosInstance.jsx';
import '../src/CSS-files/ChatbotPage.css';
import ProductCard from '../components/ProductCard.jsx';
import TextWithLineBreaks from '../components/TextWithLineBreaks';
import { useAuth } from '../src/AuthContext.jsx';

function ChatbotPage() {
    const { isAuthenticated, authToken, user, isLoading: authLoading } = useAuth();
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [sessionId, setSessionId] = useState(null);
    const [isPageLoading, setIsPageLoading] = useState(true);
    const [isAITyping, setIsAITyping] = useState(false);
    const chatWindowRef = useRef(null);

    // --- EFFECT 1: Initialize chat session based on authentication state ---
    const initializeSession = useCallback(async () => {
        if (authLoading) {
            console.log("AuthContext still loading, delaying session initialization...");
            return;
        }

        setIsPageLoading(true); // Set page loading to true while initializing session

        let currentSessionId = localStorage.getItem('chatSessionId');
        let headers = {};

        try {
            if (isAuthenticated && authToken) {
                headers = { Authorization: `Bearer ${authToken}` };
                console.log('User is authenticated. Attempting to get/create user-specific session...');

                const userSessionsResponse = await axiosInstance.get('chat/sessions/', { headers });
                const fetchedSessions = userSessionsResponse.data;

                let sessionToLoad = null;
                // Check if there are any existing sessions for the authenticated user
                if (fetchedSessions && fetchedSessions.results && fetchedSessions.results.length > 0) {
                    const sortedSessions = fetchedSessions.results.sort((a, b) => {
                        return new Date(b.updated_at) - new Date(a.updated_at);
                    });
                    sessionToLoad = sortedSessions[0];

                    if (currentSessionId && currentSessionId === sessionToLoad.id) {
                        console.log('Loading existing user session from localStorage (matching backend):', currentSessionId);
                    } else {
                        currentSessionId = sessionToLoad.id;
                        localStorage.setItem('chatSessionId', currentSessionId);
                        console.log('User has new most recent session from backend, loading:', currentSessionId);
                    }

                    setSessionId(currentSessionId);

                    // Fetch historical messages for the authenticated user session
                    const historyResponse = await axiosInstance.get(`chat/sessions/${currentSessionId}/history/`, { headers });
                    const historicalMessages = historyResponse.data.map(msg => ({
                        sender: msg.sender,
                        message_text: msg.message_text,
                        timestamp: msg.timestamp,
                        products: msg.products || [],
                    }));

                    if (historicalMessages.length === 0) {
                        setMessages([{ sender: 'chatbot', message_text: 'Welcome back! How can I help you today?', timestamp: new Date().toISOString() }]);
                    } else {
                        setMessages(historicalMessages);
                    }
                    console.log('Historical messages for authenticated user:', historicalMessages);

                } else {
                    console.log('No existing user sessions for authenticated user, creating a new one...');
                    const newSessionResponse = await axiosInstance.post('chat/sessions/', {}, { headers });
                    sessionToLoad = newSessionResponse.data;
                    currentSessionId = sessionToLoad.id;
                    localStorage.setItem('chatSessionId', currentSessionId);
                    setSessionId(currentSessionId);
                    setMessages([{ sender: 'chatbot', message_text: 'Hello! How can I help you today?', timestamp: new Date().toISOString() }]);
                    console.log('New authenticated user session created:', currentSessionId);
                }

            } else {
                // --- Anonymous User Logic ---
                console.log('User is anonymous. Checking for existing anonymous session ID...');
                if (currentSessionId) {
                    try {
                        const sessionCheckResponse = await axiosInstance.get(`chat/sessions/${currentSessionId}/`);
                        const sessionDetails = sessionCheckResponse.data;
                        console.log('Found and loaded existing anonymous session from localStorage:', sessionDetails.id);
                        setSessionId(currentSessionId);

                        // Fetch historical messages for the anonymous session
                        const historyResponse = await axiosInstance.get(`chat/sessions/${currentSessionId}/history/`);
                        const historicalMessages = historyResponse.data.map(msg => ({
                            sender: msg.sender,
                            message_text: msg.message_text,
                            timestamp: msg.timestamp,
                            products: msg.products || [],
                        }));
                        if (historicalMessages.length === 0) {
                            setMessages([{ sender: 'chatbot', message_text: 'Welcome back! How can I help you today?', timestamp: new Date().toISOString() }]);
                        } else {
                            setMessages(historicalMessages);
                        }
                        console.log('Historical messages for anonymous session:', historicalMessages);

                    } catch (error) {
                        console.warn('Existing anonymous session ID from localStorage failed validation/load, creating new:', error);
                        localStorage.removeItem('chatSessionId');
                        currentSessionId = null;
                    }
                }

                if (!currentSessionId) {
                    console.log('No valid anonymous session ID found, creating new anonymous session...');
                    const response = await axiosInstance.post('chat/sessions/', {});
                    currentSessionId = response.data.id;
                    localStorage.setItem('chatSessionId', currentSessionId);
                    setSessionId(currentSessionId);
                    setMessages([{ sender: 'chatbot', message_text: 'Hello! It is a new Anonymous session, How can I help you today?', timestamp: new Date().toISOString() }]);
                    console.log('New anonymous session created:', response.data);
                }
            }
        } catch (error) {
            console.error('Error during session initialization:', error);
            setMessages([{ sender: 'chatbot', message_text: 'An error occurred during chat initialization. Please refresh.', timestamp: new Date().toISOString() }]);
            
            if (error.response && error.response.status === 401) {
                console.log("Authentication token invalid, attempting to clear and re-initialize.");
                localStorage.removeItem('chatSessionId');
                setSessionId(null);
                setMessages([]);
            } else {
                localStorage.removeItem('chatSessionId');
                setSessionId(null);
                setMessages([]);
            }
        } finally {
            setIsPageLoading(false); // Hide loading state after session initialization
        }
    }, [isAuthenticated, authToken, authLoading]);

    // --- EFFECT 1: Initialize session on mount or auth change ---
    useEffect(() => {
        initializeSession();
    }, [initializeSession]);

    // --- EFFECT 2: Auto-scroll to the latest message ---
    useEffect(() => {
        if (chatWindowRef.current) {
            chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
        }
    }, [messages, isAITyping]); // Re-run when messages change or AI typing state changes

    
    // --- Function to handle sending a message ---
    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || !sessionId) {
            console.warn("Attempted to send empty message or no session ID.");
            return;
        }

        const userMessage = {
            sender: 'user',
            message_text: inputMessage.trim(),
            id: `temp-${Date.now()}`, // Use a temporary ID for optimistic updates
            timestamp: new Date().toISOString()
        };

        setMessages((prevMessages) => [...prevMessages, userMessage]); // Optimistically add user message
        setInputMessage('');

        setIsAITyping(true);

        try {
            const response = await axiosInstance.post(`chat/sessions/${sessionId}/send_message/`,
                { message_text: userMessage.message_text }
            );

            const chatbotResponseData = response.data;

            const chatbotMessage = {
                id: chatbotResponseData.id,
                sender: chatbotResponseData.sender,
                message_text: chatbotResponseData.message_text,
                timestamp: chatbotResponseData.timestamp,
                products: chatbotResponseData.products || [],
            };
            setMessages((prevMessages) => [...prevMessages, chatbotMessage]);

        } catch (error) {
            console.error('Error sending message:', error);
            setMessages((prevMessages) => {
                const updatedMessages = prevMessages.filter(msg => msg.id !== userMessage.id); // Remove optimistic user message
                return [
                    ...updatedMessages,
                    { sender: 'chatbot', message_text: `Apologies, something went wrong: ${error.response?.data?.detail || error.message}. Please try again.`, timestamp: new Date().toISOString(), isError: true },
                ];
            });
            // Re-initialize session on certain errors if the session became invalid
            if (error.response && (error.response.status === 401 || error.response.status === 404 || error.response.status === 403)) {
                console.warn('Session invalid during message send, attempting re-initialization.');
                localStorage.removeItem('chatSessionId');
                setSessionId(null);
            }
        } finally {
            setIsAITyping(false);
        }
    };

    // --- Function to handle resetting the chat session ---
    const handleResetSession = async () => {
        if (window.confirm("Are you sure you want to reset the conversation? This will start a new chat session.")) {
            setIsPageLoading(true); // Show loading state while resetting
            try {
                if (sessionId) {
                    const response = await axiosInstance.post(
                        `chat/sessions/${sessionId}/reset_session/`,
                        {}
                    );

                    const newSessionId = response.data.new_session_id;
                    if (newSessionId) {
                        localStorage.setItem('chatSessionId', newSessionId);
                        setSessionId(newSessionId);
                        setMessages([]); // Clear old messages
                        console.log('Session reset on backend. New session ID:', newSessionId);
                        setMessages((prevMessages) => [
                            ...prevMessages,
                            { sender: 'chatbot', message_text: 'Session reset. Hello! How can I help you today?', timestamp: new Date().toISOString() }
                        ]);
                    } else {
                        console.error('Backend did not return a new session ID after reset.');
                        alert('Session reset failed: No new session ID received.'); 
                    }
                } else {
                    console.log('No current session to reset, just clearing local storage and re-initializing.');
                    localStorage.removeItem('chatSessionId');
                    setSessionId(null);
                    setMessages([]);
                }
            } catch (error) {
                console.error('Error resetting session:', error);
                alert('Failed to reset session. Please try refreshing the page.');
                localStorage.removeItem('chatSessionId');
                setSessionId(null);
                setMessages([]);
            } finally {
                setIsPageLoading(false); // Hide loading state after reset
            }
        }
    };

    // --- Loading State ---
    if (authLoading || isPageLoading) {
        return <div className="chatbot-loading">Loading chat...</div>;
    }


    return (
        <div className="chatbot-container">
            <div className="chat-window" ref={chatWindowRef}>
                {messages.map((msg, index) => (
                    // Use a unique key for each message, falling back to index if no ID
                    <div key={msg.id || index} className={`message ${msg.sender} ${msg.isError ? 'error' : ''}`}>
                        <div className="message-bubble">
                            <p><TextWithLineBreaks text={msg.message_text} /></p>
                            {/* Display products if available */}
                            {msg.products && msg.products.length > 0 && (
                                <div className="product-display-area">
                                    <h4 className='mt-5'>Found Products:</h4>
                                    <div className="product-cards-container">
                                        {msg.products.map(product => (
                                            <ProductCard key={product.id} product={product} />
                                        ))}
                                    </div>
                                </div>
                            )}
                            <span className="timestamp">
                                {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                        </div>
                    </div>
                ))}

                {isAITyping && (
                    <div className="message chatbot loading"> {/* Reusing existing message classes */}
                        <div className="message-bubble">
                            <p>Responding... <span className="spinner"></span></p>
                        </div>
                    </div>
                )}
            </div>
            <form onSubmit={handleSendMessage} className="message-input-form">
                <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    placeholder="Type your message..."
                    className="message-input"
                    aria-label="Type your message"
                    disabled={isAITyping} 
                />
                <button 
                    type="submit" 
                    className="send-button" 
                    disabled={isAITyping} 
                >
                    Send
                </button>
                <button 
                    type="button" 
                    onClick={handleResetSession} 
                    className="reset-button"
                    disabled={isAITyping} 
                >
                    Reset Chat
                </button>
            </form>
        </div>
    );
}

export default ChatbotPage;