import streamlit as st
from PIL import Image
import pandas as pd

st.set_page_config(
    page_title="Home",
    page_icon="📌",
    layout='wide'
    )


banner = Image.open( 'banner.png' )
st.image( banner)


# Import dataset
df_raw = pd.read_csv( 'dataset/dfpronto.csv' )

df = df_raw.copy()



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

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv = convert_df(df)

st.sidebar.markdown(":file_folder:")
st.sidebar.download_button(
    label='Download CSV',
    data=csv,
    file_name='dfpronto.csv',
    mime='text/csv',
)


#========================================================

st.markdown( """---""" )

st.title('')

st.markdown("This dashboard was built to follow the company's growth metrics, with regard to restaurants, type of cuisine and location.")

st.markdown( """ """ )

col1, col2 = st.columns(2)

with col1:
    
    st.markdown (
        """
        
        ## How to use this dashboard:
        - Overall: contains the general metrics;
        - Local: contains informations about countries and cities of the restaurants;
        - Restaurants: contains informations about the restaurants and type of cuisines.

        ### Important: 
        The price average for two, was converted to dollar, so that the comparison is possible


        ### Ask for Help
        - Time de Data Science no Discord
            - @ivelise
            """)

with col2:
    st.markdown('## Last Updates')
    st.write('Pop-up with the informations of the restaurants')
    
    update = Image.open( 'update.png' )
    st.image(update)
