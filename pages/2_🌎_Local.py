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


st.set_page_config( page_title='Local', page_icon='🌎', layout='wide')

# Import dataset
df_raw = pd.read_csv( 'dataset/dfpronto.csv' )

df = df_raw.copy()


#=======================================================
#       BARRA LATERAL
#=======================================================


logo = Image.open( 'logo.png' )
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




#====================================
#      LAYOUT LOCATIONS
#====================================
st.markdown("__________")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Table Booking', df['has_table_booking'].sum(), help="Restaurants that has table booking")

with col2:
    st.metric('Delivery Service', df['is_delivering_now'].sum(), help="Restaurants with delivery service")

with col3:
    st.metric('Online Service', df['has_online_delivery'].sum(), help="Restaurants that acept online requests")

with st.container():
    st.subheader('Mean price by country')
    df_aux = df[['restaurant_name', 'country', 'dollar']].groupby('country').mean().reset_index()
    fig = px.line(df_aux, x='country', y='dollar')
    st.plotly_chart( fig, use_container_width=True)
    

col1, col2 = st.columns(2)

with col1:
    st.subheader('Votes distribution by country - Top 5')
    df_aux = df[['country', 'votes']].groupby('country').sum().reset_index().sort_values('votes', ascending=False).head(5)
    top5country = df_aux['country'].unique()
    df5country = df.loc[df['country'].isin (top5country)]
    df5country['votes'] = df5country['votes']+1
    df5country = df5country.loc[(df['votes'] < 2500), :] 
    fig = px.box( y='votes', x='country', data_frame=df5country, color='country')
    st.plotly_chart(fig, use_container_width=True)
      
    
with col2:
    st.subheader('reações')
    

    
with st.container():
    st.subheader('reações')
    
      
    