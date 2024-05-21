
import streamlit as st
import psycopg2
import hashlib
import pandas as pd

class PanelAdmin:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="db",
            port="5432",
            database="proyecto_cripto",
            user="admin",
            password="cripto"
        )
        self.cursor = self.conn.cursor()

        self.herramientas_disponibles = {
            "Editar": "Editar",
            "Correr": "Correr",
            "Admin Portal": "Admin Portal",
            "Todas" : "Todas"
        }

    def lista_usuarios(self):
        self.cursor.execute("SELECT usuario FROM usuarios")
        return [item[0] for item in self.cursor.fetchall()]


    def create_user(self, username, password):
        self.cursor.execute("INSERT INTO usuarios (usuario, contraseña) VALUES (%s, %s)", (username, password))
        self.conn.commit()

    def assign_tool(self, usuario, tool_name):
        tool_list = ','.join(tool_name) if isinstance(tool_name, list) else tool_name
        self.cursor.execute("UPDATE usuarios SET permiso = %s WHERE usuario = %s", (tool_list, usuario))
        self.conn.commit()
    
    def delete_user(self, username):
        self.cursor.execute("DELETE FROM usuarios WHERE usuario = %s", (username,))
        self.conn.commit()
        
    def lista_usuarios_registrados(self):  
        self.cursor.execute("SELECT * FROM usuarios")
        self.conn.commit()
        return self.cursor.fetchall()


    def main(self):
        st.image('resources/dmx.jpg', width=100)
        col1,col2 = st.columns(2)
        with col1:
            st.subheader('Crea un nuevo usuario')
            username = st.text_input("Nombre de usuario")
            password = st.text_input("Contraseña", type="password")
            password = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if st.button("Crear usuario"):
                self.create_user(username, password)
                st.success("Usuario creado exitosamente.")
        with col2:
            st.subheader('Asigna herramientas a un usuario')
            usuarios = self.lista_usuarios()
            usuario = st.selectbox("Selecciona un usuario", usuarios, key='1')
            herramientas = self.herramientas_disponibles.keys()
            herramientas = st.multiselect("Selecciona una herramienta", herramientas)
            if st.button("Asignar herramientas"):
                self.assign_tool(usuario, herramientas)
                st.success("Herramientas asignadas exitosamente.")
                
        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Elimina un usuario')
            usuario = st.selectbox("Selecciona un usuario", usuarios, key='2')
            if st.button("Eliminar usuario"):
                self.delete_user(usuario)
                st.success("Usuario eliminado exitosamente.")
        with col4: 
            st.subheader('Usuarios registrados')
            usuarios_registrados = self.lista_usuarios_registrados()
            usuarios_registrados = pd.DataFrame(usuarios_registrados, columns=['Contraseña', 'Permisos', 'Usuario'])
            usuarios_registrados = usuarios_registrados.drop(columns=['Contraseña'])
            st.dataframe(usuarios_registrados, hide_index=True)
            
if __name__ == "__main__": 
    panel = PanelAdmin()
    panel.main()


