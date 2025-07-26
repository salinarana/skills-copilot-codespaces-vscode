import streamlit as st
import pandas as pd
import datetime
from datetime import date
import numpy as np
import hashlib
import json
import os
from streamlit.components.v1 import html

# User Management Functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

def register_user(username, password, email, full_name, user_type="user"):
    """Register a new user"""
    users = load_users()
    if username in users:
        return False, "Username already exists"
    
    users[username] = {
        "password": hash_password(password),
        "email": email,
        "full_name": full_name,
        "user_type": user_type,
        "created_date": str(datetime.datetime.now()),
        "bookings": []
    }
    save_users(users)
    return True, "Registration successful"

def authenticate_user(username, password):
    """Authenticate user login"""
    users = load_users()
    if username in users and users[username]["password"] == hash_password(password):
        return True, users[username]["user_type"]
    return False, None

def get_user_info(username):
    """Get user information"""
    users = load_users()
    return users.get(username, {})

# Car Management Functions
def load_cars():
    """Load cars from JSON file"""
    if os.path.exists("cars.json"):
        try:
            with open("cars.json", "r") as f:
                cars_data = json.load(f)
                return pd.DataFrame(cars_data)
        except:
            return create_sample_cars()
    return create_sample_cars()

def save_cars(df):
    """Save cars to JSON file"""
    with open("cars.json", "w") as f:
        json.dump(df.to_dict('records'), f, indent=2)

def create_sample_cars():
    """Create sample car data"""
    data = {
        'car_id': list(range(1, 16)),
        'make': ['Toyota', 'Honda', 'Ford', 'BMW', 'Mercedes', 'Audi', 'Tesla', 'Nissan', 'Hyundai', 'Kia', 
                'Chevrolet', 'Volkswagen', 'Subaru', 'Lexus', 'Jeep'],
        'model': ['Camry', 'Civic', 'Focus', 'X5', 'C-Class', 'A4', 'Model 3', 'Altima', 'Elantra', 'Optima',
                 'Malibu', 'Jetta', 'Outback', 'RX 350', 'Wrangler'],
        'type': ['Sedan', 'Sedan', 'Hatchback', 'SUV', 'Sedan', 'Sedan', 'Sedan', 'Sedan', 'Sedan', 'Sedan',
                'Sedan', 'Sedan', 'SUV', 'SUV', 'SUV'],
        'year': [2022, 2023, 2021, 2023, 2022, 2023, 2023, 2021, 2022, 2021, 2022, 2023, 2023, 2022, 2023],
        'price_per_day': [80, 75, 65, 150, 160, 140, 180, 70, 60, 55, 70, 65, 90, 170, 130],
        'seats': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'transmission': ['Automatic']*15,
        'fuel_type': ['Gasoline', 'Gasoline', 'Gasoline', 'Diesel', 'Gasoline', 'Gasoline', 'Electric', 
                     'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 'Gasoline', 
                     'Gasoline'],
        'available': [True]*15,
        'location': ['Downtown', 'Airport']*7 + ['Downtown'],
        'image_url': [
            'https://cdn.jdpower.com/Models/640x480/2017-Toyota-Camry.jpg',
            'https://cdn.jdpower.com/Models/640x480/2021-Honda-Civic.jpg',
            'https://cdn.jdpower.com/Models/640x480/2018-Ford-Focus.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-BMW-X5.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Mercedes-Benz-C-Class.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Audi-A4.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Tesla-Model3.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Nissan-Altima.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Hyundai-Elantra.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Kia-Optima.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Chevrolet-Malibu.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Volkswagen-Jetta.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Subaru-Outback.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Lexus-RX350.jpg',
            'https://cdn.jdpower.com/Models/640x480/2022-Jeep-Wrangler.jpg'
        ]
    }
    df = pd.DataFrame(data)
    save_cars(df)
    return df

def add_car(make, model, car_type, year, price_per_day, seats, transmission, fuel_type, location, image_url):
    """Add a new car to the fleet"""
    df = load_cars()
    new_car_id = df['car_id'].max() + 1 if not df.empty else 1
    
    new_car = pd.DataFrame([{
        'car_id': new_car_id,
        'make': make,
        'model': model,
        'type': car_type,
        'year': year,
        'price_per_day': price_per_day,
        'seats': seats,
        'transmission': transmission,
        'fuel_type': fuel_type,
        'available': True,
        'location': location,
        'image_url': image_url
    }])
    
    df = pd.concat([df, new_car], ignore_index=True)
    save_cars(df)
    return True

# Booking Management Functions
def load_bookings():
    """Load bookings from JSON file"""
    if os.path.exists("bookings.json"):
        try:
            with open("bookings.json", "r") as f:
                bookings_data = json.load(f)
                df = pd.DataFrame(bookings_data)
                if not df.empty:
                    df['pickup_date'] = pd.to_datetime(df['pickup_date']).dt.date
                    df['return_date'] = pd.to_datetime(df['return_date']).dt.date
                return df
        except:
            return pd.DataFrame()
    return pd.DataFrame()

def save_bookings(df):
    """Save bookings to JSON file"""
    df_copy = df.copy()
    if not df_copy.empty:
        df_copy['pickup_date'] = df_copy['pickup_date'].astype(str)
        df_copy['return_date'] = df_copy['return_date'].astype(str)
    
    with open("bookings.json", "w") as f:
        json.dump(df_copy.to_dict('records'), f, indent=2)

def generate_booking_id():
    """Generate unique booking ID"""
    return f"B-{pd.Timestamp.now().strftime('%Y%m%d%H%M%S')}-{np.random.randint(1000, 9999)}"

def add_booking(username, car_id, pickup_date, return_date, total_price, location, image_url, make, model):
    """Add a new booking"""
    df = load_bookings()
    booking_id = generate_booking_id()
    
    new_booking = pd.DataFrame([{
        'booking_id': booking_id,
        'username': username,
        'car_id': car_id,
        'make': make,
        'model': model,
        'pickup_date': pickup_date,
        'return_date': return_date,
        'total_price': total_price,
        'location': location,
        'image_url': image_url,
        'status': 'pending',
        'booking_date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    
    df = pd.concat([df, new_booking], ignore_index=True)
    save_bookings(df)
    return booking_id

def update_booking_status(booking_id, status):
    """Update booking status"""
    df = load_bookings()
    df.loc[df['booking_id'] == booking_id, 'status'] = status
    save_bookings(df)

# Custom CSS
def local_css():
    """Apply custom CSS styles"""
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .admin-header {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .search-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .car-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .car-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .car-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .booking-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #28a745;
    }
    
    .booking-pending {
        border-left-color: #ffc107;
    }
    
    .booking-approved {
        border-left-color: #28a745;
    }
    
    .booking-rejected {
        border-left-color: #dc3545;
    }
    
    .user-info {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #2196f3;
    }
    
    .admin-info {
        background: #ffebee;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #e74c3c;
    }
    
    .stats-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .add-car-form {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Page Configuration
st.set_page_config(
    page_title="Car Rental Management System",
    layout="wide",
    page_icon="🚗",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
local_css()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_type' not in st.session_state:
    st.session_state.user_type = ""

# Login Page
def login_page():
    st.markdown("""
    <div class="main-header">
        <h1>🚗 Car Rental Management System</h1>
        <p>Your trusted partner for car rentals</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.subheader("Login to Your Account")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                auth_result, user_type = authenticate_user(username, password)
                if auth_result:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_type = user_type
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.subheader("Create New Account")
        
        with st.form("register_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_full_name = st.text_input("Full Name")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            user_type = st.selectbox("Account Type", ["user", "admin"])
            register_button = st.form_submit_button("Register", use_container_width=True)
            
            if register_button:
                if not all([new_username, new_email, new_full_name, new_password, confirm_password]):
                    st.error("Please fill in all fields")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    success, message = register_user(new_username, new_password, new_email, new_full_name, user_type)
                    if success:
                        st.success(message)
                        st.info("You can now login with your credentials")
                    else:
                        st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Admin Panel
def admin_panel():
    st.markdown(
        """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">""",
        unsafe_allow_html=True
    )
    
    user_info = get_user_info(st.session_state.username)
    
    # Admin header and logout
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div class="admin-info">
            <h3>👨‍💼 Admin Panel - Welcome, {user_info.get('full_name', st.session_state.username)}!</h3>
            <p><i class="fas fa-envelope"></i> {user_info.get('email', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()
    
    st.markdown("""
    <div class="admin-header">
        <h1>🛠️ Admin Dashboard</h1>
        <p>Manage cars and bookings</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Stats
    cars_df = load_cars()
    bookings_df = load_bookings()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stats-card">
            <h3>🚗 Total Cars</h3>
            <h2>{}</h2>
        </div>
        """.format(len(cars_df)), unsafe_allow_html=True)
    
    with col2:
        available_cars = len(cars_df[cars_df['available'] == True]) if not cars_df.empty else 0
        st.markdown("""
        <div class="stats-card">
            <h3>✅ Available Cars</h3>
            <h2>{}</h2>
        </div>
        """.format(available_cars), unsafe_allow_html=True)
    
    with col3:
        total_bookings = len(bookings_df) if not bookings_df.empty else 0
        st.markdown("""
        <div class="stats-card">
            <h3>📋 Total Bookings</h3>
            <h2>{}</h2>
        </div>
        """.format(total_bookings), unsafe_allow_html=True)
    
    with col4:
        pending_bookings = len(bookings_df[bookings_df['status'] == 'pending']) if not bookings_df.empty else 0
        st.markdown("""
        <div class="stats-card">
            <h3>⏳ Pending Bookings</h3>
            <h2>{}</h2>
        </div>
        """.format(pending_bookings), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Admin Tabs
    tab1, tab2, tab3 = st.tabs(["🚗 Manage Cars", "📋 Manage Bookings", "➕ Add New Car"])
    
    # Manage Cars Tab
    with tab1:
        st.subheader("🚗 Car Fleet Management")
        
        if not cars_df.empty:
            # Car management filters
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_make = st.selectbox("Filter by Make", ['All'] + sorted(cars_df['make'].unique()))
            with col2:
                filter_status = st.selectbox("Filter by Status", ['All', 'Available', 'Not Available'])
            with col3:
                filter_location = st.selectbox("Filter by Location", ['All'] + sorted(cars_df['location'].unique()))
            
            # Apply filters
            filtered_cars = cars_df.copy()
            if filter_make != 'All':
                filtered_cars = filtered_cars[filtered_cars['make'] == filter_make]
            if filter_status == 'Available':
                filtered_cars = filtered_cars[filtered_cars['available'] == True]
            elif filter_status == 'Not Available':
                filtered_cars = filtered_cars[filtered_cars['available'] == False]
            if filter_location != 'All':
                filtered_cars = filtered_cars[filtered_cars['location'] == filter_location]
            
            # Display cars
            for idx, car in filtered_cars.iterrows():
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.image(car['image_url'], width=150)
                
                with col2:
                    st.write(f"**{car['make']} {car['model']}** ({car['year']})")
                    st.write(f"Type: {car['type']} | Seats: {car['seats']}")
                    st.write(f"Price: ${car['price_per_day']}/day | Location: {car['location']}")
                    st.write(f"Status: {'✅ Available' if car['available'] else '❌ Not Available'}")
                
                with col3:
                    if st.button(f"Toggle Status", key=f"toggle_{car['car_id']}"):
                        cars_df.loc[cars_df['car_id'] == car['car_id'], 'available'] = not car['available']
                        save_cars(cars_df)
                        st.rerun()
                    
                    if st.button(f"Remove Car", key=f"remove_{car['car_id']}", type="secondary"):
                        cars_df = cars_df[cars_df['car_id'] != car['car_id']]
                        save_cars(cars_df)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No cars in the fleet. Add some cars to get started!")
    
    # Manage Bookings Tab
    with tab2:
        st.subheader("📋 Booking Management")
        
        if not bookings_df.empty:
            # Booking filters
            col1, col2 = st.columns(2)
            with col1:
                booking_status_filter = st.selectbox("Filter by Status", ['All', 'pending', 'approved', 'rejected'])
            with col2:
                booking_date_filter = st.selectbox("Filter by Date", ['All', 'Today', 'This Week', 'This Month'])
            
            # Apply filters
            filtered_bookings = bookings_df.copy()
            if booking_status_filter != 'All':
                filtered_bookings = filtered_bookings[filtered_bookings['status'] == booking_status_filter]
            
            # Display bookings
            for idx, booking in filtered_bookings.iterrows():
                status_class = f"booking-{booking['status']}"
                
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    st.image(booking['image_url'], width=120)
                
                with col2:
                    st.write(f"**Booking ID:** {booking['booking_id']}")
                    st.write(f"**Customer:** {booking['username']}")
                    st.write(f"**Car:** {booking['make']} {booking['model']}")
                    st.write(f"**Dates:** {booking['pickup_date']} to {booking['return_date']}")
                    st.write(f"**Total:** ${booking['total_price']}")
                    st.write(f"**Status:** {booking['status'].upper()}")
                
                with col3:
                    if booking['status'] == 'pending':
                        if st.button("✅ Approve", key=f"approve_{booking['booking_id']}"):
                            update_booking_status(booking['booking_id'], 'approved')
                            st.rerun()
                        
                        if st.button("❌ Reject", key=f"reject_{booking['booking_id']}"):
                            update_booking_status(booking['booking_id'], 'rejected')
                            st.rerun()
                    else:
                        st.write(f"Status: {booking['status'].upper()}")
                
                st.markdown("---")
        else:
            st.info("No bookings yet.")
    
    # Add New Car Tab
    with tab3:
        st.subheader("➕ Add New Car to Fleet")
        
        st.markdown('<div class="add-car-form">', unsafe_allow_html=True)
        with st.form("add_car_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                make = st.text_input("Make")
                model = st.text_input("Model")
                car_type = st.selectbox("Type", ["Sedan", "SUV", "Hatchback", "Coupe", "Convertible", "Truck"])
                year = st.number_input("Year", min_value=2015, max_value=2025, value=2023)
                price_per_day = st.number_input("Price per Day ($)", min_value=30, max_value=500, value=80)
            
            with col2:
                seats = st.number_input("Number of Seats", min_value=2, max_value=8, value=5)
                transmission = st.selectbox("Transmission", ["Automatic", "Manual"])
                fuel_type = st.selectbox("Fuel Type", ["Gasoline", "Diesel", "Electric", "Hybrid"])
                location = st.selectbox("Location", ["Downtown", "Airport", "North Station", "South Station"])
                image_url = st.text_input("Image URL", value="https://via.placeholder.com/640x480?text=Car+Image")
            
            submit_button = st.form_submit_button("Add Car to Fleet", use_container_width=True)
            
            if submit_button:
                if all([make, model, car_type, year, price_per_day, seats, transmission, fuel_type, location]):
                    if add_car(make, model, car_type, year, price_per_day, seats, transmission, fuel_type, location, image_url):
                        st.success(f"Successfully added {make} {model} to the fleet!")
                        st.rerun()
                    else:
                        st.error("Failed to add car. Please try again.")
                else:
                    st.error("Please fill in all required fields.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# User Panel
def user_panel():
    cars_df = load_cars()
    
    # Font Awesome for icons
    st.markdown(
        """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">""",
        unsafe_allow_html=True
    )
    
    # User info and logout
    user_info = get_user_info(st.session_state.username)
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-info">
            <h3>👋 Welcome, {user_info.get('full_name', st.session_state.username)}!</h3>
            <p><i class="fas fa-envelope"></i> {user_info.get('email', 'N/A')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_type = ""
            st.rerun()
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>🚗 Car Rental System</h1>
        <p>Find and book your perfect car</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User Tabs
    tab1, tab2 = st.tabs(["🔍 Search & Book Cars", "📋 My Bookings"])
    
    # Search & Book Tab
    with tab1:
        # Search Section
        st.markdown("""
        <div class="search-card">
            <h2>🔍 Search Cars</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            search_make = st.selectbox("Make", ['All'] + sorted(cars_df['make'].unique()))
        with col2:
            search_type = st.selectbox("Type", ['All'] + sorted(cars_df['type'].unique()))
        with col3:
            max_price = st.slider("Max Daily Price ($)", 50, 200, 200)
        with col4:
            search_location = st.selectbox("Location", ['All'] + sorted(cars_df['location'].unique()))
        
        # Filter cars
        filtered_df = cars_df[cars_df['available'] == True].copy()  # Only show available cars
        if search_make != 'All':
            filtered_df = filtered_df[filtered_df['make'] == search_make]
        if search_type != 'All':
            filtered_df = filtered_df[filtered_df['type'] == search_type]
        if search_location != 'All':
            filtered_df = filtered_df[filtered_df['location'] == search_location]
        filtered_df = filtered_df[filtered_df['price_per_day'] <= max_price]
        
        # Display Results
        if len(filtered_df) > 0:
            st.subheader(f"🚘 Available Cars ({len(filtered_df)} found)")
            
            # Sort options
            sort_col, _ = st.columns([2, 8])
            with sort_col:
                sort_option = st.selectbox("Sort by", 
                                        ["Price: Low to High", "Price: High to Low", 
                                         "Year: Newest", "Year: Oldest"])
            
            if sort_option == "Price: Low to High":
                filtered_df = filtered_df.sort_values('price_per_day')
            elif sort_option == "Price: High to Low":
                filtered_df = filtered_df.sort_values('price_per_day', ascending=False)
            elif sort_option == "Year: Newest":
                filtered_df = filtered_df.sort_values('year', ascending=False)
            else:
                filtered_df = filtered_df.sort_values('year')
            
            # Display cars in a responsive grid
            cols = st.columns(3)
            for idx, row in filtered_df.iterrows():
                with cols[idx % 3]:
                    with st.container():
                        st.markdown(f"""
                        <div class="car-card">
                            <img src="{row['image_url']}" class="car-image">
                            <div class="car-info">
                                <h3>{row['make']} {row['model']}</h3>
                                <p class="price">${row['price_per_day']} <span>/ day</span></p>
                                <div class="specs">
                                    <p><i class="fas fa-car"></i> {row['type']}</p>
                                    <p><i class="fas fa-calendar-alt"></i> {row['year']}</p>
                                    <p><i class="fas fa-users"></i> {row['seats']} seats</p>
                                    <p><i class="fas fa-gas-pump"></i> {row['fuel_type']}</p>
                                    <p><i class="fas fa-map-marker-alt"></i> {row['location']}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Booking Form
                        with st.expander("📅 Book this car", expanded=False):
                            with st.form(key=f"booking_form_{row['car_id']}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    pickup_date = st.date_input("Pickup Date", 
                                                               min_value=date.today(), 
                                                               key=f"pickup_{row['car_id']}")
                                with col2:
                                    return_date = st.date_input("Return Date", 
                                                              min_value=date.today() + datetime.timedelta(days=1), 
                                                              key=f"return_{row['car_id']}")
                                
                                if st.form_submit_button("Book Now", use_container_width=True):
                                    if return_date <= pickup_date:
                                        st.error("Return date must be after pickup date")
                                    else:
                                        days = (return_date - pickup_date).days
                                        total_price = days * row['price_per_day']
                                        
                                        booking_id = add_booking(
                                            st.session_state.username,
                                            row['car_id'],
                                            pickup_date,
                                            return_date,
                                            total_price,
                                            row['location'],
                                            row['image_url'],
                                            row['make'],
                                            row['model']
                                        )
                                        
                                        st.success(f"""
                                        ✅ Booking request submitted successfully!
                                        Booking ID: {booking_id}
                                        Car: {row['make']} {row['model']}
                                        Total: ${total_price}
                                        Status: Pending admin approval
                                        """)
                        st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No cars match your search criteria. Please adjust your filters.")
    
    # My Bookings Tab
    with tab2:
        st.subheader("📋 My Bookings")
        
        user_bookings = load_bookings()
        if not user_bookings.empty:
            user_bookings = user_bookings[user_bookings['username'] == st.session_state.username]
            
            if not user_bookings.empty:
                # Booking status filter
                status_filter = st.selectbox("Filter by Status", ['All', 'pending', 'approved', 'rejected'])
                
                if status_filter != 'All':
                    display_bookings = user_bookings[user_bookings['status'] == status_filter]
                else:
                    display_bookings = user_bookings
                
                if not display_bookings.empty:
                    for idx, booking in display_bookings.iterrows():
                        status_class = f"booking-{booking['status']}"
                        status_emoji = {"pending": "⏳", "approved": "✅", "rejected": "❌"}
                        
                        st.markdown(f"""
                        <div class="booking-card {status_class}">
                            <div style="display: flex; align-items: center;">
                                <img src="{booking['image_url']}" style="width: 120px; height: 80px; object-fit: cover; border-radius: 8px; margin-right: 1rem;">
                                <div>
                                    <h4>{booking['make']} {booking['model']}</h4>
                                    <p><strong>Status:</strong> {status_emoji.get(booking['status'], '❓')} {booking['status'].upper()}</p>
                                    <p><strong>Booking ID:</strong> {booking['booking_id']}</p>
                                    <p><strong>Dates:</strong> {booking['pickup_date']} to {booking['return_date']}</p>
                                    <p><strong>Total:</strong> ${booking['total_price']}</p>
                                    <p><strong>Location:</strong> {booking['location']}</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(f"No {status_filter} bookings found.")
            else:
                st.info("You haven't made any bookings yet.")
        else:
            st.info("You haven't made any bookings yet.")

# Main execution
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.user_type == "admin":
            admin_panel()
        else:
            user_panel()

if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown("© 2025 Car Rental Management System. All rights reserved.")