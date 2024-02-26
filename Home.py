import streamlit as st

def main():
    st.image("omdena_logo.png", width=300, use_column_width=True)
    st.title(" :blue[Fake News Detection Portal]")
    
    with st.container(border=True):
        st.selectbox("Select News Source:", ["www.elsalvador.com", "www.elmundo"])
        st.write('Enter the URL of the news article or paste text from the news article below...')
        url = st.text_input('URL of the article:')
        article = st.text_area('Text from the article:')
        summary = 'This is the summary'
        if st.button('Get Summary & Insights',type='primary'):
            st.text_area('Summary:', summary)
    
    with st.container(border=True):
        st.text_area('##### Summary:',disabled=True)
        
    with st.container(border=True):
        st.markdown('##### Key Insights:')
        st.markdown('###### Insight1')
        st.markdown('###### Insight2')
        st.markdown('###### Insight3')
    
    with st.container(border=True):
        row1 = st.columns(2, gap='small')
        row2 = st.columns(2,gap='small')
        with row1[0]:
            st.write('##### Validation:')
        with row2[0]:   
            if st.button('Confirm',type='primary'):
                pass
        with row1[1]:
            st.write('#####')
        with row2[1]:
            if st.button('Clear'):
                pass
    
    with st.container(border=True):
        row1 = st.columns(2, gap='small')
        row2 = st.columns(2,gap='small')
        with row1[0]:
            st.write('##### Prediction:')
        with row2[0]:   
            st.toggle('Fact',disabled=True,)
        with row1[1]:
            st.write('#####')
        with row2[1]:   
            conf = '95%'
            st.write(f'###### Confidence: {conf}')
            
            
    with st.container(border=True):
        st.text_area('##### Justification:',disabled=True)
        
    with st.container(border=True):
        if st.button('Reset',type='primary'):
            pass
   
   
    

if __name__== '__main__':
    main()
