import streamlit as st

# Función para obtener el inverso modular
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return "No hay inverso"

# Configuración de la página
st.set_page_config(
    page_title="Envío de mensajes",
    page_icon="🔒",
    layout="wide"
)
st.image('Logo_del_ITESM.svg', width=100)
# Título de la aplicación
st.title('Envío de mensajes encriptados')

# Inicializar el registro de mensajes en la sesión, si no está presente
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

# Definir las columnas
col1, col2 = st.columns(2)

# Sección para encriptar mensajes
with col1:
    st.subheader("Encriptar mensaje")
    mensaje = st.text_input("Escribe tu mensaje aquí")
    if st.button("Enviar mensaje"):
        message_encoded = [ord(ch) for ch in mensaje]
        cipher_text = [pow(ch, 29, 13*11) for ch in message_encoded]
        t = "".join(chr(i) for i in cipher_text)  # Convertir lista a texto
        st.session_state.mensajes.append(t)
        st.success("Mensaje enviado correctamente")

# Sección para desencriptar mensajes
with col2:
    st.subheader("Desencriptar mensaje")
    if st.session_state.mensajes:
        # Desencriptar el último mensaje enviado
        k = [ord(i) for i in st.session_state.mensajes[-1]]
        message_enc = [pow(ch, 29, 13*11) for ch in k]
        message = "".join(chr(ch) for ch in message_enc)
        st.subheader(mensaje)
    else:
        st.warning("No hay mensajes para desencriptar.")

col3, col4, col5 = st.columns(3)
with col3:
    pass

with col4:
    st.subheader("Registro de mensajes")
    st.table(st.session_state.mensajes)
    
with col5:
    pass
