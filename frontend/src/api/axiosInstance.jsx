import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; 

// This function retrieves the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Create an Axios instance with default settings
const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Your Django API base URL
  timeout: 35000, // Set a timeout for requests
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// Request Interceptor: Attach CSRF token for POST, PUT, PATCH, DELETE requests
axiosInstance.interceptors.request.use(
    config => {
        // Only attach CSRF token for methods that require it (POST, PUT, PATCH, DELETE)
        if (config.method === 'post' || config.method === 'put' || config.method === 'patch' || config.method === 'delete') {
            const csrftoken = getCookie('csrftoken'); // Get the CSRF token
            if (csrftoken) {
                config.headers['X-CSRFToken'] = csrftoken; // Add it to the headers
            }
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Request Interceptor: Attach Authorization header with access token
axiosInstance.interceptors.request.use(
    config => {
        const accessToken = localStorage.getItem('accessToken'); // Get token from localStorage
        if (accessToken) {
            config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// Response Interceptor: Handle token refresh and error responses
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response) {
      // This block handles errors where the server *sent a response* with an error status (e.g., 401, 404, 500)

      // If error is 401 Unauthorized and not already retrying
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;   // Mark the request as retried
        const refreshToken = localStorage.getItem('refreshToken');

        if (refreshToken) {
          try {
            // Decode the refresh token to check its validity
            const decodedRefreshToken = jwtDecode(refreshToken);
            const currentTime = Date.now() / 1000;
            if (decodedRefreshToken.exp < currentTime) {
              // Refresh token is expired
              console.log('Refresh token expired, logging out.');
              localStorage.clear();
              window.location.href = '/login'; // Redirect to login
              return Promise.reject(error); // Reject the original error
            }

            // Attempt to refresh the access token using the refresh token
            const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
              refresh: refreshToken,
            });

            localStorage.setItem('accessToken', response.data.access);
            // Update the Authorization header with the new access token
            originalRequest.headers.Authorization = `Bearer ${response.data.access}`;
            
            return axiosInstance(originalRequest); // Retry the original request with the new access token
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError);
            localStorage.clear();
            window.location.href = '/login';       // Redirect to login on refresh failure
            return Promise.reject(refreshError);   // Reject the refresh error
          }
        } else {
          // No refresh token available, log out
          console.log('No refresh token found, logging out.');
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(error); // Reject the original error
        }
      }
      // If the error is not 401 Unauthorized,
      // you can handle other status codes or errors here
      return Promise.reject(error);

    } else if (error.request) {
      // This block handles errors where the request was made but no response was received
      // This can happen if the server is down or there is a network issue
      console.error("Axios Interceptor: No response received from server. Check network or server status.", error.message);
      
      return Promise.reject(error); // Reject the error
    } else {
      // This block handles errors that occurred while setting up the request
      console.error("Axios Interceptor: Error setting up request:", error.message);
      return Promise.reject(error); // Reject the error
    }
  }
);

export default axiosInstance;