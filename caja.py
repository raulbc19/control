import streamlit as st
import requests
from datetime import datetime
import pytz

st.title("Control de Caja - Fondo Común")

# --- 1. CONFIGURACIÓN ---
BIN_ID = st.secrets["BIN_ID"]
API_KEY = st.secrets["API_KEY"]
URL = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
HEADERS = {
    'X-Master-Key': API_KEY,
    'Content-Type': 'application/json'
}

denominaciones = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

# --- 2. FUNCIONES ---
def cargar_datos():
    try:
        respuesta = requests.get(URL, headers=HEADERS)
        return respuesta.json()['record']
    except:
        return {} 

def guardar_datos(datos):
    requests.put(URL, json=datos, headers=HEADERS)
    st.success("¡Datos guardados correctamente en la nube!")

# --- 3. INTERFAZ ---
if 'base_datos' not in st.session_state:
    st.session_state.base_datos = cargar_datos()

st.subheader("Indica cuántas unidades hay de cada valor:")

total = 0
nuevas_cantidades = {}

for d in denominaciones:
    clave = str(d)
    valor_guardado = st.session_state.base_datos.get(clave, 0)
    
    label = f"Billetes de {d} €" if d >= 5 else f"Monedas de {d} €" if d >= 1 else f"Monedas de {int(d*100)} céntimos"
    
    nuevas_cantidades[clave] = st.number_input(label, min_value=0, value=int(valor_guardado), step=1)
    total += nuevas_cantidades[clave] * d

st.divider()

# --- NUEVO: MOSTRAR FECHA Y TOTAL ---
st.metric(label="Dinero Total en la Caja", value=f"{total:.2f} €")

# Rescatamos la fecha de la base de datos (si no hay, pone "Aún no se ha guardado")
fecha_mod = st.session_state.base_datos.get("ultima_modificacion", "Aún no se ha guardado")
st.caption(f"🕒 **Última vez modificado:** {fecha_mod}")

# Botón para guardar
if st.button("Guardar Cambios"):
    # 1. Calculamos la fecha y hora actual en España
    zona_horaria = pytz.timezone("Europe/Madrid") 
    ahora = datetime.now(zona_horaria)
    fecha_texto = ahora.strftime("%d/%m/%Y a las %H:%M")
    
    # 2. Metemos la fecha en el mismo paquete de datos que las cantidades
    nuevas_cantidades["ultima_modificacion"] = fecha_texto
    
    # 3. Guardamos todo
    guardar_datos(nuevas_cantidades)
    
    # 4. Actualizamos la pantalla al instante para que muestre la nueva fecha
    st.session_state.base_datos = nuevas_cantidades
    st.rerun()
