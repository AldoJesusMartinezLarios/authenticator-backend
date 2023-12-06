# AUTHENTIFICATOR BACKEND
Api rest para poder autentificar

SQLite3, FastAPI, HTTPAuthentificator

gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
