Setup Python venv, install requirements.txt.

python manage.py migrate

python manage.py createsuperuser (optional) to manage via admin

python manage.py runserver

Visit http://127.0.0.1:8000/:

Register a new user at /register/

Login at /login/

Create a new post at /posts/new/ (tags accept comma-separated values)

View posts, click to view details, add comments

Try editing / deleting posts only as the author

Test tags: clicking a tag shows posts for that tag at /tags/<tag>/

Use search via header form to search content, title, or tags at /search/?q=term
