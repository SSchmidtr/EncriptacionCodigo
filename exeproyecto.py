import streamlit as st
from streamlit_ace import st_ace
import psycopg2
import hashlib
from psycopg2 import sql

# Conexión a la base de datos
def obtener_conexion_db():
    return psycopg2.connect(
        host="db",
        port="5432",
        database="proyecto_cripto",
        user="admin",
        password="cripto"
    )

# Validación del usuario
def validar_usuario(contraseña_ingresada):
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    contraseña_hash = hashlib.sha256(contraseña_ingresada.encode('utf-8')).hexdigest()
    query = sql.SQL("SELECT permiso FROM usuarios WHERE contraseña = %s")
    cursor.execute(query, (contraseña_hash,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        permiso = result[0].split(',')
        return True, permiso
    else:
        return False, []

def obtener_codigo_almacenado():
    conn = obtener_conexion_db()
    cursor = conn.cursor()
    query = sql.SQL("SELECT codigo FROM codigo_guardado")
    cursor.execute(query, (1,))  # Suponiendo que el usuario_id es 1 por ahora
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else "print('No code found!')"


# Almacenamiento del código
def guardar_codigo(codigo):
    conn = obtener_conexion_db()
    cursor = conn.cursor()

    # Uso adecuado de sql.SQL con formateo de argumentos
    query = sql.SQL("UPDATE codigo_guardado SET codigo = %s")

    # Pasar ambos argumentos en una tupla para el método `execute`
    cursor.execute(query, (codigo, 1))  # Almacenar para el usuario con ID 1

    # Confirmar cambios en la base de datos
    conn.commit()
    cursor.close()
    conn.close()


# Formulario de inicio de sesión
def mostrar_formulario_inicio_sesion():
    st.image('resources/Logo_del_ITESM.svg', width=100)
    contraseña_ingresada = st.text_input("Contraseña", type="password", key="contraseña")
    if st.button("Iniciar sesión"):
        usuario_valido, permiso = validar_usuario(contraseña_ingresada)
        if usuario_valido:
            st.session_state.usuario_autenticado = True
            st.session_state.permiso = permiso
            st.rerun()
        else:
            st.error("Error de inicio de sesión. Por favor, verifica tus credenciales.")

# Función principal para el inicio de sesión y el editor
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

    if st.session_state.usuario_autenticado:
        codigo_actual = obtener_codigo_almacenado()  # Recuperar el código almacenado
        if 'permiso' in st.session_state and 'editar' in st.session_state.permiso:
            st.subheader('Editar')
            editado = st_ace(value=codigo_actual, language='python', key='editor')  # Mostrar el código almacenado
            if st.button("Guardar código"):
                guardar_codigo(editado)  # Almacenar el código editado
                st.success("Código guardado con éxito!")
            
        if 'permiso' in st.session_state and 'correr' in st.session_state.permiso:
            st.subheader('Correr')
            st.write('Hello world!')         

# Ejecución de la función principal
if __name__ == "__main__":
    main()
