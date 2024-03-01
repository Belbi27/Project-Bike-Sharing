from telnetlib import LOGOUT
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image

data_day = pd.read_csv("day.csv")

data_day['dteday'] = pd.to_datetime(data_day['dteday'])
data_day['season'] = data_day.season.astype('category')
data_day['yr'] = data_day.yr.astype('category')
data_day['mnth'] = data_day.mnth.astype('category')
data_day['holiday'] = data_day.holiday.astype('category')
data_day['weekday'] = data_day.weekday.astype('category')
data_day['workingday'] = data_day.workingday.astype('category')
data_day['weathersit'] = data_day.weathersit.astype('category')

data_day.season.replace((1,2,3,4), ('Spring', 'Summer', 'Fall', 'Winter'), inplace=True)
data_day.yr.replace((0,1), (2011, 2012), inplace=True)
data_day.mnth.replace((1,2,3,4,5,6,7,8,9,10,11,12), ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'), inplace=True)
data_day.weekday.replace((0,1,2,3,4,5,6), ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'), inplace=True)
data_day.workingday.replace((0,1), ('No', 'Yes'), inplace=True)
data_day.weathersit.replace((1,2,3,4), ('Clear', 'Misty', 'Light_SnowRain', 'Heavy_SnowRain'), inplace=True)

def create_daily_rental_day(data_day):
    daily_rental_day = data_day.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered" : "sum",
        "cnt" : "sum"
    })
    daily_rental_day = daily_rental_day.reset_index()
    return daily_rental_day

datetime_columns = ["dteday"]
data_day.sort_values(by="dteday", inplace=True)
data_day.reset_index(inplace=True)
 
for column in datetime_columns:
    data_day[column] = pd.to_datetime(data_day[column])

min_date = data_day["dteday"].min()
max_date = data_day["dteday"].max()

with st.sidebar:
    image = Image.open('Logo.png')
    st.image(image, caption='Logo', use_column_width=True)
    start_date, end_date = st.date_input(
        label= 'Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_data_day = data_day[(data_day["dteday"] >= str(start_date)) & 
                (data_day["dteday"] <= str(end_date))]

daily_rental_day = create_daily_rental_day(main_data_day)

st.header('Bike Sharing Dashboard :bike:')

st.subheader('User')
col1, col2, col3 = st.columns(3)
with col1:
    user_casual = daily_rental_day.casual.sum()
    st.metric("Not Registered Users", value=user_casual)
with col2:
    user_registered = daily_rental_day.registered.sum()
    st.metric("Registered Users", value=user_registered)
with col3:
    user_total = daily_rental_day.cnt.sum()
    st.metric("Total Users", value=user_total)

st.subheader("Influence of Weather on Rentals")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
sns.barplot(x='cnt', y='weathersit', data=data_day, palette="flare", hue='weathersit', orient="h", ax=ax)
ax.set_ylabel("Weather Conditions", fontsize=15)
ax.set_xlabel("Total Rental", fontsize=15)
ax.set_title(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Difference in Rental Amount on Holidays and Weekdays in Each Season")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
sns.barplot(x='workingday', y='cnt', data=data_day, palette="magma", hue='season', ax=ax)
ax.set_ylabel("Total Rental", fontsize=15)
ax.set_xlabel("Day", fontsize=15)
ax.set_xticks([0,1])
ax.set_xticklabels(['Weekend', 'Weekday'])
ax.set_title(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("Total rent for each month")
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(20,10))
sns.barplot(x='mnth', y='cnt', data=data_day, palette="mako", hue='yr', ax=ax)
ax.set_ylabel("Total Rental", fontsize=15)
ax.set_xlabel("Month", fontsize=15)
ax.set_title(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)