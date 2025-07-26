# Car Rental Management System

A comprehensive car rental management system built with Streamlit that features separate admin and user panels.

## Features

### Admin Panel
- **Dashboard**: View statistics about cars, bookings, and system overview
- **Car Management**: Add, remove, and toggle availability of cars in the fleet
- **Booking Management**: Approve or reject customer booking requests
- **Real-time Updates**: All changes are saved and reflected immediately

### User Panel
- **Car Search**: Filter cars by make, type, location, and price
- **Booking System**: Book cars with date selection and automatic pricing
- **Booking Tracking**: View all bookings with status updates
- **User Authentication**: Secure login and registration system

## Installation

1. Clone or download the project files
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

### First Time Setup

1. Run the application using `streamlit run app.py`
2. Navigate to the registration tab
3. Create an admin account by selecting "admin" as the account type
4. Create user accounts by selecting "user" as the account type

### Admin Access

1. Login with an admin account
2. Access the admin dashboard to:
   - View system statistics
   - Manage the car fleet
   - Approve/reject booking requests
   - Add new cars to the system

### User Access

1. Login with a user account
2. Search and filter available cars
3. Book cars by selecting dates
4. Track your bookings and their approval status

## System Architecture

### Data Storage
- User data is stored in `users.json`
- Car data is stored in `cars.json`
- Booking data is stored in `bookings.json`

### User Roles
- **Admin**: Full access to manage cars and bookings
- **User**: Can search cars and make booking requests

### Booking Workflow
1. User searches for available cars
2. User selects dates and submits booking request
3. Booking status is set to "pending"
4. Admin reviews and approves/rejects the booking
5. User can view updated booking status

## File Structure

```
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── users.json         # User data (auto-generated)
├── cars.json          # Car data (auto-generated)
└── bookings.json      # Booking data (auto-generated)
```

## Features Included

### Authentication System
- Secure password hashing using SHA-256
- User registration with email validation
- Session management
- Role-based access control

### Car Management
- Add new cars to the fleet
- Toggle car availability
- Remove cars from the fleet
- Filter cars by various criteria

### Booking System
- Date-based booking
- Automatic price calculation
- Booking status tracking
- Admin approval workflow

### User Interface
- Responsive design
- Modern CSS styling
- Font Awesome icons
- Intuitive navigation

## Sample Data

The system comes with 15 sample cars including:
- Various makes: Toyota, Honda, BMW, Mercedes, Tesla, etc.
- Different types: Sedan, SUV, Hatchback
- Price range: $55-$180 per day
- Multiple locations: Downtown, Airport

## Default Admin Account

For testing purposes, you can create an admin account during registration by:
1. Going to the Register tab
2. Filling in the required information
3. Selecting "admin" from the Account Type dropdown

## Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Hashlib**: Password hashing (built-in)
- **JSON**: Data storage (built-in)
- **Datetime**: Date handling (built-in)

### Security Features
- Password hashing for secure storage
- Session-based authentication
- Role-based access control
- Input validation

## Customization

### Adding More Car Types
Edit the `car_type` selectbox options in the admin panel's "Add New Car" form.

### Modifying Locations
Update the `location` selectbox options in both the car addition form and search filters.

### Styling Changes
Modify the CSS in the `local_css()` function to customize the appearance.

## Troubleshooting

### Common Issues

1. **Application won't start**: Make sure all dependencies are installed
2. **Data not persisting**: Check file permissions in the application directory
3. **Login issues**: Verify username and password are correct

### Data Reset

To reset all data, simply delete the JSON files:
- `users.json`
- `cars.json`
- `bookings.json`

The application will regenerate sample data on the next run.

## Support

For issues or questions, please check the application logs in the Streamlit interface or review the console output for error messages.
