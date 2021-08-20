from python:2.7
copy ./techtrends /app
workdir /app
run pip install -r requirements.txt
run python init_db.py
expose 3111
cmd ["python", "app.py"]
