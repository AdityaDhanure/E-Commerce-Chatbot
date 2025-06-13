import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import '../src/CSS-files/ProductSearchPage.css';
import ViewProductDetails from '../components/ViewProductDetails';

// Function to fetch products from the Django API
const fetchProducts = async (query = '') => {
    try {
        const response = await fetch(`http://localhost:8000/api/products/?search=${query}`); // Use your Django API endpoint
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data; // Assuming your API returns an array of products
    } catch (error) {
        console.error("Error fetching products:", error);
        throw error; // Re-throw to be caught by the component
    }
};

// Main component for the Product Search Page
function ProductSearchPage() {
  const [searchParams, setSearchParams] = useSearchParams(); // Hook to read/write URL params
  const [searchTerm, setSearchTerm] = useState(''); // Local state for input field
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // useEffect to read URL params and fetch data on initial load or URL change
  useEffect(() => {
    const queryFromUrl = searchParams.get('q'); // Get the 'q' parameter from URL
    if (queryFromUrl) {
      setSearchTerm(queryFromUrl); // Set input field to current URL query
      performSearch(queryFromUrl); // Trigger search based on URL query
    } else {
      setProducts([]); 
    }
  }, [searchParams]);

  // Function to perform the search and fetch products
  const performSearch = async (query) => {
    setLoading(true);
    setError(null);
    try {
      const responseData = await fetchProducts(query); // Call your API function
      if (responseData && Array.isArray(responseData.results)) {
        setProducts(responseData.results); // Use the array from the 'results' key
      } else if (Array.isArray(responseData)) {
        setProducts(responseData); // If the API returns a direct array (no pagination)
      } else {
        console.error("API response is not an array or does not contain a 'results' array:", responseData);
        setProducts([]); // Ensure products is always an array
      }
    } catch (err) {
      setError("Failed to fetch products: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    setSearchParams({ q: searchTerm }); // Update URL with the search term
  };

  return (
    <div className="product-search-page">
      <h1>Discover Products</h1>
      <form onSubmit={handleSubmit} className="search-form">
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by name or description..."
          className="search-input border"
        />
        <button type="submit" className="search-button">Search</button>
      </form>

      {loading && <p className="loading-message">Loading products...</p>}
      {error && <p className="error-message">{error}</p>}

      {!loading && !error && products.length === 0 && searchTerm && (
        <p className="no-results-message">No products found for "{searchTerm}".</p>
      )}
      {!loading && !error && products.length === 0 && !searchTerm && (
        <p className="no-results-message">Start searching for products!</p>
      )}

      <div className="product-grid">
        {products.length > 0 ? (
          products.map((product) => (
            <ViewProductDetails key={product.id} product={product} />
          ))
        ) : (
          !loading && !error && <p>No products found. Try a different search.</p>
        )}
      </div>
    </div>
  );
}

export default ProductSearchPage;

