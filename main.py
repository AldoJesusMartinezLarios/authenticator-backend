import hashlib
import sqlite3
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

security = HTTPBasic()

def get_db_connection():
    connection = sqlite3.connect("sql/usuarios.db")
    return connection

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
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta para obtener el token del usuario
    cursor.execute("SELECT token FROM usuarios WHERE username=? AND password=?", (email, password))
    result = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    connection.close()

    if result:
        return {"token": result[0]}
    else:
        raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

# Endpoint para visualizar todos los usuarios
@app.get("/usuarios")
def get_all_users(token: str = Depends(validate_user)):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta para obtener todos los usuarios
    cursor.execute("SELECT username FROM usuarios")
    users = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    connection.close()

    return {"usuarios": users}

# Endpoint para crear un nuevo usuario
@app.post("/usuarios")
def create_user(username: str, password: str, token: str = Depends(validate_user)):
    # Puedes agregar lógica adicional para validar la información del usuario antes de insertarla en la base de datos

    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Insertar nuevo usuario
    cursor.execute("INSERT INTO usuarios (username, password, token) VALUES (?, ?, ?)", (username, password, "nuevo_token"))
    connection.commit()

    # Cerrar la conexión a la base de datos
    connection.close()

    return {"message": f"Usuario {username} creado correctamente"}

# Endpoint para actualizar un usuario
@app.put("/usuarios/{username}")
def update_user(username: str, new_password: str, token: str = Depends(validate_user)):
    # Puedes agregar lógica adicional para validar la información del usuario antes de actualizarla en la base de datos

    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Actualizar la contraseña del usuario
    cursor.execute("UPDATE usuarios SET password = ? WHERE username = ?", (new_password, username))
    connection.commit()

    # Cerrar la conexión a la base de datos
    connection.close()

    return {"message": f"Contraseña del usuario {username} actualizada"}

# Endpoint para visualizar un usuario específico
@app.get("/usuarios/{username}")
def get_user(username: str, token: str = Depends(validate_user)):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Consulta para obtener información de un usuario específico
    cursor.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    user = cursor.fetchone()

    # Cerrar la conexión a la base de datos
    connection.close()

    if user:
        return {"usuario": user}
    else:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

# Endpoint para eliminar un usuario
@app.delete("/usuarios/{username}")
def delete_user(username: str, token: str = Depends(validate_user)):
    # Puedes agregar lógica adicional para validar que el usuario tenga los permisos necesarios antes de eliminarlo

    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()

    # Eliminar el usuario
    cursor.execute("DELETE FROM usuarios WHERE username=?", (username,))
    connection.commit()

    # Cerrar la conexión a la base de datos
    connection.close()

    return {"message": f"Usuario {username} eliminado correctamente"}
