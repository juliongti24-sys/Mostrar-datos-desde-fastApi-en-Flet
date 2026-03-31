import requests

# URL de tu backend en FastAPI
BASE_URL = "http://localhost:8000/productos"

# LISTAR PRODUCTOS
def list_products(limit: int = 100, offset: int = 0):
    try:
        response = requests.get(f"{BASE_URL}/?limit={limit}&offset={offset}")
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión al listar: {e}")
        return {"items": [], "total": 0}

# OBTENER UN PRODUCTO POR ID
def get_product(product_id: str):
    try:
        response = requests.get(f"{BASE_URL}/{product_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Error al obtener el producto: {e}")

# CREAR PRODUCTO
def create_product(producto: dict):
    try:
        response = requests.post(f"{BASE_URL}/", json=producto)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error del servidor: {err.response.text}")
    except Exception as e:
        raise Exception(f"Error al conectar con la API: {e}")

# ACTUALIZAR PRODUCTO
def update_product(product_id: str, producto: dict):
    try:
        response = requests.put(f"{BASE_URL}/{product_id}", json=producto)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Error del servidor: {err.response.text}")
    except Exception as e:
        raise Exception(f"Error al actualizar: {e}")

# ELIMINAR PRODUCTO
def delete_product(product_id: str):
    try:
        response = requests.delete(f"{BASE_URL}/{product_id}")
        response.raise_for_status()
        # Suele devolver None o el dict del producto eliminado, dependiendo de tu backend
        return True 
    except Exception as e:
        raise Exception(f"Error al eliminar: {e}")