import '../src/CSS-files/ProductCard.css';
import { useNavigate } from 'react-router-dom';

function ProductCard({ product }) {
    const navigate = useNavigate();

    const handleViewDetails = () => {
        navigate(`/products?q=${product.name}`);
    };

  return (
    <div className="product-card">
      <img src={product.image_url || 'https://via.placeholder.com/100'} alt={product.name} />
      <h3>{product.name}</h3>
      <p>{product.description.substring(0, 70)}...</p>
      <p><strong>${product.price}</strong></p>
      <button onClick={() => handleViewDetails()}>View Details</button>
    </div>
  );
}

export default ProductCard;