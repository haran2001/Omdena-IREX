import streamlit as st
from utils import logo
import json
import os

def save_settings(settings):
    with open("config/settings.json", "w") as file:
        json.dump(settings, file)
        
def load_settings():
    try:
        path = os.path.abspath('config/settings.json')
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
         return None
            


def main():
    #logo()
    st.write("#") #forces the page to load from top 
    st.image("omdena_logo.png", width=300, use_column_width=True)
    st.title(" :blue[Portal de detección de noticias falsas]")
    st.write("##### Por favor, asegúrate de que estos ajustes estén agregados antes de proceder con la validación de noticias. Estos son cambios únicos, a menos que desees cambiarlos en el futuro.")
    settings=load_settings()
    if settings:
        st.write('  El punto final actual del servidor es: ' + settings['server_endpoint'])
        #st.write('  El directorio actual de informes es: ' + settings['report_directory'])
        st.write()
        st.write('Puedes cambiarlos agregando nuevos valores a continuación:')
    else:
        st.write('El punto final del servidor y el directorio de informes aún no se han agregado. Por favor, agrégalos abajo:')
        settings = {}
        
    
    with st.container(border=True):
         settings['server_endpoint'] = st.text_input('Ingrese el punto final del servidor backend:')
         settings['report_directory'] = 'report/report_output'
         #settings['report_directory'] = st.text_input('Ingresa el directorio donde te gustaría almacenar tus informes:')
    if st.button('Guardar Configuraciones',type='primary'):
        if not settings['server_endpoint'] or not settings['report_directory']:
            st.warning('Asegúrate de agregar tanto el punto final del servidor como el directorio de informes antes de continuar.')
        else:
            save_settings(settings)
            st.success("Configuraciones de la aplicación guardadas exitosamente. Por favor, regresa a la página de inicio para continuar.")
    


if __name__=='__main__':
   main()