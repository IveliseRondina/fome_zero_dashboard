# Libraries
import plotly.express as px
import plotly.graph_objects as go
import folium
import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config( page_title='Overall', page_icon='📊', layout='wide')


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



#=========================
#  LAYOUT VISÃO GERAL
#========================


st.markdown("__________")

st.title('Overall Metrics')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric('Number of Restaurants', value=df['restaurant_id'].nunique())
    
    with col2:
        st.metric('Number of Countries', value=df['country'].nunique() )
        
    with col3:
        st.metric('Number of Cities', value=df['city'].nunique() )
        
    with col4:
        st.metric('Type of Cuisines', value=df['cuisines'].nunique() )
        
    with col5:
        sum_votes = df['votes'].sum()
        votes = (f'{sum_votes:,f}').replace(",",".")[:9]
        st.metric('Sum of Votes', value=votes )

st.markdown("__________")
        
with st.container():
    st.header("Overview Map")
#    midpoint = [np.average(df['latitude']), np.average(df['longitude'])]
#    
#    df_aux = df.head(50)
#    
#    st.pydeck_chart(pdk.Deck(
#                            map_style=None,
#                            initial_view_state= pdk.ViewState(latitude=midpoint[0],
#                                                 longitude=midpoint[1],
#                                                 zoom=2,
#                                                 pitch=50),
#                            layers=[pdk.Layer("HexagonLayer",
#                                             data=df_aux,
#                                             get_position=['longitude', 'latitude'],
#                                             radius=200,
#                                             elevation_scale=50,
#                                             elevation_range=[0,3000],
#                                             pickable=True,
#                                             extrudded=True,
#                                             coverage=1),
#                                     pdk.Layer('ScatterplotLayer',
#                                              data=df_aux,
#                                              get_position=['longitude', 'latitude'],
#                                              get_color=[200,30,0,160],
#                                              get_radius= 200)]))
    
    map = folium.Map(location=[39,32], zoom_start=1.5)
    
    marker_cluster = MarkerCluster().add_to(map)
    
    for i in df.index:
        html = df.loc[i].to_frame().to_html()
        folium.Marker([df.loc[i,'latitude'], df.loc[i,'longitude']],
                      tooltip=df.loc[i,"restaurant_name"],
                      popup=folium.Popup(folium.IFrame(html=html, width=300, height=400))).add_to(marker_cluster) 
    
    folium_static( map, width=1200 , height=600)
        
        

#for i in df_istanbul.index:
#    html = df_istanbul.loc[i].to_frame().to_html()
#    folium.Marker([df_istanbul.loc[i].Latitude,df_istanbul.loc[i].Longitude],
#                  tooltip=df_istanbul.loc[i,"Restaurant Name"],
#                  popup = folium.Popup(folium.IFrame(html=html, width=300, height=400)),
##                   icon=folium.Icon(icon=df_istanbul.loc[i,"Aggregate rating"])
#                 ).add_to(m)
#m