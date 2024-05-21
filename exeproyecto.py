import streamlit as st
from streamlit_ace import st_ace
import psycopg2
import hashlib
from psycopg2 import sql
import contextlib
import io
from portaladmin import PanelAdmin

def obtener_conexion_db():
    return psycopg2.connect(
        host="db",
        port="5432",
        database="proyecto_cripto",
        user="admin",
        password="cripto"
    )

def run_and_capture_output(code):
    #Si es imagen se puede ver una imagen tambien
    #Imágen siendo gráfico o algo similar
    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer):
        exec(code)
    output = output_buffer.getvalue()
    output_buffer.close()
    return output

def validar_usuario(usuario ,contraseña_ingresada):
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    usuario = usuario.strip().lower()
    contraseña_ingresada = contraseña_ingresada.strip().lower()
    contraseña_hash = hashlib.sha256(contraseña_ingresada.encode('utf-8')).hexdigest()
    query = sql.SQL("SELECT permiso FROM usuarios WHERE usuario = %s AND contraseña = %s")
    cursor.execute(query, (usuario,contraseña_hash,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        permiso = result[0].split(',')
        return True, [perm.lower() for perm in permiso]
        return False, []

def obtener_codigo_almacenado():
    #desencriptar con el hash de la combinación de contraseñas
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    query = sql.SQL("SELECT codigo FROM codigo_guardado")
    cursor.execute(query, (1,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "print('No code found!')"

def guardar_codigo(codigo):
    #Guardar el código encriptado con el hash de la combinación de contraseñas
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    query = sql.SQL("UPDATE codigo_guardado SET codigo = {}").format(sql.Literal(codigo))
    cursor.execute(query, (codigo,))
    conn.commit()
    cursor.close()
    conn.close()

def mostrar_formulario_inicio_sesion():
    st.image('resources/dmx.jpg', width=100)
    usuario = st.text_input("Usuario", key="usuario")
    contraseña_ingresada = st.text_input("Contraseña", type="password", key="contraseña")
    if st.button("Iniciar sesión"):
        usuario_valido, permiso = validar_usuario(usuario,contraseña_ingresada)
        if usuario_valido:
            st.session_state.usuario_autenticado = True
            st.session_state.permiso = permiso
            st.rerun()
        else:
            st.error("Error de inicio de sesión. Por favor, verifica tus credenciales.")

def main():
    st.set_page_config(
        page_title="Envío de mensajes",
        page_icon="🔒",
        layout="wide"
    )
    if "usuario_autenticado" not in st.session_state:
        st.session_state.usuario_autenticado = False

    if not st.session_state.usuario_autenticado:
        mostrar_formulario_inicio_sesion()
    else:
        herramientas_disponibles = {
            "Editar": "Editar",
            "Correr": "Correr",
            "Admin Portal": "Admin Portal"
        }
        
        if 'todo' in st.session_state.permiso:
            opciones_sidebar = list(herramientas_disponibles.keys())
        else:
            opciones_sidebar = [herramienta for herramienta in herramientas_disponibles if herramienta.lower() in st.session_state.permiso]
        
        opcion_seleccionada = st.sidebar.radio("Seleccione una herramienta", opciones_sidebar)

        if opcion_seleccionada == "Editar":
            st.image('resources/dmx.jpg', width=100)
            st.subheader('Editar')
            codigo_actual = obtener_codigo_almacenado()
            editado = st_ace(value=codigo_actual, language='python', key='editor')
            if st.button("Guardar código"):
                guardar_codigo(editado)
                st.success("Código guardado con éxito!")

        elif opcion_seleccionada == "Correr":
            st.image('resources/dmx.jpg', width=100)
            st.subheader('Correr')
            codigo_actual = obtener_codigo_almacenado()
            if st.button("Correr código"):
                output = run_and_capture_output(codigo_actual)
                st.write(f"Output: {output}")

        elif opcion_seleccionada == "Admin Portal":
            panel_admin = PanelAdmin()
            panel_admin.main()

if __name__ == "__main__":
    main()
