import streamlit as st
from streamlit_option_menu import option_menu
from views import Home, About, Guide, Team, Settings
from utils import logo
from cryptography.fernet import Fernet

# Function to encrypt user key
def encrypt_key(key, keyfile):
    cipher_suite = Fernet(keyfile)
    encrypted_key = cipher_suite.encrypt(key.encode())
    return encrypted_key
# Function to decrypt user key
def decrypt_key(encrypted_key, keyfile):
    cipher_suite = Fernet(keyfile)
    decrypted_key = cipher_suite.decrypt(encrypted_key).decode()
    return decrypted_key

def submit():
   st.session_state.my_key = st.session_state.key_openai
    
    # Encrypt and save user key
   keyfile = Fernet.generate_key()  # Generate a key for encrypting user keys
   encrypted_user_key = encrypt_key(st.session_state.my_key, keyfile)
   
   # Store encrypted key in a secure manner (e.g., in a database or file)
   # Here, we'll just store it in a Streamlit session state for simplicity
   st.session_state.encrypted_user_key = encrypted_user_key
   st.session_state.keyfile = keyfile
   
   st.success("Your key has been securely saved!")
   
   
   st.session_state.key = ''
def main():
    #logo()
    st.write("#")
   #add streamlit option menu to create options
    with st.sidebar: 
        st.image("omdena_logo2.png")
        #st.text_input('Introduce tu clave de OpenAI:',type='password',key='key_openai',on_change=submit)
        #st.text_input('Ingresa tu clave de búsqueda de Google:',type='password',key='key_google',on_change=submit)
        choice = option_menu("Menu", ["Inicio", "Nuestro proyecto", "Guia", "Colaboradores","Configuraciones"],
                            icons=['house', 'info', 'book', 'people','gear'],
                            menu_icon="app-indicator", default_index=0,
                            styles={
            "container": {"padding": "5!important", "background-color": "#0A122A"},
            "icon": {"color": "#DOCCD0", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#000000"},
            "nav-link-selected": {"background-color": "#3399ff"},
        }
        )
    if choice == "Inicio":
        Home.main()
    if choice == "Nuestro proyecto":
        About.main()
    if choice == "Guia":
        Guide.main()
    if choice == "Colaboradores":
        Team.main()
    if choice == "Configuraciones":
        Settings.main()

    with st.sidebar:
        "# Falsa o Real?"
        "Detecta noticias falsas con ayuda de nuestra herramienta de IA"
        st.image("Fake_or_Real2.png")


if __name__=='__main__':
   main()