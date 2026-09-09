import streamlit as st
import requests

st.title("Control de Caja - Tesorería JMM")

# --- 1. CONFIGURACIÓN DE LA BASE DE DATOS ---
# Leemos las claves secretas que configuramos en Streamlit
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    'X-Master-Key': API_KEY,
    'Content-Type': 'application/json'
}

denominaciones = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

# --- 2. FUNCIONES PARA CARGAR Y GUARDAR ---
def cargar_datos():
    try:
        respuesta = requests.get(URL, headers=HEADERS)
        return respuesta.json()['record']
    except:
        return {} # Si falla, empezamos de cero

def guardar_datos(nuevos_datos):
    requests.put(URL, json=nuevos_datos, headers=HEADERS)
    st.success("¡Datos guardados correctamente en la nube!")

# --- 3. INTERFAZ DE LA APP ---
# Cargamos los datos solo la primera vez que se abre la página
if 'cantidades' not in st.session_state:
    st.session_state.cantidades = cargar_datos()

st.subheader("Indica cuántas unidades hay de cada valor:")

total = 0
nuevas_cantidades = {}

# Generar las cajas de número
for d in denominaciones:
    clave = str(d)
    # Buscamos cuánto había guardado (o 0 si no había nada)
    valor_guardado = st.session_state.cantidades.get(clave, 0)
    
    label = f"Billetes de {d} €" if d >= 5 else f"Monedas de {d} €" if d >= 1 else f"Monedas de {int(d*100)} céntimos"
    
    nuevas_cantidades[clave] = st.number_input(label, min_value=0, value=valor_guardado, step=1)
    total += nuevas_cantidades[clave] * d

st.divider()
st.metric(label="Dinero Total en la Caja", value=f"{total:.2f} €")

# Botón para guardar
if st.button("Guardar Cambios"):
    guardar_datos(nuevas_cantidades)
    st.session_state.cantidades = nuevas_cantidades
