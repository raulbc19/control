import streamlit as st

st.title("Control de Caja - Fondo Común")

# Definir los tipos de billetes/monedas
denominaciones = [500, 200, 100, 50, 20, 10, 5, 2, 1, 0.50, 0.20, 0.10, 0.05, 0.02, 0.01]

st.subheader("Indica cuántas unidades hay de cada valor:")

total = 0
cantidades = {}

# Crear un input numérico para cada denominación
for d in denominaciones:
    # Si la denominación es mayor a 1, tratamos como billete/moneda entera, si es menor, como moneda
    label = f"Billetes de {d} €" if d >= 5 else f"Monedas de {d} €" if d >= 1 else f"Monedas de {int(d*100)} céntimos"
    
    # Usamos session_state o inputs directos
    cantidades[d] = st.number_input(label, min_value=0, value=0, step=1)
    total += cantidades[d] * d

st.divider()
st.metric(label="Dinero Total en la Caja", value=f"{total:.2f} €")
