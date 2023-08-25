import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#read in the file
uploaded_file = st.file_uploader("Upload a csv", type=("csv"))
df = pd.read_csv(uploaded_file)

if not df.empty:

    clinic_source = df['Clinic Name'].unique().tolist()
    clinic_dept = df['Department'].unique().tolist()
    admit_source = df['Admit Source'].unique().tolist()

    with st.sidebar:
        st.write("Select a range on the slider (it represents movie score) \
        to view the total number of movies in a genre that falls \
        within that range ")
    
        new_wait_time = st.slider(label = "Choose a value:",
                                    min_value = 10.0,
                                    max_value = 120.0,
                                    value = (13.0,24.0))

        #create a multiselect widget to display genre
        new_dept_list = st.multiselect('Choose Dept:',
                                                clinic_dept)
        #create a selectbox option that holds all unique years
        admit_source_select = st.selectbox('Choose a Admit Source',
            admit_source, 0)
        
wait_time_filter = (df['Wait Time Min'].between(*new_wait_time))        
dept_admit_filter = (df['Department'].isin(new_dept_list)) \
& (df['Admit Source'] == admit_source_select)

st.dataframe(df[wait_time_filter])