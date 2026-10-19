# Finora – Expense Tracker

Finora is a web-based expense tracking application built using Python and Django. It helps users manage their daily expenses, track income, organize spending by category, and monitor their monthly budget through a simple dashboard.

## Features

- **User Authentication:** User registration, login, logout, and password reset pages.
- **Expense Management:** Add, view, update, and delete expenses.
- **Category Management:** Organize expenses into different categories.
- **Income Management:** Record and manage income details.
- **Dashboard:** View total expenses, monthly expenses, and category summaries.
- **Monthly Budget:** Set and monitor a monthly budget.
- **Expense Reports:** View expense summaries and monthly charts.
- **Responsive Design:** Simple and user-friendly interface.

## Technologies Used

- Python
- Django
- HTML5
- CSS3
- JavaScript
- PostgreSQL
- Chart.js

## Project Structure

```text
Finora/
├── expense_tracker/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── home/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── base.html
├── manage.py
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/finora-expense-tracker.git
cd finora-expense-tracker
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

If you have a `requirements.txt` file:

```bash
pip install -r requirements.txt
```

Otherwise, install Django and the database driver required by your project.

### 5. Configure the database

Update the database settings in `expense_tracker/settings.py` to match your local database configuration.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

`http://127.0.0.1:8000/`

## Learning Outcomes

- Developed a web application using Django's MVT architecture.
- Practiced database models and relationships.
- Implemented user authentication and session management.
- Built CRUD operations for expenses and income.
- Created dashboard summaries and visual reports.
- Practiced frontend development and Django template integration.

## Future Improvements

- Export expense reports to PDF or Excel.
- Add email notifications for budget limits.
- Improve mobile responsiveness.
- Add advanced expense filtering and analytics.

## Author

**Rekhapalli Uma Satya Santosh**
- GitHub: [RekhapalliUmaSatyaSantosh](https://github.com/RekhapalliUmaSatyaSantosh)
- LinkedIn: [uma-satya-santosh-rekhapalli](https://linkedin.com/in/uma-satya-santosh-rekhapalli/)

---

This project was developed for learning and practicing Python full-stack web development.
