import streamlit as st
import streamlit.components.v1 as com
import requests
import base64
from datetime import datetime
from pyhtml2pdf import converter
import os
import time
import json
import pandas as pd
from views import Settings

def generate_news_content_html(news):
    max_words_per_section = 250
    words = news.split()
    paragraph_sections = [' '.join(words[i:i+max_words_per_section]) for i in range(0, len(words), max_words_per_section)]

    paragraph_divs = ""
    for section in paragraph_sections:
        paragraph_divs += f"<div class='paragraph'>{section}</div>\n"

    html_content = paragraph_divs
    return html_content

    

def load_settings():
    try:
        path = os.path.abspath('config/settings.json')
        with open(path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
         return None


def validate_news(server_endpoint,headline,news):
        response = requests.post(server_endpoint,data={'headline': headline,'news':news})
        return response.json()
       
def clear_fields():
    st.session_state['headline'] = ''
    st.session_state['news'] = ''
    
def create_report(headline,news,date_time,category,confidence,reasoning,context,times):
    news = generate_news_content_html(news)
    with open('report/context_temp.html','r') as con:
        context = con.read()
    with open('report/styles.css') as source:
        design = source.read()
    with open("report/omdena_logo.png",'rb') as img:
        r_img = img.read()
        img_src = base64.b64encode(r_img).decode('utf-8')
    content = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Omdena IREX</title>
            <style>{design}</style>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body>
        <div id=parent>
        <p style="text-align:center;"><img src="data:image/gif;base64,{img_src}" alt="omdena png"  width="800" class="center"></p>
        <div class="container">
                <div class="sections">
                    <h2 class="section-title">Informe sobre análisis de noticias del portal de Omdena para la detección de noticias falsas</h2>
                </div>
                <div class="sections">
                    <h2 class="section-title">Fecha:</h2>
                    <div class="list-card">
                        <div>
                            <span>{date_time}</span>
                        </div>
                    </div>
                </div>
                <div class="sections">
                    <div class="list-card">
                        <div>
                            <h2 class="section-title">Titular de la Noticia:</h2>
                            <span>{headline}</span>
                        </div>
                    </div>
                </div>
                <div class="sections">
                        <div>
                           <h2 class="section-title">Detalles de la Noticia:</h2>
                           <div class="section-details">
                            <span>{news}</span>
                           </div> 
                        </div>
                </div>
        </div>

       
        <div class="container cards">
            <div class="card">
                <div class="m-level">
                    <span>Probabilidad basada únicamente en el análisis de texto:{confidence}</span>
                    <br></br>
                    <span>Predicción basada en toda la información recopilada:{category}</span>
                </div>
            </div>
        </div>
        
        
        <div class="container">
                    <h2 class="section-title">Razonamiento:</h2>
                    <div class="section-details">
                    <span> {reasoning} </span>
                    </div>
        </div>

        <div class="container">   
                    <h2 class="section-title">Fuentes:</h2>
                    <div class="section-details">
                    <span> {context} </span>
                    </div>
        </div>

        </div>
        </body>
        </html>"""
    with open('report/report.html', 'w') as f:
        f.write(content)
    
def generate_pdf(report_path,headline,news,date_time,category,confidence,reasoning,context,times):
    try:
        create_report(headline,news,date_time,category,confidence,reasoning,context,times)
        source_path = os.path.abspath('report/report.html')
        dest_path = os.path.abspath(report_path)
        if os.path.exists(dest_path):
            converter.convert(f'file:///{source_path}', dest_path + '/report.pdf')
        else:
            raise Exception('La ruta de informe especificada no existe. Por favor, confirma que el directorio de informes especificado en tu página de configuración es válido en tu sistema.')
    except Exception as e:
        raise Exception(f"La generación del informe PDF falló con error: {e}")
       


def main():
    #logo()
    settings=load_settings()
    if not settings:
        st.warning('El punto final del servidor y el directorio de informes no se han agregado a tu configuración. Debes agregarlos la primera vez que uses la aplicación. Siempre puedes cambiarlos más tarde yendo a la página de configuración.')
        Settings.main()
    else:
    
        flag = ''
        st.session_state['response'] = {}
        if 'val_completed' not in st.session_state:
            st.session_state['val_completed'] = False
            
        st.write("#") #forces the page to load from top 
        st.image("omdena_logo.png", width=300, use_column_width=True)
        st.title(" :blue[Portal de detección de noticias falsas]")
        
        st.toast('''¡Tu privacidad es importante para nosotros! Puedes estar tranquilo, priorizamos la protección de tus datos. Nuestra aplicación está diseñada pensando en tu privacidad, y no capturamos ni utilizamos tus datos personales de ninguna manera. Tu confianza es importante para nosotros, y estamos comprometidos a mantener la confidencialidad y seguridad de tu información. Si tienes alguna inquietud o pregunta sobre tu privacidad, no dudes en contactarnos. Gracias por elegirnos.''', icon="⚠️")

        #added to center the image on the sidebar to make it look better
        st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
        )
        
        

        with st.container(border=True):
            st.session_state['headline'] = st.text_input('##### Ingrese el titular del artículo de noticias:')
            st.session_state['news'] = st.text_area('##### Pegue el texto del artículo de noticias:')
                
                
        with st.container(border=True):
            row1 = st.columns(1, gap='small')
            row2 = st.columns(1,gap='small')
            with row1[0]:
                st.write('##### Validación:')
            with row2[0]: 
                    if st.button('Confirmar',type='primary') or st.session_state['val_completed']:
                        if not(st.session_state['headline']):
                            st.warning('Por favor, ingrese el titular de la noticia.',icon='🚨')
                        elif not(st.session_state['news']):
                            st.warning('Por favor, pegue el artículo de noticias.',icon= '🚨')
                        else:
                            server_endpoint = settings['server_endpoint']
                            with st.spinner('Validación de noticias en progreso...'):
                                time.sleep(5)
                            
                                response = validate_news(server_endpoint,st.session_state['headline'],st.session_state['news'])
                                st.session_state['response'] = response
                                st.session_state['context'] = response['context']
                                st.session_state['probability'] = response['result_pred_proba']
                                st.session_state['times'] = response['times']
                                decision_result = response['decision_result']
                                des_res = json.loads(str(decision_result))
                                st.session_state['category'] = des_res['category']
                                st.session_state['reasoning'] = des_res['reasoning']
                                
                                print(st.session_state['category'] )
                                print(st.session_state['probability'] )
                            
                            
                                #st.session_state['response'] = {'ret':'testing'}
                                #st.session_state['context'] = 'context jhjhrehjhrejhjhrehjhjerhjjhrehjrhjrehjehjjhrerjhjrjhhjrhjreerjhjhr'
                                #st.session_state['probability'] = '0.70'
                                #st.session_state['times'] = '2'
                                #st.session_state['category'] = 'Fake'
                                #st.session_state['reasoning'] = 'reasoning ehjjhejherhjjhrejherhjhjhjhjrjhrhjrehjrehj'

                                
                                if  st.session_state['category'] == 'Fake':
                                    flag = False
                                    prob_msg = 'Falso'
                                else:
                                    flag = True
                                    prob_msg = 'Real'
                                    
                                st.session_state['rep_date_time'] =  datetime.now().strftime("%B %d %Y %H:%M:%S")
                                st.session_state['probability'] = "{:2.0f}".format(round(st.session_state['probability'] * 100,2)) + '%'
                                
                            

                                with st.container(border=True):
                                    row0 = st.columns(2, gap='small')
                                    row1 = st.columns(2, gap='small')
                                    row2 = st.columns(2,gap='small')
                                    row3 = st.columns(2,gap='small')
                                    
                                    with row0[0]:
                                        st.write('##### Fecha y hora de ejecución:')
                                    with row0[1]:
                                        if st.session_state['response']:
                                            st.write('##### ' + st.session_state['rep_date_time'])
                                
                                    
                                    with row1[0]:
                                        st.write('##### Etiqueta predicha basada en toda la información recopilada:')
                                    with row1[1]:   
                                        if flag == '':
                                            st.write('')
                                        elif flag == False:
                                            st.warning('Falso',icon='❌')
                                        else:
                                            st.warning('Real',icon='✅')
                                        
                                    with row2[0]:
                                        st.write('##### Probabilidad predicha basada únicamente en el texto:')
                                    with row2[1]:
                                        if st.session_state['response']:   
                                            st.metric('Probabilidad de ' + str(prob_msg) + '(análisis de texto únicamente)', st.session_state['probability'])
                                    #with row3[0]:
                                        #st.write('##### Número de intentos:')
                                    #with row3[1]:
                                        #if st.session_state['response']:
                                            #st.markdown('#### ' +  str(st.session_state['times'])) 
                                            
                                            
                                            
                                                
                                    with st.container(border=True):
                                        if st.session_state['response']:
                                            st.write('##### Razonamiento:')
                                            st.markdown(f"""<p style='text-align: justify; font-size: 15px;'>{st.session_state['reasoning']}</p>""", unsafe_allow_html=True,)
                                        
                                            
                                    with st.container(border=True):
                                        if st.session_state['response']:
                                            st.write('##### Contexto:')
                                            """df = pd.DataFrame(st.session_state['context'])
                                            st_df = st.dataframe(df,column_config={"snippet": "Snippets", 
                                                                        "source": st.column_config.LinkColumn("Sources URL"),
                                                                        "width":"100"
                                                                        },hide_index=True)
                                            con_html = df.to_html()"""
                                        
                                            
                                            context = st.session_state['context']
                                            st.markdown("<div>",True)
                                            for i in range(len(context)):
                                                st.markdown(f"<li>{context[i]['snippet']}",True)
                                                st.markdown(f"{context[i]['source']}</li>",True)
                                            st.markdown("</div>",True)
                                            
                                            with open('report/context_temp.html','w') as f:
                                                f.write("<ul>")
                                                for i in range(len(context)):
                                                    #f.write(f"<li>{context[i]['snippet']}")
                                                    f.write(f"<li><a href={context[i]['source']}</a>{context[i]['snippet']}</li><br></br>")
                                                f.write("</ul>")
                                                
                                                
                                    st.session_state['val_completed'] = True
                                    st.success('Validación completada!')            
            
                                    '''with st.container(border=True):
                                        con_html = ''
                                        if st.button('Guardar Informe', on_click=generate_pdf,type='primary',args=(settings['report_directory'],st.session_state['headline'],st.session_state['news'],st.session_state['rep_date_time'],st.session_state['category'],st.session_state['probability'],st.session_state['reasoning'],con_html,st.session_state['times'])):
                                                with st.spinner('Generación de informe en curso...'):
                                                    time.sleep(5)
                                                st.success('Informe generado exitosamente')
                                        else:
                                            st.error(f"Ha ocurrido un error")'''
                                            
        with st.container(border=True):
            con_html = ''
            if st.button('Guardar Informe',type='primary'):
                try:
                    if st.session_state['val_completed']:
                        generate_pdf(settings['report_directory'],st.session_state['headline'],st.session_state['news'],st.session_state['rep_date_time'],st.session_state['category'],st.session_state['probability'],st.session_state['reasoning'],con_html,st.session_state['times'])
                        with st.spinner('Generación de informe en curso...'):
                            time.sleep(5)
                        st.success('Informe generado exitosamente')
                        with open("report/report_output/report.pdf", "rb") as pdf_file:
                            PDFbyte = pdf_file.read()
                        st.download_button(label="Download Report",data=PDFbyte,file_name='/report'  + datetime.now().strftime("%d%m%Y_%H%M%S") + '.pdf',mime='application/octet-stream',type='primary')
                    else:
                        st.warning('Las noticias aún no han sido validadas. Valida las noticias primero')
                except Exception as e:
                    st.error(f"Ha ocurrido un error: {e}")
                                                

if __name__== '__main__':
    main()
