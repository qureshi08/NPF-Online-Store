# NPF Online Store - User Guide

Welcome to the NPF Online Store! This guide will help you set up, run, and manage your e-commerce application.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher
- Git

### 2. Installation
1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone https://github.com/qureshi08/NPF-Online-Store.git
    cd "NPF Online Store"
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables**:
    Create a `.env` file in the root directory with the following content:
    ```
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=sqlite:///app.db
    CLOUDINARY_CLOUD_NAME=your_cloud_name
    CLOUDINARY_API_KEY=your_api_key
    CLOUDINARY_API_SECRET=your_api_secret
    STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
    STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
    ```
    
    **Getting Stripe Keys:**
    - Sign up at [stripe.com](https://stripe.com)
    - Go to Developers > API keys
    - Copy your Publishable key (starts with `pk_test_`) and Secret key (starts with `sk_test_`)
    - For production, use live keys (pk_live_ and sk_live_)

5.  **Initialize the Database**:
    ```bash
    flask db upgrade
    ```
    *If you encounter issues, you can delete the `app.db` file and `migrations` folder, then run:*
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

### 3. Running the Application
```bash
flask run
```
The application will be available at `http://127.0.0.1:5000`.

---

## 🔑 Admin Access

To access the Admin Dashboard, you need an account with admin privileges. Since there is no "Sign Up as Admin" page for security reasons, you must create one manually or promote an existing user.

### Option A: Create Admin via Script (Recommended)
1.  Create a file named `create_admin.py` in the root directory with the following content:
    ```python
    from app import create_app, db
    from app.models import User

    app = create_app()

    with app.app_context():
        username = input("Enter Admin Username: ")
        email = input("Enter Admin Email: ")
        password = input("Enter Admin Password: ")
        
        if User.query.filter_by(email=email).first():
            print("User with this email already exists!")
        else:
            user = User(username=username, email=email, is_admin=True)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            print(f"Admin user {username} created successfully!")
    ```
2.  Run the script:
    ```bash
    python create_admin.py
    ```

### Option B: Promote Existing User via Flask Shell
1.  Register a new user on the website.
2.  Open the terminal and run:
    ```bash
    flask shell
    ```
3.  In the shell, run:
    ```python
    >>> from app import db
    >>> from app.models import User
    >>> user = User.query.filter_by(email='your_email@example.com').first()
    >>> user.is_admin = True
    >>> db.session.commit()
    >>> exit()
    ```

---

## 🛒 Application Flow

### 1. Browsing & Shopping
-   **Homepage**: Features a Hero Slider, Categories, Featured Products, and Testimonials.
-   **Shop Page**:
    -   **Search**: Use the search bar in the sidebar to find products.
    -   **Filter**: Filter by Category and Price Range.
    -   **Sort**: Sort products by Price, Name, or Newest.
-   **Product Details**: View images, description, and add to cart.

### 2. Checkout Process
1.  Add items to your cart.
2.  Click the Cart icon in the navbar.
3.  Proceed to Checkout.
4.  Enter Shipping Details (auto-filled if logged in).
5.  **Payment Method**: Choose between:
    - **Cash on Delivery**: Pay when you receive your order
    - **Bank Transfer**: Transfer to our bank account
    - **Credit/Debit Card**: Pay securely online with Stripe (requires Stripe keys to be configured)
6.  Place Order. You will see a confirmation page.

### 3. User Account
-   **Login/Register**: Create an account to track orders.
-   **My Orders**: View your order history and status. Click "View Details" to see items and invoice.

### 4. Admin Dashboard
Access via the User Dropdown > **Dashboard** (only visible to admins).
-   **Dashboard**: View Total Sales, Orders, Products, and Users. See Recent Orders.
-   **Orders**: View all orders. Update status (e.g., Pending -> Shipped -> Delivered).
-   **Products**: Add, Edit, or Delete products. Upload images.
-   **Categories**: Manage product categories.

---

## 🛠 Troubleshooting

-   **Database Errors**: If you change the `models.py` file, you must run migrations (`flask db migrate`, `flask db upgrade`).
-   **Image Uploads**: Ensure your Cloudinary credentials are correct in the `.env` file.
-   **Login Issues**: Ensure you are using the correct email/password. Check the database if needed.

Enjoy building with NPF Online Store! 🛋️
