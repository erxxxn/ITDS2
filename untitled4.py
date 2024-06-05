# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15yYRRXxL_Ic8rhpGpLltog4wBb6d4zCk
"""
import streamlit as st
from PIL import Image

def show_home():
    st.title("HomePage")
    st.header('Predicting Future Tourism Trends in Malaysia', divider='blue')
    st.subheader('HOME PAGE:house:')
    st.title(':blue[INTRODUCTION]')
    
    image = Image.open('download.jpeg.jpeg')
    st.image(image, caption="TOURISM", width=800)
    
    st.write('''
        :blue[WELCOME TO THE HOME PAGE!]
        The future of tourism application is also a crucial tool in providing stakeholders with the means and insights to handle a myriad of tourism complexity as well as the dynamism in the Malaysian tourism industry. This makes more accurate forecasts and strategic planning for smarter decisions, more sustainable growth and ultimately a better tourism experience. To create models that can together predict the accurate number of tourists into the future and that is only the tip of a giant ice berg. Using these different predictions, the project intends to provide insights and actionable recommendations to help stakeholders to make informed decisions. In a knock-on effect, it will inform better strategic planning from stakeholders, so they can leverage marketing campaigns, infrastructure development, and product offerings tied to expected tourism trends.
    ''')

    st.subheader('ANALYSIS:chart:')
    st.title(':blue[ANALYSIS OF DATASETS]')
    
    image = Image.open('pl.jpg.jpeg')
    st.image(image, width=600)
    st.subheader('Figure 1: Analysis of tourist arrivals by month')
    
    image = Image.open('photo 2.jpg.jpeg')
    st.image(image, width=400)
    st.subheader('Figure 2: Analysis of tourist arrivals each year')
    
    image = Image.open('02.jpg.jpeg')
    st.image(image, width=600)
    st.subheader('Figure 3: Analysis of visited places of tourist')

import streamlit as st
from home import show_home
from prediction import show_prediction

# Set page config
st.set_page_config(page_title="Tourism Prediction App")

# Create a sidebar for navigation
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Home', 'Prediction'])

# Show the selected page
if page == 'Home':
    show_home()
elif page == 'Prediction':
    show_prediction()

st.sidebar.success("Select a page above")

