import '../src/CSS-files/ViewProductDetails.css';

function ViewProductDetails({ product }) {
  return (
    <div className="product-details">
        <img src={product.image_url || 'https://via.placeholder.com/300'} alt={product.name} />
        <h1>{product.name}</h1>
        <p>{product.description}</p>
        <p>Price: ${product.price}</p>
        <h2>Stock: {product.stock_quantity > 0 ? product.stock_quantity + " available" : 'Out of Stock'}</h2>
        <button>Add to Cart</button>
    </div>
  );
}

export default ViewProductDetails;