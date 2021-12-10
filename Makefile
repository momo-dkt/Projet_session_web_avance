export FLASK_APP= app/app.py
export FLASK_ENV=development
export FLASK_RUN_PORT=5000

run:
	flask run --host=0.0.0.0