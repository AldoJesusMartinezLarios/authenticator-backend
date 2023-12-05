import hashlib
import sqlite3
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic
from fastapi.security import HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

# Endpoint principal
@app.get("/")
def read_root():
    return {"message": "¡Bienvenido al sistema de autenticación!"}

# Endpoint para generar tokens
@app.get("/token")
def validate_user(credentials: HTTPBasicCredentials = Depends(security)):
    email = credentials.username
    password_b = hashlib.md5(credentials.password.encode())
    password = password_b.hexdigest()

    # Conexión a la base de datos
    connection = sqlite3.connect("sql/usuarios.db")
    cursor = connection.cursor()

    # Consulta para obtener el token del usuario
    cursor.execute("SELECT token FROM usuarios WHERE username=? AND password=?", (email, password))
    result = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    connection.close()

    if result:
        return {"token": result[0]}
    else:
        return {"error": "Usuario o contraseña incorrectos"}