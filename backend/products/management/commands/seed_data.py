from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from decimal import Decimal
import random
import uuid

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed database with sample data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create admin user
        self.create_admin_user()
        
        # Create categories
        categories = self.create_categories()
        
        # Create products
        self.create_products(categories)
        
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
    
    def create_admin_user(self):
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='admin123',
                first_name='Admin',
                last_name='User',
                is_admin=True
            )
            self.stdout.write(self.style.SUCCESS('Admin user created: admin@example.com / admin123'))
        else:
            self.stdout.write('Admin user already exists')
    
    def create_categories(self):
        categories_data = [
            {'name': 'Electronics', 'slug': 'electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'slug': 'clothing', 'description': 'Fashion and apparel'},
            {'name': 'Home & Kitchen', 'slug': 'home-kitchen', 'description': 'Home appliances and kitchen items'},
            {'name': 'Books', 'slug': 'books', 'description': 'Books and publications'},
            {'name': 'Sports & Outdoors', 'slug': 'sports-outdoors', 'description': 'Sports equipment and outdoor gear'},
            {'name': 'Beauty & Health', 'slug': 'beauty-health', 'description': 'Beauty products and health items'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        return categories
    
    def create_products(self, categories):
        # Product images from Unsplash - properly matched to product names
        products_data = {
            'electronics': [
                {'name': 'Wireless Bluetooth Headphones', 'price': 2499, 'discount_price': 1999, 'brand': 'SoundMax', 'stock': 50, 'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500'},
                {'name': 'Smart Watch Pro', 'price': 4999, 'discount_price': 3999, 'brand': 'TechWear', 'stock': 30, 'image': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500'},
                {'name': 'Portable Power Bank 20000mAh', 'price': 1499, 'discount_price': 1199, 'brand': 'PowerCell', 'stock': 100, 'image': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500'},
                {'name': 'Wireless Mouse', 'price': 799, 'discount_price': 599, 'brand': 'ClickPro', 'stock': 80, 'image': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500'},
                {'name': 'USB-C Hub 7-in-1', 'price': 1999, 'discount_price': 1599, 'brand': 'ConnectAll', 'stock': 60, 'image': 'https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=500'},
                {'name': 'Mechanical Gaming Keyboard', 'price': 3499, 'discount_price': 2999, 'brand': 'GameGear', 'stock': 40, 'image': 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?w=500'},
                {'name': 'Webcam HD 1080p', 'price': 2999, 'discount_price': 2499, 'brand': 'ClearView', 'stock': 45, 'image': 'https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=500'},
                {'name': 'Bluetooth Speaker', 'price': 1999, 'discount_price': 1499, 'brand': 'SoundMax', 'stock': 70, 'image': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500'},
            ],
            'clothing': [
                {'name': 'Cotton T-Shirt Classic', 'price': 599, 'discount_price': 449, 'brand': 'StyleCo', 'stock': 200, 'image': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'},
                {'name': 'Denim Jeans Slim Fit', 'price': 1999, 'discount_price': 1599, 'brand': 'DenimHub', 'stock': 150, 'image': 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=500'},
                {'name': 'Winter Jacket Warm', 'price': 3999, 'discount_price': 2999, 'brand': 'WinterWear', 'stock': 60, 'image': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'},
                {'name': 'Running Shoes Pro', 'price': 2999, 'discount_price': 2499, 'brand': 'RunFast', 'stock': 80, 'image': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500'},
                {'name': 'Formal Shirt Premium', 'price': 1299, 'discount_price': 999, 'brand': 'FormalX', 'stock': 120, 'image': 'https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500'},
                {'name': 'Casual Shorts', 'price': 799, 'discount_price': 599, 'brand': 'StyleCo', 'stock': 100, 'image': 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=500'},
            ],
            'home-kitchen': [
                {'name': 'Non-Stick Cookware Set', 'price': 4999, 'discount_price': 3999, 'brand': 'CookMaster', 'stock': 40, 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500'},
                {'name': 'Electric Kettle 1.5L', 'price': 1299, 'discount_price': 999, 'brand': 'HeatQuick', 'stock': 90, 'image': 'https://images.unsplash.com/photo-1556909172-8c2f041fca1e?w=500'},
                {'name': 'Blender Mixer 500W', 'price': 2499, 'discount_price': 1999, 'brand': 'BlendPro', 'stock': 55, 'image': 'https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=500'},
                {'name': 'Vacuum Cleaner Handheld', 'price': 3999, 'discount_price': 3499, 'brand': 'CleanEasy', 'stock': 35, 'image': 'https://images.unsplash.com/photo-1558317374-067fb5f30001?w=500'},
                {'name': 'Air Purifier HEPA', 'price': 7999, 'discount_price': 6499, 'brand': 'PureAir', 'stock': 25, 'image': 'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=500'},
                {'name': 'Coffee Maker Automatic', 'price': 5999, 'discount_price': 4999, 'brand': 'CafeBrew', 'stock': 30, 'image': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500'},
            ],
            'books': [
                {'name': 'Python Programming Guide', 'price': 599, 'discount_price': 449, 'brand': 'TechBooks', 'stock': 150, 'image': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=500'},
                {'name': 'Data Science Handbook', 'price': 799, 'discount_price': 649, 'brand': 'TechBooks', 'stock': 100, 'image': 'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=500'},
                {'name': 'Business Strategy 101', 'price': 499, 'discount_price': 399, 'brand': 'BizReads', 'stock': 120, 'image': 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=500'},
                {'name': 'Self Improvement Daily', 'price': 349, 'discount_price': 299, 'brand': 'LifeBooks', 'stock': 200, 'image': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500'},
                {'name': 'Web Development Mastery', 'price': 699, 'discount_price': 549, 'brand': 'TechBooks', 'stock': 80, 'image': 'https://images.unsplash.com/photo-1517148815978-75f6acaaf32c?w=500'},
            ],
            'sports-outdoors': [
                {'name': 'Yoga Mat Premium', 'price': 999, 'discount_price': 799, 'brand': 'FitLife', 'stock': 100, 'image': 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=500'},
                {'name': 'Dumbbells Set 10kg', 'price': 2499, 'discount_price': 1999, 'brand': 'IronFit', 'stock': 50, 'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=500'},
                {'name': 'Camping Tent 4-Person', 'price': 5999, 'discount_price': 4999, 'brand': 'OutdoorPro', 'stock': 30, 'image': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500'},
                {'name': 'Water Bottle Insulated', 'price': 599, 'discount_price': 449, 'brand': 'HydroMax', 'stock': 150, 'image': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500'},
                {'name': 'Resistance Bands Set', 'price': 799, 'discount_price': 599, 'brand': 'FitLife', 'stock': 120, 'image': 'https://images.unsplash.com/photo-1598289431512-b97b0917affc?w=500'},
                {'name': 'Cycling Helmet', 'price': 1999, 'discount_price': 1599, 'brand': 'SafeRide', 'stock': 60, 'image': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500'},
            ],
            'beauty-health': [
                {'name': 'Face Moisturizer SPF 30', 'price': 899, 'discount_price': 699, 'brand': 'GlowSkin', 'stock': 100, 'image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500'},
                {'name': 'Hair Dryer Professional', 'price': 2499, 'discount_price': 1999, 'brand': 'StylePro', 'stock': 60, 'image': 'https://images.unsplash.com/photo-1522338140262-f46f5913618a?w=500'},
                {'name': 'Electric Toothbrush', 'price': 1999, 'discount_price': 1499, 'brand': 'DentaCare', 'stock': 80, 'image': 'https://images.unsplash.com/photo-1559650656-5d1d361ad10e?w=500'},
                {'name': 'Vitamin C Serum', 'price': 1299, 'discount_price': 999, 'brand': 'GlowSkin', 'stock': 90, 'image': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500'},
                {'name': 'Massage Gun Pro', 'price': 4999, 'discount_price': 3999, 'brand': 'RelaxMax', 'stock': 40, 'image': 'https://images.unsplash.com/photo-1617952739858-28043cecdae3?w=500'},
            ],
        }
        
        for category in categories:
            cat_products = products_data.get(category.slug, [])
            for i, prod_data in enumerate(cat_products):
                sku = f"{category.slug[:3].upper()}-{str(uuid.uuid4())[:8].upper()}"
                
                product, created = Product.objects.get_or_create(
                    sku=sku,
                    defaults={
                        'name': prod_data['name'],
                        'slug': f"{prod_data['name'].lower().replace(' ', '-')}-{str(uuid.uuid4())[:4]}",
                        'description': f"High quality {prod_data['name']}. Perfect for your needs. "
                                      f"Brand: {prod_data['brand']}. Features premium quality materials.",
                        'short_description': f"Premium {prod_data['name']} by {prod_data['brand']}",
                        'price': Decimal(str(prod_data['price'])),
                        'discount_price': Decimal(str(prod_data['discount_price'])) if prod_data.get('discount_price') else None,
                        'category': category,
                        'stock': prod_data['stock'],
                        'brand': prod_data['brand'],
                        'image_url': prod_data.get('image', ''),  # Use external image URL
                        'is_active': True,
                        'is_featured': random.choice([True, False, False]),  # 33% chance of being featured
                        'specifications': {
                            'brand': prod_data['brand'],
                            'warranty': '1 Year',
                            'material': 'Premium Quality',
                        }
                    }
                )
                if created:
                    self.stdout.write(f'Created product: {product.name}')
