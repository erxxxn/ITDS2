# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15yYRRXxL_Ic8rhpGpLltog4wBb6d4zCk
"""
import streamlit as st
from PIL import Image


st.set_page_config(
  page_title = "Homepage"
)

st.title("HomePage")

st.header('Predicting Future Tourism Trends in Malaysia' , divider='blue')
st.subheader('HOME PAGE:house:')
st.title(':blue[INTRODUCTION] ')
from PIL import Image
image = Image .open('/content/download.jpeg.jpeg')
st.image(
    image ,
    caption = "TOURISM" ,
    width = 800 ,
  )
st.write(
    '''
    :blue[WELCOME TO THE HOME PAGE!]
    The future of tourism application is also a crucial tool in providing stakeholders with the means and insights to handle a myriad of tourism complexity as well as the dynamism in the Malaysian tourism industry. This makes more accurate forecasts and strategic planning for smarter decisions, more sustainable growth and ultimately a better tourism experience. To create models that can together predict the accurate number of tourists into the future and that is only the tip of a giant ice berg. Using these different predictions, the project intends to provide insights and actionable recommendations to help stakeholders to make informed decisions. In a knock-on effect, it will inform better strategic planning from stakeholders, so they can leverage marketing campaigns, infrastructure development, and product offerings tied to expected tourism trends.
    '''
)

st.subheader('ANALYSIS:chart:')
st.title(':blue[ANALYSIS OF DATASETS]')
from PIL import Image
image = Image .open('/content/pl.jpg.jpeg')
st.image(
    image ,
    width = 600 ,
  )
st.subheader('Figure 1:  Analysis of tourist arrivals by month')


from PIL import Image
image = Image .open('/content/photo 2.jpg.jpeg')
st.image(
    image ,
    width = 400 ,
  )
st.subheader('Figure 2:  Analysis of tourist arrivals each year')


from PIL import Image
image = Image .open('/content/02.jpg.jpeg')
st.image(
    image ,
    width = 600 ,
  )
st.subheader('Figure 3:  Analysis of visited places of tourist')



st.sidebar.success("Select a page above")
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Title of the app
st.title("Tourism Arrival Prediction")

# Load the datasets
@st.cache_data
def load_data():
    poe_df = pd.read_csv('/content/pages/poe.csv')
    continents_df = pd.read_csv('/content/pages/continents2.csv')
    foreign_arrivals_df = pd.read_csv('/content/pages/foreign_arrivals.csv')
    return poe_df, continents_df, foreign_arrivals_df

poe_df, continents_df, foreign_arrivals_df = load_data()

# Merge datasets
foreign_arrivals_poe = foreign_arrivals_df.merge(poe_df, on='poe', how='left')
foreign_arrivals_full = foreign_arrivals_poe.merge(continents_df, left_on='country', right_on='alpha-3', how='left')

# Preprocess and feature engineering
foreign_arrivals_full['date'] = pd.to_datetime(foreign_arrivals_full['date'])
foreign_arrivals_full['month'] = foreign_arrivals_full['date'].dt.month
foreign_arrivals_full['year'] = foreign_arrivals_full['date'].dt.year
state_monthly_data = foreign_arrivals_full.groupby(['state', 'year', 'month']).agg({'arrivals': 'sum'}).reset_index()

# Create lag features
state_monthly_data['lag_1'] = state_monthly_data.groupby('state')['arrivals'].shift(1)
state_monthly_data['lag_2'] = state_monthly_data.groupby('state')['arrivals'].shift(2)
state_monthly_data['lag_3'] = state_monthly_data.groupby('state')['arrivals'].shift(3)

# Drop rows with missing lag values
state_monthly_data.dropna(inplace=True)

# Train-test split and train a regression model
X = state_monthly_data[['year', 'month', 'lag_1', 'lag_2', 'lag_3']]
y = state_monthly_data['arrivals']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

st.write(f'Mean Squared Error: {mse}')
st.write(f'R^2 Score: {r2}')

# User input for future prediction
st.header('User Input Parameters')
year = st.slider('Year', 2024, 2030, 2024)
month = st.slider('Month', 1, 12, 1)
state = st.selectbox('State', state_monthly_data['state'].unique())

# Prepare future data for prediction
future_data = pd.DataFrame({
    'year': [year],
    'month': [month],
    'state': [state]
})

last_known_values = state_monthly_data[state_monthly_data['state'] == state].tail(3)
future_data['lag_1'] = last_known_values.iloc[-1]['arrivals']
future_data['lag_2'] = last_known_values.iloc[-2]['arrivals']
future_data['lag_3'] = last_known_values.iloc[-3]['arrivals']

# Predict future arrivals
if not future_data.dropna().empty:
    future_data['predicted_arrivals'] = model.predict(future_data[['year', 'month', 'lag_1', 'lag_2', 'lag_3']])
    st.write(f'Predicted arrivals for {state} in {month}/{year}: {future_data["predicted_arrivals"].values[0]:.0f}')
else:
    st.write("Not enough data for prediction.")

# Prediction for all states
if st.sidebar.button('Predict for all states'):
    future_data_all = pd.DataFrame({
        'year': [year] * 12,
        'month': list(range(1, 13))
    })

    states = state_monthly_data['state'].unique()
    future_data_all = future_data_all.assign(key=1).merge(pd.DataFrame(states, columns=['state']).assign(key=1), on='key').drop('key', axis=1)

    for state in states:
        last_known_values = state_monthly_data[state_monthly_data['state'] == state].tail(3)
        future_data_all.loc[future_data_all['state'] == state, 'lag_1'] = last_known_values.iloc[-1]['arrivals']
        future_data_all.loc[future_data_all['state'] == state, 'lag_2'] = last_known_values.iloc[-2]['arrivals']
        future_data_all.loc[future_data_all['state'] == state, 'lag_3'] = last_known_values.iloc[-3]['arrivals']

    future_data_all.dropna(inplace=True)
    future_data_all['predicted_arrivals'] = model.predict(future_data_all[['year', 'month', 'lag_1', 'lag_2', 'lag_3']])
    state_predictions = future_data_all.groupby('state')['predicted_arrivals'].sum().reset_index()

    st.write(state_predictions)

    max_tourists_state = state_predictions.loc[state_predictions['predicted_arrivals'].idxmax()]
    st.write(f'State with the most tourists: {max_tourists_state["state"]} with {max_tourists_state["predicted_arrivals"]:.0f} predicted arrivals.')

    min_tourists_state = state_predictions.loc[state_predictions['predicted_arrivals'].idxmin()]
    st.write(f'State with the least tourists: {min_tourists_state["state"]} with {min_tourists_state["predicted_arrivals"]:.0f} predicted arrivals.')

    total_tourists = state_predictions['predicted_arrivals'].sum()
    st.write(f'Total predicted arrivals across all states: {total_tourists:.0f}')
