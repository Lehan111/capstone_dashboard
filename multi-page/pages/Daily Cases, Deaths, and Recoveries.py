import streamlit as st
import pandas as pd
import numpy as np

# read in data
dat = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
datdeath = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
datreco = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
st.write("# Daily Cases, Deaths, and Recoveries")
# get daily cases for Italy
dat_ita = dat[dat['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
diff_dat_ita = dat_ita.diff(axis=1)
diff_dat_ita.iloc[:, 0] = diff_dat_ita.iloc[:, 0].fillna(0)
diff_dat_ita = diff_dat_ita.astype(int)

# get daily deaths for Italy
datdeath_ita = datdeath[datdeath['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)
datdeath_ita.head()
diff_datdeath_ita = datdeath_ita.diff(axis=1)
diff_datdeath_ita.iloc[:, 0] = diff_datdeath_ita.iloc[:, 0].fillna(0)
diff_datdeath_ita = diff_datdeath_ita.astype(int)

# daily recoveries for Italy
datreco_ita = datreco[datreco['Country/Region'] == 'Italy'].drop(["Province/State", "Country/Region", "Lat", "Long"], axis=1)

# concatenate these three data frames
concatenated_dat = pd.concat([diff_dat_ita, diff_datdeath_ita, datreco_ita], axis=0)
labels = (['Daily Cases'] * len(diff_dat_ita)) + \
         (['Daily Deaths'] * len(diff_datdeath_ita)) + \
         (['Daily Recoveries'] * len(datreco_ita))
concatenated_dat.insert(0, 'Label', labels)

# User input for date
user_input_date = st.text_input('Enter a date (e.g., 1/22/20)')

# Options for user to select from
options = ["Daily Cases", "Daily Deaths", "Daily Recoveries"]


if user_input_date:
    # Check if the user input date is in the DataFrame columns
    if user_input_date in concatenated_dat.columns[1:]:
        # User selects an option
        selected_option = st.selectbox('Choose an option', options)
        # Find the value for the entered date and selected option
        value = concatenated_dat.loc[concatenated_dat['Label'] == selected_option, user_input_date].values[0]
        # show the value
        st.write(selected_option + ' of Italy on ' + user_input_date + ' is: ', value)
    else:
        st.error('The entered date is invalid or not in the dataset. Please enter a correct date.')
