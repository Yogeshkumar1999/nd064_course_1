from python:2.7
LABEL maintainer="Yogesh Kumar"
expose 3111
copy . /app
workdir /app
run pip install -r requirments.txt
run python init_db.py
