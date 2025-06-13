from django.core.management.base import BaseCommand
from products.models import ProductCategory, Product
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populates the database with specific, relevant product categories and products.'

    def handle(self, *args, **kwargs):
        fake = Faker('en_IN') # Use Indian locale for relevant mock data like descriptions

        self.stdout.write("Deleting existing product and category data...")
        Product.objects.all().delete()
        ProductCategory.objects.all().delete()
        self.stdout.write("Existing data deleted.")

        categories_data = [
            {'name': 'Laptops', 'description': 'High-performance and portable computing devices for work, study, and gaming.'},
            {'name': 'Groceries', 'description': 'Fresh produce, pantry staples, dairy, and frozen goods for daily needs.'},
            {'name': 'Smartphones', 'description': 'Cutting-edge mobile communication devices with advanced features.'},
            {'name': 'Televisions', 'description': 'Home entertainment display units, from smart TVs to projectors.'},
            {'name': 'Books', 'description': 'Fiction, non-fiction, academic literature, and children\'s books.'},
            {'name': 'Fashion', 'description': 'Apparel, footwear, and accessories for men, women, and kids.'},
            {'name': 'Home Appliances', 'description': 'Essential appliances for cooking, cleaning, and home comfort.'},
            {'name': 'Sports & Outdoors', 'description': 'Equipment and apparel for various sports, fitness, and outdoor activities.'},
            {'name': 'Beauty & Personal Care', 'description': 'Skincare, haircare, makeup, fragrances, and personal grooming products.'},
            {'name': 'Furniture', 'description': 'Items for furnishing a home or office, including chairs, tables, and beds.'},
            {'name': 'Electronics Accessories', 'description': 'Peripherals and add-ons for electronic devices.'},
            {'name': 'Kids & Baby', 'description': 'Products for infants, toddlers, and young children, including toys and clothing.'},
        ]

        self.stdout.write("Creating categories...")
        created_categories = {}
        for data in categories_data:
            category, created = ProductCategory.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            created_categories[category.name] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            else:
                self.stdout.write(f'Category already exists: {category.name}')

        # --- MODIFIED SPECIFIC PRODUCTS DATA WITH image_url AND stock_quantity ---
        specific_products_by_category = {
            'Laptops': [
                {'name': 'Dell XPS 15', 'description': 'High-performance laptop for creators.', 'price': 1499.99, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/1/200/300'},
                {'name': 'HP Spectre x360', 'description': 'Premium 2-in-1 convertible laptop.', 'price': 1299.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/2/200/300'},
                {'name': 'Lenovo ThinkPad X1 Carbon', 'description': 'Business-class ultrabook with robust security.', 'price': 1599.50, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/3/200/300'},
                {'name': 'Apple MacBook Air M2', 'description': 'Sleek and efficient laptop for everyday tasks.', 'price': 1199.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/4/200/300'},
                {'name': 'Asus ROG Zephyrus G14', 'description': 'Compact yet powerful gaming laptop with AMD CPU.', 'price': 1600.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/5/200/300'},
                {'name': 'Microsoft Surface Laptop 5', 'description': 'Elegant and fast laptop with touchscreen.', 'price': 1300.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/6/200/300'},
                {'name': 'Acer Swift 3', 'description': 'Lightweight and portable laptop for students.', 'price': 650.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/7/200/300'},
                {'name': 'MSI Creator M16', 'description': 'Laptop designed for graphic design and video editing.', 'price': 1400.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/8/200/300'},
                {'name': 'Razer Blade 14', 'description': 'Ultra-compact gaming laptop with powerful GPU.', 'price': 1800.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/id/9/200/300'},
                {'name': 'LG Gram 17', 'description': 'Feather-light 17-inch laptop with long battery life.', 'price': 1250.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/10/200/300'},
                {'name': 'Dell Inspiron 14', 'description': 'Versatile laptop for home and office use.', 'price': 750.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/11/200/300'},
                {'name': 'HP Envy 13', 'description': 'Stylish and powerful ultrabook for general use.', 'price': 999.00, 'stock_quantity': 42, 'image_url': 'https://picsum.photos/id/12/200/300'},
                {'name': 'Lenovo IdeaPad Flex 5', 'description': 'Affordable 2-in-1 convertible laptop.', 'price': 600.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/13/200/300'},
                {'name': 'Samsung Galaxy Book 3 Pro', 'description': 'Thin and light laptop with vibrant AMOLED display.', 'price': 1350.00, 'stock_quantity': 33, 'image_url': 'https://picsum.photos/id/14/200/300'},
                {'name': 'Alienware m18', 'description': 'Large screen, high-performance gaming laptop.', 'price': 2500.00, 'stock_quantity': 10, 'image_url': 'https://picsum.photos/id/15/200/300'},
                {'name': 'Chromebook Flip CX5', 'description': 'Fast and secure Chromebook for cloud-based tasks.', 'price': 700.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/16/200/300'},
                {'name': 'Gigabyte Aero 16', 'description': 'High-end laptop for content creation and gaming.', 'price': 2000.00, 'stock_quantity': 18, 'image_url': 'https://picsum.photos/id/17/200/300'},
                {'name': 'Honor MagicBook 14', 'description': 'Sleek and affordable laptop for daily use.', 'price': 680.00, 'stock_quantity': 52, 'image_url': 'https://picsum.photos/id/18/200/300'},
                {'name': 'Dynabook Tecra A50-J', 'description': 'Reliable business laptop with essential features.', 'price': 900.00, 'stock_quantity': 37, 'image_url': 'https://picsum.photos/id/19/200/300'},
                {'name': 'VAIO FE14', 'description': 'Classic design laptop for office productivity.', 'price': 850.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/20/200/300'},
                {'name': 'System76 Lemur Pro', 'description': 'Linux-first laptop with open-source firmware.', 'price': 1500.00, 'stock_quantity': 22, 'image_url': 'https://picsum.photos/id/21/200/300'},
                {'name': 'Framework Laptop 13', 'description': 'Modular and upgradable laptop for DIY enthusiasts.', 'price': 1000.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/22/200/300'},
                {'name': 'Razer Blade 16', 'description': 'High-refresh rate gaming laptop with powerful specs.', 'price': 2200.00, 'stock_quantity': 12, 'image_url': 'https://picsum.photos/id/23/200/300'},
                {'name': 'Lenovo Yoga 7i', 'description': 'Flexible 2-in-1 laptop with strong performance.', 'price': 899.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/24/200/300'},
                {'name': 'ASUS ZenBook 14 OLED', 'description': 'Compact ultrabook with a stunning OLED display.', 'price': 1100.00, 'stock_quantity': 27, 'image_url': 'https://picsum.photos/id/25/200/300'},
                {'name': 'HP Pavilion 15', 'description': 'All-rounder laptop for daily computing needs.', 'price': 720.00, 'stock_quantity': 58, 'image_url': 'https://picsum.photos/id/26/200/300'},
                {'name': 'Microsoft Surface Laptop Go 3', 'description': 'Entry-level Surface laptop, very portable.', 'price': 799.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/27/200/300'},
                {'name': 'Dell G15 Gaming Laptop', 'description': 'Budget-friendly gaming laptop with NVIDIA GPU.', 'price': 950.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/28/200/300'},
                {'name': 'MacBook Pro 14" M3', 'description': 'Professional laptop with exceptional performance and battery life.', 'price': 1999.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/29/200/300'},
                {'name': 'Huawei MateBook X Pro', 'description': 'Ultra-slim laptop with stunning display and powerful processor.', 'price': 1450.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/30/200/300'},
            ],
            'Groceries': [
                {'name': 'Ladyfinger (Okra) - 500g', 'description': 'Fresh green vegetable, ideal for curries.', 'price': 2.50, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/100/200/300'},
                {'name': 'Organic Tomatoes - 1kg', 'description': 'Farm-fresh, ripe red tomatoes.', 'price': 3.75, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/101/200/300'},
                {'name': 'Green Bell Pepper (Capsicum) - 250g', 'description': 'Crisp and fresh, good for stir-fries.', 'price': 1.80, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/102/200/300'},
                {'name': 'Potato (Aloo) - 1kg', 'description': 'Staple vegetable, versatile for many dishes.', 'price': 1.20, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/103/200/300'},
                {'name': 'Onions - 1kg', 'description': 'Fresh, pungent onions for everyday cooking.', 'price': 1.10, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/104/200/300'},
                {'name': 'Basmati Rice - 5kg', 'description': 'Premium long-grain Basmati Rice for fragrant biryanis.', 'price': 15.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/105/200/300'},
                {'name': 'Whole Wheat Flour (Atta) - 1kg', 'description': 'Finely ground whole wheat flour for chapatis.', 'price': 3.00, 'stock_quantity': 160, 'image_url': 'https://picsum.photos/id/106/200/300'},
                {'name': 'Toor Dal - 1kg', 'description': 'Split pigeon peas, essential for Indian daal.', 'price': 2.80, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/107/200/300'},
                {'name': 'Mustard Oil - 1L', 'description': 'Pure mustard oil for cooking and pickling.', 'price': 4.50, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/108/200/300'},
                {'name': 'Amul Milk - 1L', 'description': 'Pasteurized homogenized toned milk.', 'price': 1.00, 'stock_quantity': 250, 'image_url': 'https://picsum.photos/id/109/200/300'},
                {'name': 'Fresh Paneer - 200g', 'description': 'Soft Indian cottage cheese.', 'price': 3.20, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/110/200/300'},
                {'name': 'Cumin Powder - 100g', 'description': 'Ground cumin for Indian spices.', 'price': 1.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/111/200/300'},
                {'name': 'Turmeric Powder - 100g', 'description': 'High-quality turmeric powder.', 'price': 0.90, 'stock_quantity': 125, 'image_url': 'https://picsum.photos/id/112/200/300'},
                {'name': 'Salt - 1kg', 'description': 'Iodized salt.', 'price': 0.50, 'stock_quantity': 300, 'image_url': 'https://picsum.photos/id/113/200/300'},
                {'name': 'Sugar - 1kg', 'description': 'Refined white sugar.', 'price': 1.20, 'stock_quantity': 280, 'image_url': 'https://picsum.photos/id/114/200/300'},
                {'name': 'Tea Leaves - 250g', 'description': 'Premium black tea leaves.', 'price': 3.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/115/200/300'},
                {'name': 'Coffee Powder - 100g', 'description': 'Instant coffee powder for a quick brew.', 'price': 2.50, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/116/200/300'},
                {'name': 'Eggs - Tray of 12', 'description': 'Fresh farm eggs.', 'price': 2.20, 'stock_quantity': 160, 'image_url': 'https://picsum.photos/id/117/200/300'},
                {'name': 'Bread - White Sliced', 'description': 'Soft white bread slices.', 'price': 1.50, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/118/200/300'},
                {'name': 'Butter - 100g', 'description': 'Creamy dairy butter.', 'price': 1.80, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/119/200/300'},
                {'name': 'Curd (Dahi) - 500g', 'description': 'Fresh plain yogurt.', 'price': 1.75, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/120/200/300'},
                {'name': 'Green Chillies - 100g', 'description': 'Spicy green chillies.', 'price': 0.70, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/121/200/300'},
                {'name': 'Garlic - 250g', 'description': 'Fresh garlic bulbs.', 'price': 1.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/122/200/300'},
                {'name': 'Ginger - 250g', 'description': 'Fresh ginger root.', 'price': 1.10, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/123/200/300'},
                {'name': 'Coriander Leaves - 100g', 'description': 'Fresh cilantro.', 'price': 0.60, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/124/200/300'},
                {'name': 'Cauliflower - 1 pc', 'description': 'Fresh whole cauliflower.', 'price': 2.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/125/200/300'},
                {'name': 'Cabbage - 1 pc', 'description': 'Fresh whole cabbage.', 'price': 1.50, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/126/200/300'},
                {'name': 'Spinach - 500g', 'description': 'Fresh spinach leaves.', 'price': 1.30, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/127/200/300'},
                {'name': 'Capsicum (Red) - 250g', 'description': 'Sweet and vibrant red bell pepper.', 'price': 2.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/128/200/300'},
                {'name': 'Carrots - 500g', 'description': 'Fresh and crunchy carrots.', 'price': 1.60, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/129/200/300'},
            ],
            'Smartphones': [
                {'name': 'Samsung Galaxy S24 Ultra', 'description': 'Latest Android flagship with S Pen and AI features.', 'price': 1199.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/200/200/300'},
                {'name': 'iPhone 15 Pro Max', 'description': 'Apple\'s top-tier smartphone with A17 Bionic chip.', 'price': 1299.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/201/200/300'},
                {'name': 'OnePlus 12', 'description': 'Fast and smooth Android experience with Hasselblad camera.', 'price': 799.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/202/200/300'},
                {'name': 'Google Pixel 8 Pro', 'description': 'Pure Android experience with excellent AI photography.', 'price': 999.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/203/200/300'},
                {'name': 'Xiaomi 14 Ultra', 'description': 'Powerful Android phone with Leica camera system.', 'price': 1099.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/204/200/300'},
                {'name': 'Samsung Galaxy A55', 'description': 'Mid-range Android phone with excellent display and battery.', 'price': 450.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/205/200/300'},
                {'name': 'iPhone SE (3rd Gen)', 'description': 'Affordable iPhone with powerful A15 Bionic chip.', 'price': 429.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/206/200/300'},
                {'name': 'Nothing Phone (2)', 'description': 'Unique design Android phone with Glyph Interface.', 'price': 600.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/207/200/300'},
                {'name': 'Redmi Note 13 Pro Max', 'description': 'Feature-packed mid-range smartphone.', 'price': 350.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/208/200/300'},
                {'name': 'Motorola Edge 50 Pro', 'description': 'Stylish and capable Android phone with good camera.', 'price': 550.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/209/200/300'},
                {'name': 'Realme 12 Pro+', 'description': 'Mid-range phone with periscope zoom camera.', 'price': 400.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/210/200/300'},
                {'name': 'Oppo Reno 11 Pro', 'description': 'Sleek design and good camera for portraits.', 'price': 500.00, 'stock_quantity': 68, 'image_url': 'https://picsum.photos/id/211/200/300'},
                {'name': 'Vivo X100 Pro', 'description': 'Photography-focused flagship with Zeiss optics.', 'price': 950.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/212/200/300'},
                {'name': 'Sony Xperia 1 V', 'description': 'Creator-focused smartphone with 4K OLED display.', 'price': 1050.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/213/200/300'},
                {'name': 'Asus ROG Phone 8 Pro', 'description': 'Ultimate gaming smartphone with powerful cooling.', 'price': 1100.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/214/200/300'},
                {'name': 'POCO X6 Pro', 'description': 'Performance-oriented mid-range phone.', 'price': 380.00, 'stock_quantity': 72, 'image_url': 'https://picsum.photos/id/215/200/300'},
                {'name': 'Honor Magic6 Pro', 'description': 'Premium flagship with robust display and camera.', 'price': 980.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/216/200/300'},
                {'name': 'Infinix Note 40 Pro', 'description': 'Budget-friendly phone with large display and battery.', 'price': 220.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/217/200/300'},
                {'name': 'Lava Agni 2 5G', 'description': 'Indian-made smartphone with good value.', 'price': 250.00, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/218/200/300'},
                {'name': 'Micromax In 2b', 'description': 'Affordable entry-level smartphone.', 'price': 150.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/219/200/300'},
                {'name': 'Nokia G400 5G', 'description': 'Durable Nokia phone with 5G connectivity.', 'price': 280.00, 'stock_quantity': 78, 'image_url': 'https://picsum.photos/id/220/200/300'},
                {'name': 'Tecno Pova 5 Pro', 'description': 'Gaming-centric phone with fast charging.', 'price': 240.00, 'stock_quantity': 82, 'image_url': 'https://picsum.photos/id/221/200/300'},
                {'name': 'iQOO Neo 9 Pro', 'description': 'High-performance phone for gaming.', 'price': 650.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/222/200/300'},
                {'name': 'Motorola Moto G Stylus 5G', 'description': 'Mid-range phone with stylus support.', 'price': 300.00, 'stock_quantity': 62, 'image_url': 'https://picsum.photos/id/223/200/300'},
                {'name': 'Samsung Galaxy Z Fold5', 'description': 'Latest foldable phone for ultimate multitasking.', 'price': 1799.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/id/224/200/300'},
                {'name': 'Samsung Galaxy Z Flip5', 'description': 'Compact foldable phone with large cover screen.', 'price': 999.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/225/200/300'},
                {'name': 'Realme GT 5 Pro', 'description': 'Flagship killer with strong performance.', 'price': 580.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/226/200/300'},
                {'name': 'Vivo V30 Pro', 'description': 'Slim phone with excellent portrait photography.', 'price': 480.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/227/200/300'},
                {'name': 'Tecno Phantom V Fold', 'description': 'Affordable foldable smartphone.', 'price': 900.00, 'stock_quantity': 10, 'image_url': 'https://picsum.photos/id/228/200/300'},
                {'name': 'Oppo Find X7 Ultra', 'description': 'Top-tier camera phone with advanced imaging.', 'price': 1150.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/229/200/300'},
            ],
            'Televisions': [
                {'name': 'Samsung 65" Neo QLED 4K TV', 'description': 'Stunning 4K resolution with Quantum Mini LEDs and object tracking sound.', 'price': 1800.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/300/200/300'},
                {'name': 'Sony Bravia 55" OLED TV', 'description': 'Exceptional contrast and vibrant colors with XR Processor.', 'price': 1500.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/301/200/300'},
                {'name': 'LG C3 77" OLED TV', 'description': 'Large screen OLED for immersive home theater with G-Sync support.', 'price': 2500.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/id/302/200/300'},
                {'name': 'TCL 50" QLED 4K Smart TV', 'description': 'Affordable QLED TV with Google TV built-in.', 'price': 450.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/303/200/300'},
                {'name': 'Hisense U8 Series 65" Mini-LED ULED 4K UHD Google Smart TV', 'description': 'Premium picture quality with Mini-LED backlight.', 'price': 900.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/304/200/300'},
                {'name': 'Xiaomi Smart TV X Pro 43"', 'description': 'Value-for-money smart TV with vivid display.', 'price': 300.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/305/200/300'},
                {'name': 'OnePlus TV Y1S Edge 43"', 'description': 'Slim design with Gamma Engine and Android TV.', 'price': 320.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/306/200/300'},
                {'name': 'Sony Bravia XR A95L 65" QD-OLED TV', 'description': 'Top-tier QD-OLED with unparalleled brightness and color.', 'price': 3500.00, 'stock_quantity': 10, 'image_url': 'https://picsum.photos/id/307/200/300'},
                {'name': 'LG G3 65" OLED Evo TV', 'description': 'Gallery design OLED for flush wall mounting.', 'price': 2200.00, 'stock_quantity': 18, 'image_url': 'https://picsum.photos/id/308/200/300'},
                {'name': 'Samsung The Frame 55" QLED 4K Smart TV', 'description': 'Art Mode TV that blends into your decor.', 'price': 1200.00, 'stock_quantity': 22, 'image_url': 'https://picsum.photos/id/309/200/300'},
                {'name': 'Vu 55" GloLED 4K Smart TV', 'description': 'Feature-rich TV with high brightness and powerful sound.', 'price': 500.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/310/200/300'},
                {'name': 'Acer 50" H Series 4K UHD Smart TV', 'description': 'Budget-friendly 4K TV with crisp visuals.', 'price': 380.00, 'stock_quantity': 42, 'image_url': 'https://picsum.photos/id/311/200/300'},
                {'name': 'Philips 65" OLED 807 Series 4K UHD Android TV', 'description': 'Ambilight TV for immersive viewing experience.', 'price': 1700.00, 'stock_quantity': 17, 'image_url': 'https://picsum.photos/id/312/200/300'},
                {'name': 'Panasonic 40" Full HD Smart TV', 'description': 'Reliable Full HD smart TV for smaller spaces.', 'price': 280.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/313/200/300'},
                {'name': 'Toshiba 55" C350 Series LED 4K UHD Smart Fire TV', 'description': 'Integrated Fire TV experience with voice control.', 'price': 420.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/314/200/300'},
                {'name': 'Redmi Smart TV X50', 'description': 'Value-oriented 4K Smart TV from Xiaomi.', 'price': 360.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/315/200/300'},
                {'name': 'Samsung Crystal 4K 55" UHD Smart TV', 'description': 'Affordable 4K TV with vibrant colors.', 'price': 480.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/316/200/300'},
                {'name': 'LG UQ75 50" 4K UHD Smart TV', 'description': 'Entry-level 4K TV from LG with WebOS.', 'price': 400.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/317/200/300'},
                {'name': 'Mi TV 4A Horizon Edition 32"', 'description': 'Compact HD Smart TV for bedrooms.', 'price': 180.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/318/200/300'},
                {'name': 'Infinix X3 43" 4K UHD Smart TV', 'description': 'Android TV with good connectivity.', 'price': 340.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/319/200/300'},
                {'name': 'Kodak 50" CA Pro Series 4K UHD Smart Android TV', 'description': 'Feature-rich Android TV from Kodak.', 'price': 390.00, 'stock_quantity': 37, 'image_url': 'https://picsum.photos/id/320/200/300'},
                {'name': 'Croma 55" Fire TV Edition 4K UHD Smart TV', 'description': 'Croma branded Fire TV for easy streaming.', 'price': 470.00, 'stock_quantity': 33, 'image_url': 'https://picsum.photos/id/321/200/300'},
                {'name': 'Onida 32" HD Ready Smart Android TV', 'description': 'Basic Android TV for small spaces.', 'price': 190.00, 'stock_quantity': 52, 'image_url': 'https://picsum.photos/id/322/200/300'},
                {'name': 'Micromax 40" Full HD Smart LED TV', 'description': 'Budget-friendly Full HD TV.', 'price': 250.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/323/200/300'},
                {'name': 'Akai 43" Full HD Smart LED TV', 'description': 'Affordable smart TV with good picture quality.', 'price': 270.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/324/200/300'},
                {'name': 'BPL 32" HD Ready LED TV', 'description': 'Simple and reliable LED TV.', 'price': 150.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/325/200/300'},
                {'name': 'Thomson 50" 9R Series 4K UHD Smart Android TV', 'description': 'Android TV with HDR10+ support.', 'price': 410.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/326/200/300'},
                {'name': 'Haier 58" 4K UHD Smart LED TV', 'description': 'Large screen 4K TV with smart features.', 'price': 550.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/327/200/300'},
                {'name': 'Sansui 43" FHD Smart Android TV', 'description': 'Android TV with Google Assistant built-in.', 'price': 290.00, 'stock_quantity': 42, 'image_url': 'https://picsum.photos/id/328/200/300'},
                {'name': 'Daiwa 65" 4K UHD Smart TV', 'description': 'Affordable large screen smart TV.', 'price': 600.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/329/200/300'},
            ],
            'Books': [
                {'name': 'The Alchemist', 'description': 'A philosophical novel by Paulo Coelho about following dreams.', 'price': 12.50, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/400/200/300'},
                {'name': 'Atomic Habits', 'description': 'An easy & proven way to build good habits & break bad ones by James Clear.', 'price': 15.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/401/200/300'},
                {'name': 'Sapiens: A Brief History of Humankind', 'description': 'A global bestseller exploring human history by Yuval Noah Harari.', 'price': 18.75, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/402/200/300'},
                {'name': 'The Psychology of Money', 'description': 'Timeless lessons on wealth, greed, and happiness by Morgan Housel.', 'price': 14.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/403/200/300'},
                {'name': 'Rich Dad Poor Dad', 'description': 'What the Rich Teach Their Kids About Money--That the Poor and Middle Class Do Not!', 'price': 10.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/404/200/300'},
                {'name': 'The Silent Patient', 'description': 'A shocking psychological thriller by Alex Michaelides.', 'price': 13.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/405/200/300'},
                {'name': 'Ikigai: The Japanese Secret to a Long and Happy Life', 'description': 'Inspiring book on finding your purpose.', 'price': 9.50, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/406/200/300'},
                {'name': 'The Power of Habit', 'description': 'Why we do what we do in life and business by Charles Duhigg.', 'price': 16.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/407/200/300'},
                {'name': 'Think and Grow Rich', 'description': 'Classic self-help book by Napoleon Hill on personal achievement.', 'price': 8.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/408/200/300'},
                {'name': 'Life\'s Amazing Secrets', 'description': 'How to find balance and purpose in your life by Gaur Gopal Das.', 'price': 7.00, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/409/200/300'},
                {'name': 'The Monk Who Sold His Ferrari', 'description': 'A fable about fulfilling your dreams and reaching your destiny.', 'price': 11.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/410/200/300'},
                {'name': 'Harry Potter and the Sorcerer\'s Stone', 'description': 'The first book in the magical series by J.K. Rowling.', 'price': 9.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/411/200/300'},
                {'name': 'To Kill a Mockingbird', 'description': 'A classic novel by Harper Lee on justice and prejudice.', 'price': 10.50, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/412/200/300'},
                {'name': 'Pride and Prejudice', 'description': 'A romantic novel of manners by Jane Austen.', 'price': 8.50, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/413/200/300'},
                {'name': 'The Great Gatsby', 'description': 'A novel by F. Scott Fitzgerald illustrating the Roaring Twenties.', 'price': 9.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/414/200/300'},
                {'name': '1984', 'description': 'Dystopian social science fiction novel by George Orwell.', 'price': 9.75, 'stock_quantity': 88, 'image_url': 'https://picsum.photos/id/415/200/300'},
                {'name': 'Becoming', 'description': 'Memoir by former First Lady of the United States Michelle Obama.', 'price': 20.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/416/200/300'},
                {'name': 'Educated', 'description': 'A memoir by Tara Westover.', 'price': 16.50, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/417/200/300'},
                {'name': 'The Book Thief', 'description': 'A historical novel by Markus Zusak set during World War II.', 'price': 13.50, 'stock_quantity': 78, 'image_url': 'https://picsum.photos/id/418/200/300'},
                {'name': 'Sita: Warrior of Mithila (Ram Chandra Series #2)', 'description': 'Mythological fiction by Amish Tripathi.', 'price': 10.00, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/419/200/300'},
                {'name': 'The Immortals of Meluha (Shiva Trilogy #1)', 'description': 'Modern Indian mythological fantasy by Amish Tripathi.', 'price': 9.00, 'stock_quantity': 105, 'image_url': 'https://picsum.photos/id/420/200/300'},
                {'name': 'The Mahabharata', 'description': 'An epic narrative of the Kurukshetra War.', 'price': 25.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/421/200/300'},
                {'name': 'The Secret', 'description': 'Self-help book by Rhonda Byrne on the law of attraction.', 'price': 11.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/422/200/300'},
                {'name': 'Your Brain is a Superpower', 'description': 'Unlock Your True Potential by Dr. Ashwin Mohan.', 'price': 14.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/423/200/300'},
                {'name': 'The Lean Startup', 'description': 'How Today\'s Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses.', 'price': 17.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/424/200/300'},
                {'name': 'Zero to One', 'description': 'Notes on Startups, or How to Build the Future by Peter Thiel.', 'price': 15.50, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/425/200/300'},
                {'name': 'Sapiens: A Graphic History, Vol. 1', 'description': 'The first volume of the graphic adaptation of Sapiens.', 'price': 22.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/426/200/300'},
                {'name': 'The Midnight Library', 'description': 'A novel by Matt Haig about alternate realities.', 'price': 14.50, 'stock_quantity': 72, 'image_url': 'https://picsum.photos/id/427/200/300'},
                {'name': 'Sita\'s Warrior', 'description': 'An inspiring tale from Indian mythology.', 'price': 8.00, 'stock_quantity': 98, 'image_url': 'https://picsum.photos/id/428/200/300'},
                {'name': 'Wings of Fire', 'description': 'An autobiography of A. P. J. Abdul Kalam.', 'price': 12.00, 'stock_quantity': 87, 'image_url': 'https://picsum.photos/id/429/200/300'},
            ],
            'Fashion': [
                {'name': 'Men\'s Slim Fit Jeans', 'description': 'Classic blue denim jeans, comfortable and stylish.', 'price': 45.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/500/200/300'},
                {'name': 'Women\'s Floral Maxi Dress', 'description': 'Elegant and flowy dress for summer, breathable fabric.', 'price': 60.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/501/200/300'},
                {'name': 'Unisex Running Shoes', 'description': 'Lightweight and breathable athletic shoes for performance.', 'price': 80.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/502/200/300'},
                {'name': 'Leather Wallet - Men\'s', 'description': 'Genuine leather wallet with multiple card slots.', 'price': 25.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/503/200/300'},
                {'name': 'Women\'s Handbag - Tote', 'description': 'Spacious tote bag, perfect for daily use.', 'price': 35.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/504/200/300'},
                {'name': 'Sporty Smartwatch', 'description': 'Fitness tracker and smartwatch with heart rate monitor.', 'price': 120.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/505/200/300'},
                {'name': 'Classic Aviator Sunglasses', 'description': 'UV protected sunglasses with timeless design.', 'price': 30.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/506/200/300'},
                {'name': 'Men\'s Polo T-Shirt', 'description': 'Comfortable cotton polo shirt, various colors.', 'price': 20.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/507/200/300'},
                {'name': 'Women\'s High-Waisted Leggings', 'description': 'Stretchy and comfortable leggings for yoga or casual wear.', 'price': 18.00, 'stock_quantity': 160, 'image_url': 'https://picsum.photos/id/508/200/300'},
                {'name': 'Kids\' Cartoon Backpack', 'description': 'Fun backpack for school, with favorite cartoon characters.', 'price': 22.00, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/509/200/300'},
                {'name': 'Denim Jacket - Unisex', 'description': 'Classic denim jacket, suitable for all seasons.', 'price': 55.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/510/200/300'},
                {'name': 'Analog Wrist Watch - Leather Strap', 'description': 'Elegant watch with leather strap and classic dial.', 'price': 40.00, 'stock_quantity': 105, 'image_url': 'https://picsum.photos/id/511/200/300'},
                {'name': 'Winter Woolen Scarf', 'description': 'Warm and soft woolen scarf for cold weather.', 'price': 15.00, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/512/200/300'},
                {'name': 'Sneakers - White Casual', 'description': 'Versatile white sneakers for a trendy look.', 'price': 50.00, 'stock_quantity': 115, 'image_url': 'https://picsum.photos/id/513/200/300'},
                {'name': 'Formal Shirt - Men\'s Striped', 'description': 'Tailored fit formal shirt for office or events.', 'price': 38.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/514/200/300'},
                {'name': 'Ethnic Kurta Set - Women\'s', 'description': 'Traditional Indian kurta set with intricate embroidery.', 'price': 70.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/515/200/300'},
                {'name': 'Baseball Cap - Adjustable', 'description': 'Sporty cap for sun protection, adjustable size.', 'price': 10.00, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/516/200/300'},
                {'name': 'Smart Casual Blazer - Men\'s', 'description': 'Stylish blazer for semi-formal occasions.', 'price': 90.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/517/200/300'},
                {'name': 'Party Wear Heels - Women\'s', 'description': 'Sparkling high heels for special occasions.', 'price': 45.00, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/518/200/300'},
                {'name': 'Kids\' Winter Jacket', 'description': 'Warm padded jacket for children, various sizes.', 'price': 30.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/519/200/300'},
                {'name': 'Sports Socks - Pack of 3', 'description': 'Comfortable and absorbent socks for athletic use.', 'price': 8.00, 'stock_quantity': 250, 'image_url': 'https://picsum.photos/id/520/200/300'},
                {'name': 'Swim Trunks - Men\'s', 'description': 'Quick-dry swim trunks for beach or pool.', 'price': 20.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/521/200/300'},
                {'name': 'Yoga Mat & Carry Bag', 'description': 'Non-slip yoga mat with convenient carry bag.', 'price': 25.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/522/200/300'},
                {'name': 'Silver Pendant Necklace', 'description': 'Elegant silver pendant with delicate chain.', 'price': 30.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/523/200/300'},
                {'name': 'Backpack - Laptop Compartment', 'description': 'Durable backpack with padded laptop sleeve.', 'price': 40.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/524/200/300'},
                {'name': 'Designer Dress - Evening Gown', 'description': 'Exquisite evening gown for formal events.', 'price': 150.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/525/200/300'},
                {'name': 'Men\'s Leather Belt', 'description': 'Classic leather belt with a metal buckle.', 'price': 20.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/526/200/300'},
                {'name': 'Kid\'s Running Shoes', 'description': 'Comfortable and durable running shoes for active kids.', 'price': 35.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/527/200/300'},
                {'name': 'Cotton Scarf - Women\'s', 'description': 'Lightweight cotton scarf with vibrant patterns.', 'price': 12.00, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/528/200/300'},
                {'name': 'Formal Leather Shoes - Men\'s', 'description': 'Premium leather dress shoes for formal wear.', 'price': 75.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/529/200/300'},
            ],
            'Home Appliances': [
                {'name': 'Samsung 25L Convection Microwave', 'description': 'Multi-functional microwave oven for baking, grilling, and reheating.', 'price': 150.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/600/200/300'},
                {'name': 'LG 7.0 kg Fully Automatic Washing Machine', 'description': 'Front-load washing machine with smart inverter technology.', 'price': 300.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/601/200/300'},
                {'name': 'Prestige 3 Burner Gas Stove', 'description': 'High-quality gas stove with durable brass burners.', 'price': 80.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/602/200/300'},
                {'name': 'Philips Air Fryer XL', 'description': 'Healthy frying with Rapid Air Technology, 1.2 kg capacity.', 'price': 120.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/603/200/300'},
                {'name': 'Kent RO Water Purifier', 'description': 'RO+UF+TDS control for pure and healthy drinking water.', 'price': 180.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/604/200/300'},
                {'name': 'Dyson V11 Absolute Pro Vacuum Cleaner', 'description': 'Cord-free powerful vacuum cleaner for deep cleaning.', 'price': 450.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/605/200/300'},
                {'name': 'Bajaj Mixer Grinder 750W', 'description': 'Powerful mixer grinder for daily kitchen needs.', 'price': 60.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/606/200/300'},
                {'name': 'Havells Immersion Water Heater', 'description': 'Fast water heating immersion rod for quick use.', 'price': 20.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/607/200/300'},
                {'name': 'Orient Electric Stand Fan', 'description': 'High-speed oscillating stand fan for powerful air delivery.', 'price': 40.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/608/200/300'},
                {'name': 'Blue Star 1 Ton 3 Star Split AC', 'description': 'Energy-efficient air conditioner for cooling medium rooms.', 'price': 400.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/609/200/300'},
                {'name': 'Whirlpool 245L Double Door Refrigerator', 'description': 'Frost-free refrigerator with spacious storage and multi-air flow.', 'price': 350.00, 'stock_quantity': 33, 'image_url': 'https://picsum.photos/id/610/200/300'},
                {'name': 'Bosch Dishwasher 13 Place Settings', 'description': 'Efficient dishwasher with intensive Kadhai wash.', 'price': 500.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/611/200/300'},
                {'name': 'Morphy Richards Pop-up Toaster', 'description': '2-slice pop-up toaster with variable browning control.', 'price': 30.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/612/200/300'},
                {'name': 'Pigeon Induction Cooktop', 'description': 'Portable induction cooktop with multiple cooking functions.', 'price': 55.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/613/200/300'},
                {'name': 'Eureka Forbes Aquasure Water Purifier', 'description': 'UV water purifier for safe drinking water.', 'price': 120.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/614/200/300'},
                {'name': 'LG 8 kg Semi-Automatic Washing Machine', 'description': 'Top-load semi-automatic washing machine with roller jet pulsator.', 'price': 200.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/615/200/300'},
                {'name': 'Butterfly Wet Grinder 2L', 'description': 'Table top wet grinder for idli/dosa batter.', 'price': 90.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/616/200/300'},
                {'name': 'Usha Ceiling Fan', 'description': 'Energy-efficient ceiling fan with wide air throw.', 'price': 35.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/617/200/300'},
                {'name': 'Crompton Desert Air Cooler 75L', 'description': 'Large capacity desert cooler for effective cooling in dry climates.', 'price': 110.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/618/200/300'},
                {'name': 'Haier 280L Bottom Mounted Refrigerator', 'description': 'Refrigerator with freezer at bottom for convenience.', 'price': 380.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/619/200/300'},
                {'name': 'Glen Built-in Hob 4 Burner', 'description': 'Sleek built-in hob for modern kitchens.', 'price': 250.00, 'stock_quantity': 32, 'image_url': 'https://picsum.photos/id/620/200/300'},
                {'name': 'Lifelong Hand Blender', 'description': 'Ergonomic hand blender for quick blending tasks.', 'price': 25.00, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/621/200/300'},
                {'name': 'Kaff Chimney 90cm', 'description': 'Powerful kitchen chimney for smoke extraction.', 'price': 180.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/622/200/300'},
                {'name': 'Symphony Air Cooler 27L', 'description': 'Personal air cooler for small spaces.', 'price': 70.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/623/200/300'},
                {'name': 'Godrej 236L Single Door Refrigerator', 'description': 'Direct cool refrigerator with large vegetable tray.', 'price': 280.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/624/200/300'},
                {'name': 'Panasonic Rice Cooker 1.8L', 'description': 'Automatic rice cooker for perfectly cooked rice.', 'price': 45.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/625/200/300'},
                {'name': 'Sunflame Gas Hob 3 Burner', 'description': 'Compact and stylish gas hob for modern kitchens.', 'price': 100.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/626/200/300'},
                {'name': 'IFB Dishwasher 12 Place Settings', 'description': 'Efficient dishwasher with multiple wash programs.', 'price': 480.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/627/200/300'},
                {'name': 'Kent Smart RO Water Purifier', 'description': 'Advanced RO purifier with digital display and auto-flush.', 'price': 220.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/628/200/300'},
                {'name': 'Voltas 1.5 Ton 5 Star Inverter AC', 'description': 'Highly energy-efficient inverter AC for large rooms.', 'price': 550.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/629/200/300'},
            ],
            'Sports & Outdoors': [
                {'name': 'Cosco Football - Size 5', 'description': 'Durable football for practice and matches.', 'price': 20.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/700/200/300'},
                {'name': 'Yonex Badminton Racket', 'description': 'Lightweight and powerful racket for badminton players.', 'price': 35.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/701/200/300'},
                {'name': 'Kore PVC 20-50 kg Home Gym Set', 'description': 'Complete home gym set with dumbbells, barbell, and plates.', 'price': 70.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/702/200/300'},
                {'name': 'Decathlon Quechua 2-Person Camping Tent', 'description': 'Easy to set up and compact camping tent for two.', 'price': 60.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/703/200/300'},
                {'name': 'Strauss Yoga Mat - 6mm', 'description': 'Non-slip yoga mat for comfortable practice.', 'price': 15.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/704/200/300'},
                {'name': 'Nivia Basketball - Size 7', 'description': 'Official size basketball for indoor and outdoor play.', 'price': 28.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/705/200/300'},
                {'name': 'Puma Running Shoes - Unisex', 'description': 'Lightweight running shoes for everyday jogging.', 'price': 65.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/706/200/300'},
                {'name': 'Vector X Skipping Rope', 'description': 'Adjustable skipping rope with comfortable handles.', 'price': 8.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/707/200/300'},
                {'name': 'Reebok Dumbbell Set - 5kg Pair', 'description': 'Vinyl coated dumbbells for home workouts.', 'price': 40.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/708/200/300'},
                {'name': 'Wildcraft Rucksack - 45L', 'description': 'Spacious and durable rucksack for trekking and travel.', 'price': 50.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/709/200/300'},
                {'name': 'Bicycle - Mountain Bike 26 inch', 'description': 'Sturdy mountain bike for trails and daily commute.', 'price': 180.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/710/200/300'},
                {'name': 'Cricket Bat - Kashmir Willow', 'description': 'Full size cricket bat for casual and club play.', 'price': 45.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/711/200/300'},
                {'name': 'SS Cricket Helmet', 'description': 'Protective cricket helmet for batsmen.', 'price': 30.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/712/200/300'},
                {'name': 'Adidas Football Shin Guards', 'description': 'Lightweight shin guards for soccer protection.', 'price': 18.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/713/200/300'},
                {'name': 'Speedo Swimming Goggles', 'description': 'Anti-fog and UV protection swimming goggles.', 'price': 12.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/714/200/300'},
                {'name': 'Yonex Shuttlecocks - Pack of 6', 'description': 'Durable nylon shuttlecocks for badminton.', 'price': 10.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/715/200/300'},
                {'name': 'Resistance Bands Set', 'description': 'Set of 5 resistance bands for various workouts.', 'price': 25.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/716/200/300'},
                {'name': 'Trek Poles - Adjustable Pair', 'description': 'Lightweight and collapsible poles for hiking.', 'price': 30.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/717/200/300'},
                {'name': 'Camping Sleeping Bag', 'description': 'Comfortable and warm sleeping bag for camping.', 'price': 40.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/718/200/300'},
                {'name': 'Hiking Boots - Men\'s Waterproof', 'description': 'Durable and waterproof boots for trekking.', 'price': 90.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/719/200/300'},
                {'name': 'Tennis Racket - Head Graphene', 'description': 'Advanced tennis racket for powerful shots.', 'price': 85.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/720/200/300'},
                {'name': 'Table Tennis Racket - Stiga', 'description': 'Professional table tennis racket for spin and speed.', 'price': 25.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/721/200/300'},
                {'name': 'Boxing Gloves - 10oz', 'description': 'Training boxing gloves for sparring and bag work.', 'price': 35.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/722/200/300'},
                {'name': 'Skateboard - Beginner Deck', 'description': 'Complete skateboard for beginner riders.', 'price': 50.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/723/200/300'},
                {'name': 'Roller Skates - Adjustable', 'description': 'Quad roller skates with adjustable sizing.', 'price': 45.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/724/200/300'},
                {'name': 'Ab Roller Wheel', 'description': 'Compact ab roller for core strength training.', 'price': 15.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/725/200/300'},
                {'name': 'Pull Up Bar - Doorway', 'description': 'Easy to install doorway pull up bar for home gym.', 'price': 22.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/726/200/300'},
                {'name': 'Fitness Tracker Watch', 'description': 'Monitors heart rate, steps, and sleep.', 'price': 55.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/727/200/300'},
                {'name': 'Diving Mask and Snorkel Set', 'description': 'Panoramic view mask with dry snorkel for underwater exploration.', 'price': 30.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/728/200/300'},
                {'name': 'Portable Picnic Blanket', 'description': 'Waterproof and foldable blanket for outdoor picnics.', 'price': 20.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/729/200/300'},
            ],
            'Beauty & Personal Care': [
                {'name': 'Mamaearth Onion Hair Oil - 250ml', 'description': 'Reduces hair fall and promotes hair growth.', 'price': 10.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/800/200/300'},
                {'name': 'Himalaya Purifying Neem Face Wash - 150ml', 'description': 'Soap-free herbal formulation for clear skin.', 'price': 5.00, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/801/200/300'},
                {'name': 'Lakme Absolute Skin Gloss Gel Creme - 50g', 'description': 'Lightweight gel cream for a glossy finish.', 'price': 12.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/802/200/300'},
                {'name': 'Nivea Soft Light Moisturiser - 300ml', 'description': 'Quick absorbing cream for face, hand and body.', 'price': 8.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/803/200/300'},
                {'name': 'Ponds Super Light Gel Oil Free Moisturiser - 147g', 'description': 'Non-sticky, hydrating gel for all skin types.', 'price': 7.00, 'stock_quantity': 160, 'image_url': 'https://picsum.photos/id/804/200/300'},
                {'name': 'Garnier Micellar Cleansing Water - 400ml', 'description': 'Removes makeup, cleanses and soothes skin.', 'price': 9.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/805/200/300'},
                {'name': 'L\'Oreal Paris Total Repair 5 Shampoo - 340ml', 'description': 'Fights 5 signs of hair damage: dryness, roughness, dullness, breakage, split ends.', 'price': 6.00, 'stock_quantity': 170, 'image_url': 'https://picsum.photos/id/806/200/300'},
                {'name': 'Dove Beauty Bar - 100g (Pack of 3)', 'description': 'Gentle cleansing bar with 1/4 moisturizing cream.', 'price': 4.00, 'stock_quantity': 250, 'image_url': 'https://picsum.photos/id/807/200/300'},
                {'name': 'Colgate MaxFresh Toothpaste - 150g', 'description': 'Invigorating freshness with menthol.', 'price': 3.00, 'stock_quantity': 300, 'image_url': 'https://picsum.photos/id/808/200/300'},
                {'name': 'Dettol Original Germ Protection Handwash - 200ml', 'description': 'Protects from 100 illness causing germs.', 'price': 4.50, 'stock_quantity': 220, 'image_url': 'https://picsum.photos/id/809/200/300'},
                {'name': 'Vega Hair Dryer - 1200W', 'description': 'Compact and powerful hair dryer for quick styling.', 'price': 20.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/810/200/300'},
                {'name': 'Philips Multi-Grooming Kit - 9-in-1', 'description': 'All-in-one trimmer for face, hair and body.', 'price': 35.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/811/200/300'},
                {'name': 'Forest Essentials Soundarya Radiance Cream', 'description': 'Authentic Ayurvedic anti-aging cream.', 'price': 70.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/812/200/300'},
                {'name': 'Minimalist 2% Salicylic Acid Face Serum', 'description': 'Reduces blackheads & whiteheads, controls oil.', 'price': 15.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/813/200/300'},
                {'name': 'Plum Green Tea Mattifying Moisturizer', 'description': 'Lightweight, non-comedogenic moisturizer for oily skin.', 'price': 10.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/814/200/300'},
                {'name': 'Biotique Bio Bhringraj Fresh Growth Hair Oil', 'description': 'Ayurvedic oil for hair growth and scalp health.', 'price': 8.50, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/815/200/300'},
                {'name': 'St. Ives Fresh Skin Apricot Scrub - 170g', 'description': 'Deeply exfoliates for clean, glowing skin.', 'price': 6.50, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/816/200/300'},
                {'name': 'Maybelline New York Colossal Kajal', 'description': 'Smudge-proof and waterproof kajal for intense black lines.', 'price': 4.00, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/817/200/300'},
                {'name': 'Lakme 9 to 5 Primer + Matte Powder Foundation', 'description': '2-in-1 powder foundation with primer.', 'price': 18.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/818/200/300'},
                {'name': 'Beardhood Beard & Moustache Wax', 'description': 'Provides strong hold and nourishment for beard.', 'price': 9.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/819/200/300'},
                {'name': 'Gillette Mach3 Razor', 'description': '3-blade system for a close and comfortable shave.', 'price': 12.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/820/200/300'},
                {'name': 'Oral-B CrossAction Electric Toothbrush', 'description': 'Removes up to 100% more plaque than a regular toothbrush.', 'price': 25.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/821/200/300'},
                {'name': 'Nail Polish Remover - Acetone Free', 'description': 'Gentle nail polish remover with vitamin E.', 'price': 3.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/822/200/300'},
                {'name': 'VLCC Gold Facial Kit', 'description': '4-step facial kit for radiant and glowing skin.', 'price': 15.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/823/200/300'},
                {'name': 'Patanjali Aloevera Gel', 'description': 'Pure aloe vera gel for skin and hair.', 'price': 4.00, 'stock_quantity': 250, 'image_url': 'https://picsum.photos/id/824/200/300'},
                {'name': 'Durex Mutual Climax Condoms (Pack of 10)', 'description': 'Designed for mutual climax.', 'price': 8.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/825/200/300'},
                {'name': 'Vicks VapoRub - 50g', 'description': 'Cough and cold relief balm.', 'price': 3.50, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/826/200/300'},
                {'name': 'Streax Pro Argan Qwik Color - Black', 'description': 'Instant hair color in a gel form.', 'price': 6.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/827/200/300'},
                {'name': 'The Man Company Charcoal Face Wash', 'description': 'Deep cleansing face wash for men.', 'price': 7.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/828/200/300'},
                {'name': 'Joy Skin Fruits Face Wash - 100ml', 'description': 'Refreshing fruit-based face wash.', 'price': 4.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/829/200/300'},
            ],
            'Furniture': [
                {'name': 'Wakefit Orthopedic Memory Foam Mattress - Queen', 'description': 'Medium firm mattress for back support and comfort.', 'price': 250.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/900/200/300'},
                {'name': 'DeckUp Uniti 3-Door Wardrobe', 'description': 'Spacious wooden wardrobe with mirror and drawers.', 'price': 300.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/901/200/300'},
                {'name': 'Nilkamal Novella 1-Seater Sofa', 'description': 'Comfortable fabric sofa, ideal for small living rooms.', 'price': 180.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/902/200/300'},
                {'name': 'Bluewud Andrea Coffee Table', 'description': 'Modern wooden coffee table for living room.', 'price': 80.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/903/200/300'},
                {'name': 'Bharat Lifestyle Apollo Queen Bed', 'description': 'Engineered wood queen size bed without storage.', 'price': 220.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/904/200/300'},
                {'name': 'Godrej Interio Study Table', 'description': 'Compact study table with drawer and shelf.', 'price': 90.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/905/200/300'},
                {'name': 'Chair Factory Ergonomic Office Chair', 'description': 'High back ergonomic chair with lumbar support.', 'price': 120.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/906/200/300'},
                {'name': 'Supreme Plastic Armchair - Set of 2', 'description': 'Durable plastic armchairs for outdoor or indoor use.', 'price': 50.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/907/200/300'},
                {'name': 'Woodland Leatherette Recliner', 'description': 'Single seater recliner for ultimate comfort.', 'price': 280.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/id/908/200/300'},
                {'name': 'Urban Ladder Apolo Bookshelf', 'description': 'Multi-tier wooden bookshelf for books and decor.', 'price': 110.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/909/200/300'},
                {'name': 'Pepperfry Alia 2-Seater Sofa', 'description': 'Compact and stylish 2-seater sofa.', 'price': 250.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/910/200/300'},
                {'name': 'Furlenco Sofa Cum Bed - 3 Seater', 'description': 'Convertible sofa that transforms into a bed.', 'price': 350.00, 'stock_quantity': 22, 'image_url': 'https://picsum.photos/id/911/200/300'},
                {'name': 'King Size Solid Wood Bed', 'description': 'Premium solid wood bed with intricate carvings.', 'price': 400.00, 'stock_quantity': 18, 'image_url': 'https://picsum.photos/id/912/200/300'},
                {'name': 'Dressing Table with Mirror', 'description': 'Wooden dressing table with storage drawers and mirror.', 'price': 150.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/913/200/300'},
                {'name': 'Dining Table Set - 4 Seater', 'description': 'Compact dining table set with 4 chairs.', 'price': 200.00, 'stock_quantity': 27, 'image_url': 'https://picsum.photos/id/914/200/300'},
                {'name': 'Bar Stool - Adjustable Height', 'description': 'Modern bar stool with adjustable height and swivel function.', 'price': 40.00, 'stock_quantity': 48, 'image_url': 'https://picsum.photos/id/915/200/300'},
                {'name': 'Kids Study Table and Chair Set', 'description': 'Ergonomic study set for children, adjustable height.', 'price': 70.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/916/200/300'},
                {'name': 'Outdoor Patio Furniture Set', 'description': 'Weather-resistant set for garden or balcony.', 'price': 320.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/917/200/300'},
                {'name': 'TV Unit Entertainment Center', 'description': 'Modern TV unit with storage for media devices.', 'price': 130.00, 'stock_quantity': 38, 'image_url': 'https://picsum.photos/id/918/200/300'},
                {'name': 'Shoe Rack - 4 Tiers', 'description': 'Compact shoe rack for organizing footwear.', 'price': 30.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/919/200/300'},
                {'name': 'Bean Bag Chair - Large', 'description': 'Comfortable and relaxing large bean bag chair.', 'price': 60.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/920/200/300'},
                {'name': 'Floor Lamp - Modern Design', 'description': 'Tall floor lamp with minimalist design for ambient lighting.', 'price': 45.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/921/200/300'},
                {'name': 'Computer Desk with Storage', 'description': 'Spacious computer desk with drawers and shelves.', 'price': 100.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/922/200/300'},
                {'name': 'Wall Shelf - Floating Design', 'description': 'Set of 3 floating wall shelves for decor and storage.', 'price': 25.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/923/200/300'},
                {'name': 'Wardrobe - 2 Door Metal', 'description': 'Durable metal wardrobe for compact spaces.', 'price': 180.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/924/200/300'},
                {'name': 'Accent Chair - Velvet Upholstery', 'description': 'Stylish accent chair with plush velvet upholstery.', 'price': 160.00, 'stock_quantity': 28, 'image_url': 'https://picsum.photos/id/925/200/300'},
                {'name': 'Console Table - Entryway', 'description': 'Slim console table perfect for entryways or hallways.', 'price': 70.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/926/200/300'},
                {'name': 'Office Storage Cabinet', 'description': 'Lockable filing cabinet for office documents.', 'price': 110.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/927/200/300'},
                {'name': 'Kids Bunk Bed', 'description': 'Space-saving bunk bed for children\'s room.', 'price': 280.00, 'stock_quantity': 15, 'image_url': 'https://picsum.photos/id/928/200/300'},
                {'name': 'Pouf Ottoman - Fabric', 'description': 'Versatile pouf ottoman for seating or footrest.', 'price': 35.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/929/200/300'},
            ],
            'Electronics Accessories': [
                {'name': 'Anker PowerCore 10000mAh Power Bank', 'description': 'Compact and fast-charging power bank for smartphones.', 'price': 25.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/1000/200/300'},
                {'name': 'JBL C100SI In-Ear Headphones', 'description': 'Deep bass sound with noise isolating microphone.', 'price': 12.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/1001/200/300'},
                {'name': 'SanDisk Ultra Dual Drive Go USB Type-C 128GB', 'description': 'Dual USB-C and USB-A flash drive for easy transfers.', 'price': 18.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/1002/200/300'},
                {'name': 'Logitech M220 Silent Wireless Mouse', 'description': 'Quiet clicks and comfortable grip wireless mouse.', 'price': 15.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/1003/200/300'},
                {'name': 'HP K500F Gaming Keyboard', 'description': 'Wired gaming keyboard with Rainbow Backlit and Metal Panel.', 'price': 30.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/1004/200/300'},
                {'name': 'WD Elements Portable External Hard Drive 1TB', 'description': 'High-capacity external hard drive for backups.', 'price': 60.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/1005/200/300'},
                {'name': 'Boat Airdopes 131 True Wireless Earbuds', 'description': 'Immersive audio with 15 hours playtime.', 'price': 20.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/1006/200/300'},
                {'name': 'Portronics Adapto 20 Fast Charger 20W', 'description': 'PD fast charger for iPhones and Android devices.', 'price': 10.00, 'stock_quantity': 160, 'image_url': 'https://picsum.photos/id/1007/200/300'},
                {'name': 'AmazonBasics HDMI Cable - 10 feet', 'description': 'High-speed HDMI cable for connecting devices to TV.', 'price': 8.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/1008/200/300'},
                {'name': 'TP-Link TL-WN725N USB Wi-Fi Adapter', 'description': 'Nano size USB Wi-Fi adapter for desktop or laptop.', 'price': 7.00, 'stock_quantity': 140, 'image_url': 'https://picsum.photos/id/1009/200/300'},
                {'name': 'Seagate Expansion Desktop Hard Drive 4TB', 'description': 'Large capacity desktop storage solution.', 'price': 100.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/1010/200/300'},
                {'name': 'Sony WH-1000XM5 Noise Cancelling Headphones', 'description': 'Industry-leading noise cancellation with exceptional sound.', 'price': 350.00, 'stock_quantity': 25, 'image_url': 'https://picsum.photos/id/1011/200/300'},
                {'name': 'Apple AirPods Pro 2nd Gen', 'description': 'Active Noise Cancellation with Adaptive Transparency.', 'price': 250.00, 'stock_quantity': 35, 'image_url': 'https://picsum.photos/id/1012/200/300'},
                {'name': 'Redgear Pro Series Wired Gamepad', 'description': 'Ergonomic gamepad for PC gaming.', 'price': 22.00, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/1013/200/300'},
                {'name': 'Logitech C920s HD Pro Webcam', 'description': 'Full HD 1080p video calling and recording.', 'price': 70.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/1014/200/300'},
                {'name': 'AmazonBasics AA Alkaline Batteries (Pack of 10)', 'description': 'Long-lasting alkaline batteries for various devices.', 'price': 5.00, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/1015/200/300'},
                {'name': 'boAt Stone 1000 Bluetooth Speaker', 'description': 'Powerful and portable Bluetooth speaker with rich bass.', 'price': 40.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/1016/200/300'},
                {'name': 'D-Link DIR-615 Wireless N300 Router', 'description': 'High-speed wireless router for home networks.', 'price': 28.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/1017/200/300'},
                {'name': 'Dell KM117 Wireless Keyboard and Mouse Combo', 'description': 'Compact wireless combo for everyday use.', 'price': 25.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/1018/200/300'},
                {'name': 'Generic Laptop Cooling Pad', 'description': 'USB-powered cooling pad with dual fans for laptops.', 'price': 15.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/1019/200/300'},
                {'name': 'Samsung EVO Select Micro SD Card 256GB', 'description': 'High-speed memory card for phones and cameras.', 'price': 35.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/1020/200/300'},
                {'name': 'Google Chromecast with Google TV', 'description': 'Stream entertainment from your phone to TV with smart TV features.', 'price': 49.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/1021/200/300'},
                {'name': 'Fire TV Stick 4K Max', 'description': 'Streaming stick with Wi-Fi 6 support and Alexa voice remote.', 'price': 55.00, 'stock_quantity': 55, 'image_url': 'https://picsum.photos/id/1022/200/300'},
                {'name': 'Xbox Wireless Controller - Robot White', 'description': 'Modernized design with sculpted surfaces and refined geometry.', 'price': 60.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/1023/200/300'},
                {'name': 'Nintendo Switch Pro Controller', 'description': 'Premium game controller for Nintendo Switch.', 'price': 70.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/1024/200/300'},
                {'name': 'Ugreen USB C Hub 6-in-1', 'description': 'Multi-port adapter with HDMI, USB 3.0, and SD card readers.', 'price': 30.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/1025/200/300'},
                {'name': 'TP-Link Kasa Smart Plug Mini (2-pack)', 'description': 'Smart Wi-Fi plugs for controlling devices remotely.', 'price': 20.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/1026/200/300'},
                {'name': 'Logitech H111 Wired Headset', 'description': 'Stereo headset with noise-canceling mic for calls.', 'price': 18.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/1027/200/300'},
                {'name': 'Razer DeathAdder Essential Gaming Mouse', 'description': 'Ergonomic wired gaming mouse with high-precision sensor.', 'price': 35.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/1028/200/300'},
                {'name': 'Blue Yeti USB Microphone', 'description': 'Popular USB microphone for podcasting and streaming.', 'price': 100.00, 'stock_quantity': 30, 'image_url': 'https://picsum.photos/id/1029/200/300'},
            ],
            'Kids & Baby': [
                {'name': 'Pampers Premium Care Diapers - Size M (50 Count)', 'description': 'Softest diapers for baby\'s delicate skin.', 'price': 20.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/1100/200/300'},
                {'name': 'Himalaya Gentle Baby Shampoo - 200ml', 'description': 'Mild shampoo for baby\'s hair, no tears formula.', 'price': 6.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/1101/200/300'},
                {'name': 'Fisher-Price Rocker & Play', 'description': 'Infant to toddler rocker with soothing vibrations.', 'price': 45.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/1102/200/300'},
                {'name': 'Lego Duplo My First Animals - 10904', 'description': 'Large building blocks for toddlers to learn animals.', 'price': 25.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/1103/200/300'},
                {'name': 'Johnson\'s Baby Oil - 200ml', 'description': 'Pure mineral oil for baby massage and hydration.', 'price': 4.00, 'stock_quantity': 200, 'image_url': 'https://picsum.photos/id/1104/200/300'},
                {'name': 'MamyPoko Pants Diapers - Size L (44 Count)', 'description': 'Pant-style diapers for easy changing.', 'price': 18.00, 'stock_quantity': 130, 'image_url': 'https://picsum.photos/id/1105/200/300'},
                {'name': 'Chicco Baby Moments Body Lotion - 200ml', 'description': 'Nourishing lotion for baby\'s soft skin.', 'price': 7.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/1106/200/300'},
                {'name': 'Graco Pack \'n Play Portable Playard', 'description': 'Full-size bassinet and playard for infants.', 'price': 90.00, 'stock_quantity': 40, 'image_url': 'https://picsum.photos/id/1107/200/300'},
                {'name': 'Mega Bloks First Builders Bag - 80 Pieces', 'description': 'Classic building blocks for creative play.', 'price': 20.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/1108/200/300'},
                {'name': 'Crayola Super Tips Washable Markers - 50 Count', 'description': 'Versatile markers for drawing and coloring.', 'price': 15.00, 'stock_quantity': 120, 'image_url': 'https://picsum.photos/id/1109/200/300'},
                {'name': 'Hot Wheels 5-Car Gift Set', 'description': 'Collection of 5 die-cast cars for young enthusiasts.', 'price': 10.00, 'stock_quantity': 150, 'image_url': 'https://picsum.photos/id/1110/200/300'},
                {'name': 'Barbie Dreamhouse Playset', 'description': 'Multi-story dollhouse with furniture and accessories.', 'price': 150.00, 'stock_quantity': 20, 'image_url': 'https://picsum.photos/id/1111/200/300'},
                {'name': 'Mattel Uno Card Game', 'description': 'Classic family card game for ages 7 and up.', 'price': 7.00, 'stock_quantity': 180, 'image_url': 'https://picsum.photos/id/1112/200/300'},
                {'name': 'LuvLap Stroller Cum Pram', 'description': 'Lightweight and foldable stroller for babies.', 'price': 60.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/1113/200/300'},
                {'name': 'Farlin Baby Bottle Cleanser - 700ml', 'description': 'Natural plant-based cleanser for baby bottles.', 'price': 9.00, 'stock_quantity': 100, 'image_url': 'https://picsum.photos/id/1114/200/300'},
                {'name': 'Mee Mee Walker with Push Handle', 'description': 'Adjustable baby walker with musical tray.', 'price': 35.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/1115/200/300'},
                {'name': 'Soft Toy - Teddy Bear 2 Feet', 'description': 'Large, cuddly teddy bear, perfect for hugs.', 'price': 25.00, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/1116/200/300'},
                {'name': 'Wooden Blocks Set - 100 Pieces', 'description': 'Educational wooden blocks for creative building.', 'price': 30.00, 'stock_quantity': 95, 'image_url': 'https://picsum.photos/id/1117/200/300'},
                {'name': 'Kids Scooter - 3 Wheel Adjustable', 'description': 'Stable 3-wheel scooter for young riders.', 'price': 40.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/1118/200/300'},
                {'name': 'Baby Carrier - Ergonomic', 'description': 'Comfortable baby carrier for parents and babies.', 'price': 50.00, 'stock_quantity': 65, 'image_url': 'https://picsum.photos/id/1119/200/300'},
                {'name': 'Mustela Baby Lotion - 300ml', 'description': 'Hydrating and protective daily lotion for baby.', 'price': 14.00, 'stock_quantity': 80, 'image_url': 'https://picsum.photos/id/1120/200/300'},
                {'name': 'Philips Avent Natural Baby Bottle - 9oz (2-pack)', 'description': 'Natural nipple shape for easy latch on.', 'price': 18.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/1121/200/300'},
                {'name': 'Disney Princess Doll Set', 'description': 'Collection of popular Disney Princess dolls.', 'price': 40.00, 'stock_quantity': 70, 'image_url': 'https://picsum.photos/id/1122/200/300'},
                {'name': 'Toy Remote Control Car', 'description': 'High-speed RC car for kids.', 'price': 30.00, 'stock_quantity': 85, 'image_url': 'https://picsum.photos/id/1123/200/300'},
                {'name': 'Kids Art Easel with Whiteboard & Chalkboard', 'description': 'Double-sided easel for drawing and learning.', 'price': 55.00, 'stock_quantity': 60, 'image_url': 'https://picsum.photos/id/1124/200/300'},
                {'name': 'Baby Monitor with Camera', 'description': 'Video baby monitor with night vision and two-way talk.', 'price': 80.00, 'stock_quantity': 45, 'image_url': 'https://picsum.photos/id/1125/200/300'},
                {'name': 'R for Rabbit Tiny Toes Grand Stroller', 'description': 'Stylish and feature-packed stroller.', 'price': 70.00, 'stock_quantity': 50, 'image_url': 'https://picsum.photos/id/1126/200/300'},
                {'name': 'Cloud Bedtime Plush Toy', 'description': 'Soft plush toy that lights up and plays lullabies.', 'price': 22.00, 'stock_quantity': 90, 'image_url': 'https://picsum.photos/id/1127/200/300'},
                {'name': 'Kids Story Book Set - Moral Stories', 'description': 'Collection of engaging story books with moral lessons.', 'price': 15.00, 'stock_quantity': 110, 'image_url': 'https://picsum.photos/id/1128/200/300'},
                {'name': 'Learning Tablet - Toddler Edition', 'description': 'Interactive tablet for early learning and play.', 'price': 35.00, 'stock_quantity': 75, 'image_url': 'https://picsum.photos/id/1129/200/300'},
            ],
        }
        # --- END MODIFIED SPECIFIC PRODUCTS DATA ---

        self.stdout.write("Populating products with specific names...")
        total_products_created = 0
        for category_name, products_list in specific_products_by_category.items():
            category_obj = created_categories.get(category_name)
            if not category_obj:
                self.stdout.write(self.style.WARNING(f'Skipping products for missing category: {category_name}'))
                continue

            for product_data in products_list:
                # --- MODIFIED PRODUCT CREATION LOGIC ---
                # Prioritize provided values, fall back to Faker/random if not specified
                product_description = product_data.get('description', fake.paragraph(nb_sentences=3))
                product_stock = product_data.get('stock_quantity', random.randint(10, 200))
                product_image_url = product_data.get('image_url', fake.image_url())
                # --- END MODIFIED PRODUCT CREATION LOGIC ---
                
                # Create a unique SKU, trying a few times if there's a collision
                product_sku = None
                for _ in range(5): # Try 5 times to generate a unique SKU
                    try:
                        sku_prefix = category_name[:3].upper()
                        # Use ean8 for consistency, fall back to random_number if Faker runs out
                        generated_sku_suffix = fake.unique.ean8() if hasattr(fake.unique, 'ean8') else fake.random_number(digits=8)
                        temp_sku = f"{sku_prefix}-{generated_sku_suffix}"
                        
                        # Check if SKU already exists
                        if not Product.objects.filter(sku=temp_sku).exists():
                            product_sku = temp_sku
                            break # SKU is unique, break from retry loop
                        else:
                            # If it exists, clear unique cache for Faker if applicable, or just let it try again
                            if hasattr(fake.unique, 'clear'):
                                fake.unique.clear() 
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f'SKU generation issue: {e}. Retrying or falling back.'))
                        # Fallback for faker unique issue if it's exhausted
                        if hasattr(fake.unique, 'clear'): # Try clearing unique if available
                            fake.unique.clear()
                        product_sku = f"{sku_prefix}-{fake.random_number(digits=8)}" # Fallback to generic random number
                        break # Break after fallback to avoid infinite loop on faker unique exhaustion

                if not product_sku: # If after retries, SKU is still not generated uniquely
                    product_sku = f"{category_name[:3].upper()}-{fake.random_number(digits=9)}" # Ensure it's generated
                    self.stdout.write(self.style.ERROR(f'Failed to generate unique SKU after retries for {product_data["name"]}, using a fallback random SKU.'))


                is_available = random.choice([True, True, True, False]) # More likely to be available

                Product.objects.create(
                    name=product_data['name'],
                    description=product_description, # Now uses the 'description' from data or generates
                    price=product_data['price'],
                    category=category_obj,
                    stock_quantity=product_stock,    # Now uses the 'stock_quantity' from data or generates
                    image_url=product_image_url,     # Now uses the 'image_url' from data or generates
                    sku=product_sku,
                    is_available=is_available
                )
                self.stdout.write(f'  - Created product: {product_data["name"]} ({category_name})')
                total_products_created += 1

        # This part ensures you have a good total count if your specific lists are short.
        # You can remove or adjust it if you only want explicitly defined products.
        target_products_count = sum(len(products) for products in specific_products_by_category.values()) + 50 # Add 50 extra random ones
        
        if total_products_created < target_products_count:
            self.stdout.write(f"Adding additional random products to reach target of {target_products_count}...")
        
        while total_products_created < target_products_count:
            random_category_name = random.choice(list(created_categories.keys()))
            category_obj = created_categories.get(random_category_name)

            product_name = fake.unique.word().capitalize() + " " + fake.word().capitalize()
            product_description = fake.paragraph(nb_sentences=3, variable_nb_sentences=True)
            product_price = round(random.uniform(10, 1000), 2)
            product_stock = random.randint(0, 150)
            product_image_url = fake.image_url()
            
            # Ensure unique SKU for random products as well
            current_random_sku = None
            for _ in range(5):
                try:
                    sku_prefix = random_category_name[:3].upper()
                    generated_sku_suffix = fake.unique.ean8() if hasattr(fake.unique, 'ean8') else fake.random_number(digits=8)
                    temp_sku = f"{sku_prefix}-{generated_sku_suffix}"
                    if not Product.objects.filter(sku=temp_sku).exists():
                        current_random_sku = temp_sku
                        break
                    else:
                        if hasattr(fake.unique, 'clear'):
                            fake.unique.clear() # Try clearing unique if available
                except Exception:
                    pass
            else:
                 current_random_sku = f"{random_category_name[:3].upper()}-{fake.random_number(digits=9)}"
            
            is_available = random.choice([True, False])

            try:
                Product.objects.create(
                    name=product_name,
                    description=product_description,
                    price=product_price,
                    category=category_obj,
                    stock_quantity=product_stock,
                    image_url=product_image_url,
                    sku=current_random_sku,
                    is_available=is_available
                )
                self.stdout.write(f'  - Created additional random product: {product_name}')
                total_products_created += 1
            except Exception as e:
                # This might happen if faker runs out of unique words/ean8s or SKUs
                self.stdout.write(self.style.WARNING(f'Could not create unique random product (SKU/name likely duplicate): {e}'))
                break # Exit loop if we can't create more unique products

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {total_products_created} products and {len(created_categories)} categories.'))