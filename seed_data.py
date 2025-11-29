"""
Seed script to populate the database with dummy furniture data
Run this with: python seed_data.py
"""
from app import create_app, db
from app.models import User, Category, Product, ProductImage
from werkzeug.security import generate_password_hash

app = create_app()

def seed_data():
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional - comment out if you want to keep existing data)
        # db.drop_all()
        # db.create_all()
        
        # Create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@npfstore.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Created admin user (username: admin, password: admin123)")
        
        # Create categories
        categories_data = [
            {'name': 'Living Room', 'slug': 'living-room'},
            {'name': 'Bedroom', 'slug': 'bedroom'},
            {'name': 'Dining Room', 'slug': 'dining-room'},
            {'name': 'Office', 'slug': 'office'},
            {'name': 'Outdoor', 'slug': 'outdoor'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat = Category.query.filter_by(slug=cat_data['slug']).first()
            if not cat:
                cat = Category(**cat_data)
                db.session.add(cat)
                db.session.flush()
            categories[cat_data['name']] = cat
        
        print(f"✅ Created {len(categories)} categories")
        
        # Create products with real furniture images from Unsplash
        products_data = [
            # Living Room
            {
                'name': 'Modern L-Shape Sofa',
                'slug': 'modern-l-shape-sofa',
                'description': 'Luxurious L-shaped sofa with premium fabric upholstery. Perfect for modern living rooms with ample seating space.',
                'price': 89999,
                'stock': 8,
                'category': 'Living Room',
                'images': [
                    'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=800',
                    'https://images.unsplash.com/photo-1493663284031-b7e3aefcae8e?w=800',
                ]
            },
            {
                'name': 'Velvet Accent Chair',
                'slug': 'velvet-accent-chair',
                'description': 'Elegant velvet accent chair with golden legs. Adds a touch of luxury to any room.',
                'price': 24999,
                'stock': 15,
                'category': 'Living Room',
                'images': [
                    'https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=800',
                ]
            },
            {
                'name': 'Marble Coffee Table',
                'slug': 'marble-coffee-table',
                'description': 'Contemporary coffee table with genuine marble top and brass frame.',
                'price': 34999,
                'stock': 12,
                'category': 'Living Room',
                'images': [
                    'https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=800',
                ]
            },
            {
                'name': 'Scandinavian TV Unit',
                'slug': 'scandinavian-tv-unit',
                'description': 'Minimalist TV stand with oak wood finish and ample storage space.',
                'price': 45999,
                'stock': 6,
                'category': 'Living Room',
                'images': [
                    'https://images.unsplash.com/photo-1594026112284-02bb6f3352fe?w=800',
                ]
            },
            
            # Bedroom
            {
                'name': 'King Size Upholstered Bed',
                'slug': 'king-size-upholstered-bed',
                'description': 'Luxurious king-size bed with tufted headboard and premium fabric.',
                'price': 124999,
                'stock': 5,
                'category': 'Bedroom',
                'images': [
                    'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=800',
                ]
            },
            {
                'name': 'Wooden Wardrobe',
                'slug': 'wooden-wardrobe',
                'description': 'Spacious 4-door wardrobe with mirror and multiple compartments.',
                'price': 79999,
                'stock': 4,
                'category': 'Bedroom',
                'images': [
                    'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',
                ]
            },
            {
                'name': 'Bedside Table Set',
                'slug': 'bedside-table-set',
                'description': 'Pair of elegant bedside tables with drawers and modern design.',
                'price': 18999,
                'stock': 20,
                'category': 'Bedroom',
                'images': [
                    'https://images.unsplash.com/photo-1558211583-803a5f8cb25f?w=800',
                ]
            },
            
            # Dining Room
            {
                'name': '6-Seater Dining Table Set',
                'slug': '6-seater-dining-table-set',
                'description': 'Complete dining set with solid wood table and 6 cushioned chairs.',
                'price': 94999,
                'stock': 7,
                'category': 'Dining Room',
                'images': [
                    'https://images.unsplash.com/photo-1617806118233-18e1de247200?w=800',
                ]
            },
            {
                'name': 'Modern Bar Stools',
                'slug': 'modern-bar-stools',
                'description': 'Set of 2 adjustable bar stools with leather seats and chrome base.',
                'price': 15999,
                'stock': 25,
                'category': 'Dining Room',
                'images': [
                    'https://images.unsplash.com/photo-1551298370-9d3d53740c72?w=800',
                ]
            },
            {
                'name': 'Glass Display Cabinet',
                'slug': 'glass-display-cabinet',
                'description': 'Elegant display cabinet with glass doors and LED lighting.',
                'price': 54999,
                'stock': 3,
                'category': 'Dining Room',
                'images': [
                    'https://images.unsplash.com/photo-1595428774223-ef52624120d2?w=800',
                ]
            },
            
            # Office
            {
                'name': 'Executive Office Desk',
                'slug': 'executive-office-desk',
                'description': 'Premium L-shaped office desk with built-in storage and cable management.',
                'price': 64999,
                'stock': 10,
                'category': 'Office',
                'images': [
                    'https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=800',
                ]
            },
            {
                'name': 'Ergonomic Office Chair',
                'slug': 'ergonomic-office-chair',
                'description': 'High-back ergonomic chair with lumbar support and adjustable armrests.',
                'price': 29999,
                'stock': 18,
                'category': 'Office',
                'images': [
                    'https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=800',
                ]
            },
            {
                'name': 'Bookshelf Unit',
                'slug': 'bookshelf-unit',
                'description': '5-tier open bookshelf with modern ladder design.',
                'price': 22999,
                'stock': 14,
                'category': 'Office',
                'images': [
                    'https://images.unsplash.com/photo-1594620302200-9a762244a156?w=800',
                ]
            },
            
            # Outdoor
            {
                'name': 'Patio Dining Set',
                'slug': 'patio-dining-set',
                'description': 'Weather-resistant outdoor dining set with 4 chairs and umbrella.',
                'price': 74999,
                'stock': 6,
                'category': 'Outdoor',
                'images': [
                    'https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?w=800',
                ]
            },
            {
                'name': 'Garden Lounge Chairs',
                'slug': 'garden-lounge-chairs',
                'description': 'Set of 2 reclining lounge chairs with cushions for outdoor relaxation.',
                'price': 39999,
                'stock': 9,
                'category': 'Outdoor',
                'images': [
                    'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800',
                ]
            },
        ]
        
        for prod_data in products_data:
            # Check if product already exists
            existing = Product.query.filter_by(slug=prod_data['slug']).first()
            if existing:
                continue
                
            images = prod_data.pop('images')
            category_name = prod_data.pop('category')
            
            product = Product(
                **prod_data,
                category_id=categories[category_name].id
            )
            db.session.add(product)
            db.session.flush()
            
            # Add images
            for img_url in images:
                img = ProductImage(image_url=img_url, product_id=product.id)
                db.session.add(img)
        
        db.session.commit()
        print(f"✅ Created {len(products_data)} products with images")
        print("\n🎉 Database seeding completed!")
        print("\n📝 Admin credentials:")
        print("   Username: admin")
        print("   Password: admin123")

if __name__ == '__main__':
    seed_data()
