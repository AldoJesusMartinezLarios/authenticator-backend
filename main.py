import fastapi
import sqlite3
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

app = fastapi.FastAPI()

origins = [
    "https://8080-aldojesusma-iotdevicesf-a4w6rsh4ddx.ws-us106.gitpod.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar la seguridad con HTTP Bearer
security_bearer = HTTPBearer()

# Modelo Pydantic para la creación de usuarios
class CreateUser(BaseModel):
    username: str
    password: str
    token: str  # Agregamos un campo para el token en el modelo

# Ruta principal que requiere autenticación
@app.get("/", response_model=dict)
def root(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    """
    Ruta principal que requiere autenticación.

    - **credentials**: Credenciales de autorización con un token Bearer.
    """
    token = credentials.credentials

    # Validar el token consultando la base de datos
    if validate_token(token):
        return {"auth": True}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Ruta para autenticarse manualmente
@app.post("/login", response_model=dict)
def manual_login(token: str):
    """
    Ruta para autenticarse manualmente proporcionando un token.

    - **token**: Token de autenticación.
    """
    if validate_token(token):
        return {"auth": True}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

# Ruta para crear un nuevo usuario (no requiere autenticación)
@app.post("/users", response_model=dict)
def create_user(user: CreateUser):
    """
    Ruta para crear un nuevo usuario.

    - **user**: Información del nuevo usuario.
    """
    # Verificar si el usuario ya existe
    with sqlite3.connect("sql/usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(status_code=400, detail="El usuario ya existe")

        # Insertar nuevo usuario en la base de datos con el token proporcionado
        cursor.execute("INSERT INTO users (username, password, token) VALUES (?, ?, ?)",
                       (user.username, user.password, user.token))  
        conn.commit()
    return {"message": "Usuario creado correctamente"}

# Función para validar tokens (puedes implementar tu lógica específica aquí)
def validate_token(token: str):
    with sqlite3.connect("sql/usuarios.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE token = ?", (token,))
        user = cursor.fetchone()
        return user is not None

# Función para generar tokens (puedes implementar tu lógica específica aquí)
def generate_token():
    import secrets
    return secrets.token_hex(16)