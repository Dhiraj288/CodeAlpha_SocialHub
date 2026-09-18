# SocialHub

SocialHub is a full-stack social media web application built using Django as part of my CodeAlpha Full Stack Development Internship.

The platform allows users to create accounts, build profiles, share text and image posts, interact through likes and comments, follow other users, search for people, and use a responsive light/dark interface.

## Features

- User Registration and Login
- User Profiles
- Profile Picture and Bio
- Create Text and Image Posts
- Edit and Delete Posts
- Like and Unlike Posts
- Add and Delete Comments
- Follow and Unfollow Users
- Followers and Following Count
- Search Users
- Image Preview Before Upload
- Dark and Light Mode
- Responsive User Interface
- Secure POST Actions with CSRF Protection

## Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML
- CSS
- JavaScript
- Django Template Language

### Database
- SQLite

### Other
- Pillow for image handling
- Git and GitHub for version control

## Project Structure

```text
SocialMedia/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── social/
│   ├── migrations/
│   ├── static/
│   │   └── social/
│   │       ├── style.css
│   │       └── script.js
│   │
│   ├── templates/
│   │   └── social/
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── feed.html
│   │       ├── create_post.html
│   │       ├── edit_post.html
│   │       ├── profile.html
│   │       ├── edit_profile.html
│   │       ├── user_profile.html
│   │       └── search_users.html
│   │
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Dhiraj288/CodeAlpha_SocialHub.git
```

Move into the project directory:

```bash
cd CodeAlpha_SocialHub
```

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

## Main Functionalities

Users can register and log in to their accounts, create and manage posts, upload images, interact with posts using likes and comments, discover other users through search, and follow or unfollow them.

Users can also customize their profiles with a profile picture and bio.

## Security

SocialHub uses Django's built-in authentication system and CSRF protection. Important state-changing actions such as likes, follows, deletions, and logout use POST requests with CSRF tokens.

## Internship

This project was developed as part of the **CodeAlpha Full Stack Development Internship**.

## Developer

**Dhiraj Kumar Verma**

GitHub: Dhiraj288

## Repository

CodeAlpha_SocialHub