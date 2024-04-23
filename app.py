import streamlit as st
from tools.sha1 import SHA1
from enviar_mensaje import enviar

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    return "No hay inverso"

st.set_page_config(
    page_title="Envío de mensajes",
    page_icon="🔒",
    layout="wide"
)
st.title('Envío de mensajes encriptados')

col1, col2 = st.columns(2)
with col1:
    st.subheader("Encriptar mensaje")
    mensaje = st.text_input("Escribe tu mensaje aquí")
    if st.button("Enviar mensaje"):
        message_encoded = [ord(ch) for ch in mensaje]
        cipher_text = [pow(ch, 29, 13*11) for ch in message_encoded]
        t = ""
        for i in cipher_text:
            t += chr(i)
        st.write(f"Mensaje encriptado: {t}")
        
        st.success("Mensaje enviado correctamente")
        st.write(f"Mensaje encriptado: {cipher_text}")
    
with col2:
    st.subheader("Desencriptar mensaje")
    k = []
    for i in t:
        k.append(ord(i))
    message_enc = [pow(ch, 29, 13*11) for ch in k]
    message = "".join(chr(ch) for ch in message_enc)
    st.write(f"Mensaje desencriptado: {message}")
    