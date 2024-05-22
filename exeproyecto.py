import streamlit as st
from streamlit_ace import st_ace
import psycopg2
import hashlib
from psycopg2 import sql
import contextlib
import io
from portaladmin import PanelAdmin
from cryptography.fernet import Fernet
import matplotlib.pyplot as plt
import base64


CLAVE_MAESTRA = b'wpmvV7vMlE8FVwVwFhBNZ1R1NUVTxk9sL7m_KDQX8RY='

def obtener_conexion_db():
    return psycopg2.connect(
        host="db",
        port="5432",
        database="proyecto_cripto",
        user="admin",
        password="cripto"
    )

def run_and_capture_output(code):
    output_buffer = io.StringIO()
    error_buffer = io.StringIO()
    image_buffer = io.BytesIO()
    plt.figure()
    try:
        with contextlib.redirect_stdout(output_buffer):
            with contextlib.redirect_stderr(error_buffer):
                exec(code)
    except SyntaxError as e:
        return f"SyntaxError: {e.text.strip()}\nError on line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"Error: {str(e)}"
    plt.savefig(image_buffer, format='png')
    image_buffer.seek(0)
    plt.close()

    output = output_buffer.getvalue()
    error_output = error_buffer.getvalue()
    if error_output:
        return error_output

    output_buffer.close()
    error_buffer.close()

    image_base64 = base64.b64encode(image_buffer.read()).decode('utf-8')
    image_buffer.close()
    if image_base64:
        st.image(f"data:image/png;base64,{image_base64}")

    return output

def validar_usuario(usuario, contraseña_ingresada):
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    usuario = usuario.strip().lower()
    contraseña_ingresada = contraseña_ingresada.strip().lower()
    contraseña_hash = hashlib.sha256(contraseña_ingresada.encode('utf-8')).hexdigest()
    query = sql.SQL("SELECT permiso FROM usuarios WHERE usuario = %s AND contraseña = %s")
    cursor.execute(query, (usuario, contraseña_hash,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        permiso = result[0].split(',')
        return True, [perm.lower() for perm in permiso]
    return False, []

def obtener_codigo_almacenado():
    try:
        conn = obtener_conexion_db()
        cursor = conn.cursor()
        query = sql.SQL("SELECT codigo FROM codigo_guardado WHERE id = 1")
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            codigo_cifrado = result[0]
            fernet = Fernet(CLAVE_MAESTRA)
            codigo_descifrado = fernet.decrypt(codigo_cifrado.encode()).decode()
            return codigo_descifrado
        else:
            return "print('No code found!')"
    except Exception as e:
        st.error(f"Error al obtener y descifrar el código: {e}")
        return "print('Error al obtener y descifrar el código')"

def guardar_codigo(codigo):
    try:
        fernet = Fernet(CLAVE_MAESTRA)
        codigo_cifrado = fernet.encrypt(codigo.encode())

        conn = obtener_conexion_db()
        cursor = conn.cursor()
        query = sql.SQL("UPDATE codigo_guardado SET codigo = {} WHERE id = 1").format(sql.Literal(codigo_cifrado.decode()))
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Código guardado con éxito!")
    except Exception as e:
        st.error(f"Error al guardar el código: {e}")

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
        page_icon="resources/dmx.jpg",
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
        
        if 'todas' in st.session_state.permiso or 'todo' in st.session_state.permiso:
            opciones_sidebar = list(herramientas_disponibles.keys())
        else:
            opciones_sidebar = [herramienta for herramienta in herramientas_disponibles if herramienta.lower() in st.session_state.permiso]
        
        if not opciones_sidebar:
            st.error("No tiene permisos para acceder a ninguna herramienta.")
        else:
            opcion_seleccionada = st.sidebar.selectbox("Seleccione una herramienta", opciones_sidebar)

            if opcion_seleccionada == "Editar":
                st.image('resources/dmx.jpg', width=100)
                st.subheader('Editar')
                codigo_actual = obtener_codigo_almacenado()
                editado = st_ace(value=codigo_actual, language='python', key='editor')
                if st.button("Guardar código"):
                    guardar_codigo(editado)

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
