# Virtual Bank

## Installation
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in the values
3. Run `docker-compose up -d` to raise the database container
4. Run `pip3 install -r requirements.txt` to install the dependencies
5. Run `python manage.py migrate` to run the migrations
6. Run `python manage.py runserver` to run the server
7. Go to <a>http://localhost:8000 to see the server running

## Database migrations
1. Run `python manage.py makemigrations` to create a new migration file
2. Run `python manage.py migrate` to apply the migrations
3. Run `python manage.py showmigrations` to see the migration history
4. Run `python manage.py migrate <app_name> zero` to revert all migrations of an app
5. Run `python manage.py migrate zero` to revert all migrations
6. 