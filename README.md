# Virtual Bank
REST API for a virtual bank application created with [Django](https://www.djangoproject.com/), [Django REST Framework](https://www.django-rest-framework.org/) and [PostgreSQL](https://www.postgresql.org/).
<br>
<br>
It has the following endpoints:
- `POST /api/v1/accounts` - Create a new account
- `GET /api/v1/accounts` - Get all accounts
- `GET /api/v1/accounts/<id>` - Get a specific account
- `PUT /api/v1/accounts/<id>` - Update a whole account
- `PATCH /api/v1/accounts/<id>` - Update specific fields of an account
- `DELETE /api/v1/accounts/<id>` - Delete an account
- `GET /api/v1/accounts/<id>/balance` - Get the balance of an account
- `POST /api/v1/accounts/<id>/deposit` - Deposit money to an account
- `GET /api/v1/accounts/<id>/withdraw_code` - Get a withdraw code for an account
- `POST /api/v1/accounts/<id>/withdraw` - Withdraw money from an account

## Installation
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the values
3. Run `docker-compose up -d` to raise the database container
4. Run `python3 -m venv venv`
5. Run `source venv/bin/activate`
6. Run `pip3 install -r requirements.txt` to install the dependencies
7. Run `python3 manage.py migrate` to run the migrations
8. Run `python3 manage.py runserver` to run the server
9. **[OPTIONAL]** Run `uwsgi --http :8000 --module django_app.wsgi` if you want to run the project with **uWSGI**
10. **[OPTIONAL]** Run `gunicorn django_app.wsgi ` if you want to run the project with **Gunicorn**
11. Go to <a>http://localhost:8000 to see the server running

## Database migrations
1. Run `python3 manage.py makemigrations` to create a new migration file
2. Run `python3 manage.py migrate` to apply the migrations
3. Run `python3 manage.py showmigrations` to see the migration history
4. Run `python3 manage.py migrate <app_name> zero` to revert all migrations of an app
5. Run `python3 manage.py migrate zero` to revert all migrations