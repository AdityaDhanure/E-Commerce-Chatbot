import React, { createContext, useContext, useState, useEffect, useMemo } from 'react';
import axiosInstance from './api/axiosInstance.jsx'; 
import {jwtDecode} from 'jwt-decode';
import { useCallback } from 'react'; 

// 1. Create the Context
const AuthContext = createContext(null);

// 2. Create the AuthProvider Component
export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [authToken, setAuthToken] = useState(null);
    const [user, setUser] = useState(null); 
    const [isLoading, setIsLoading] = useState(true); 

    // Function to handle login
    const login = useCallback((accessToken, refreshToken) => { 
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
        setAuthToken(accessToken);
        setIsAuthenticated(true);

        try {
            const decodedUser = jwtDecode(accessToken);
            setUser({
                id: decodedUser.user_id,
                username: decodedUser.username,
            });
        } catch (error) {
            console.error("Failed to decode access token:", error);
            logout();
        }
    }, []);

    // Function to fetch user details (e.g., username)
    const fetchUserDetails = async (token) => {
        try {
            const config = {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            };
            const response = await axiosInstance.get('api/user/', config);
            setUser(response.data); // Assuming response.data contains { id, username, etc. }           
        } catch (error) {
            console.error('Failed to fetch user details:', error);
            logout(); // If fetching user details fails, log out
        }
    };

    // Function to refresh the access token
    const refreshToken = async () => {
        try {
            const refresh = localStorage.getItem('refreshToken');
            if (!refresh) {
                return false; // No refresh token available
            }
            const response = await axiosInstance.post('api/token/refresh/', { refresh });
            const { access } = response.data;
            localStorage.setItem('accessToken', access);
            setAuthToken(access);
            return true; // Token refreshed
        } catch (error) {
            console.error('Token refresh failed:', error);
            logout(); // If refresh fails, log out
            return false;
        }
    };

    // Function to handle logout
    const logout = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('chatSessionId'); // CRUCIAL: Remove chat session ID on logout
        setAuthToken(null);
        setIsAuthenticated(false);
        setUser(null);
    };

    // Effect to check authentication status on mount
    useEffect(() => {
        const checkAuth = async () => {
            setIsLoading(true); // Start loading
            const accessToken = localStorage.getItem('accessToken');
            const refreshToken = localStorage.getItem('refreshToken');

            if (accessToken) {
                try {
                    const decoded = jwtDecode(accessToken);
                    const currentTime = Date.now() / 1000;

                    if (decoded.exp > currentTime) {
                        setAuthToken(accessToken);
                        setIsAuthenticated(true);
                        setUser({ // Set user from token payload
                            id: decoded.user_id,
                            username: decoded.username,
                        });
                        console.log('Existing access token is valid.');
                    } else if (refreshToken) {
                        console.log('Access token expired, attempting to refresh...');
                        try {
                            const response = await axiosInstance.post('/api/token/refresh/', { refresh: refreshToken });
                            const newAccessToken = response.data.access;
                            localStorage.setItem('accessToken', newAccessToken);
                            setAuthToken(newAccessToken);
                            setIsAuthenticated(true);
                            const decodedRefreshed = jwtDecode(newAccessToken);
                            setUser({ // Set user from new token payload
                                id: decodedRefreshed.user_id,
                                username: decodedRefreshed.username,
                            });
                            console.log('Tokens refreshed successfully.');
                        } catch (refreshError) {
                            console.error('Failed to refresh token:', refreshError);
                            logout(); // Use logout for consistency
                        }
                    } else {
                        logout(); // No refresh token, force logout
                    }
                } catch (error) {
                    console.error("Error decoding token or during initial auth check:", error);
                    logout(); // Malformed token, force logout
                }
            } else {
                console.log('No access token found in local storage.');
                setIsAuthenticated(false);
            }
            setIsLoading(false); // End loading
        };

        checkAuth();
    }, []);  // Run only once on mount

    // Memoize the context value to avoid unnecessary re-renders
    const contextValue = useMemo(() => ({
        isAuthenticated,
        authToken,
        user,
        isLoading,
        login,
        logout,
        refreshToken, // Function to refresh the token
        fetchUserDetails // Function to fetch user details
    }), [
        isAuthenticated,
        authToken,
        user,
        isLoading,
        login,
        logout,
        refreshToken,
        fetchUserDetails
    ]);

    // Render loading state while checking authentication
    if (isLoading) {
        return <div>Loading authentication...</div>; // You can customize this loading state
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
};

// 3. Create the custom hook for easy consumption
export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};