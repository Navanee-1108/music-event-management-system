🎵 Music Event Management System

A full-stack Music Event Management System built using Django.
This web application allows users to explore events, view event details, and book events online.
It also includes a custom admin dashboard for managing event services, users, and bookings efficiently.

---

🚀 Features

👤 User Features

- User Registration & Login Authentication
- Browse Available Events
- View Event Details
- Book Events Online
- Duplicate Booking Prevention
- Booking Confirmation Email
- Contact Form with Email Notification
- View Personal Bookings (My Bookings Page)

---

🛠 Admin Features

- Custom Admin Dashboard
- Add New Event Services
- Edit Existing Services
- Activate / Deactivate Event Services
- Manage Customer Bookings
- Accept Customer Bookings
- View Registered Users

---

🛠 Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- SQLite
- Django Authentication System

---

📁 Project Structure

music-event-management-system

├── event_management        # Django project settings
├── events                  # Main Django application
│   ├── migrations
│   ├── static
│   ├── templates
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── media                   # Uploaded event images
├── screenshots             # Screenshots used in README
│   ├── home.png
│   ├── booking.png
│   └── admin.png
│
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore

---



## 📸 Screenshots

### Home Page
![Home](screenshots/home.png)

### Event Booking Page
![Booking](screenshots/booking.png)

### Admin Dashboard
![Admin](screenshots/admin.png)

---

⚙ Installation & Setup

Clone the repository

git clone https://github.com/Navanee-1108/music-event-management-system.git

Navigate to the project folder

cd music-event-management-system

Install dependencies

pip install -r requirements.txt

Run migrations

python manage.py migrate

Start development server

python manage.py runserver

Open in browser

http://127.0.0.1:8000

---

👨‍💻 Author

Developed by Navaneethakrishnan

GitHub:
https://github.com/Navanee-1108