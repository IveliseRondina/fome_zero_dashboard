# Libraries
import folium
import pandas as pd
from PIL import Image
import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

st.set_page_config( page_title='Local', page_icon='🍴', layout='wide')

# Import dataset
df_raw = pd.read_csv( 'dataset/dfpronto.csv' )

df = df_raw.copy()


#=======================================================
#       BARRA LATERAL
#=======================================================


logo = Image.open( 'logo.png')
st.sidebar.image( logo)

st.sidebar.markdown( """_______""" )

# FILTRO
st.sidebar.markdown( '## Average Price for Two' )

dollar_slider_min, dollar_slider_max = st.sidebar.slider( 
    'Select price limit:',
    value=[0.0, 755.0],
    min_value=0.0,
    max_value=755.0)

st.sidebar.markdown( """---""" )

st.sidebar.markdown( '## Countries' )

country = st.sidebar.multiselect( 
    'Select the country:',
    list(df['country'].unique()), 
    default=list(df['country'].unique()) )

st.sidebar.markdown( """---""" )

## Filtro de preço
linhas_selecionadas_max = df['dollar'] <=  dollar_slider_max
linhas_selecionadas_min = df['dollar'] >=  dollar_slider_min
df = df.loc[linhas_selecionadas_max & linhas_selecionadas_min, :]

# Filtro de país
linhas_selecionadas = df['country'].isin( country )
df = df.loc[linhas_selecionadas, :]




#----------------------------------------------------
#       LAYOUT VISAO RESTAURANTE
#---------------------------------------------------



st.markdown("__________")

with st.container():  
        st.markdown('## Mean Price by cuisines (dollar)')
        df_aux = df[['cuisines', 'dollar']].groupby('cuisines').mean().round(2).sort_values('dollar', ascending=False).reset_index().head(15)
        fig = px.bar(df_aux, x='cuisines', y='dollar',color='cuisines')
        st.plotly_chart( fig, use_container_width=True)
        

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.subheader('Type os Cuisines')
        text = " ".join(cat for cat in df.cuisines)

        # Generate word cloud
        word_cloud = WordCloud(
            width=3000,
            height=2000,
            random_state=1,
            collocations=False,
            stopwords=STOPWORDS,
            ).generate(text)
        
        # Display the generated Word Cloud
        plt.imshow(word_cloud)
        plt.axis("off")
        fig = plt.show()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot(fig)
        
with col2:        
    with st.container():
        st.subheader('Top 10 Cuisines')
        cozinhas = ['North Indian',' American', 'Cafe' ,'Italian', 'Pizza', 'Chinese', 'Burger', 'Fast Food' ,'Continental', 'Seafood']

        df10coz = df.loc[df['cuisines'].isin (cozinhas)]

        fig = px.histogram(df10coz, x="cuisines", color_discrete_sequence=['mediumpurple'])
        st.plotly_chart( fig, use_container_width=True )


        
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Top 10 Restaurants')
        rest10 = df[['restaurant_name', 'country', 'city', 'cuisines', 'dollar', 'aggregate_rating', 'votes']].sort_values('aggregate_rating', ascending=False).head(10)
        st.dataframe(rest10)
        
    with col2:
        st.subheader('Rating distribution')
     
        
        fig = plt.figure(figsize=(12, 6))
        sns.distplot(df['aggregate_rating'], color="y")
        
        st.pyplot(fig)

     
        
