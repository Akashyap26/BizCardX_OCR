!pip install streamlit
!pip install numpy
!pip install easyocr
!pip install PIL
!pip install
!pip install mysql-connector-python

import streamlit as st
import pandas as pd
import numpy as np
import easyocr as ocr
from PIL import Image
import mysql.connector

reader = ocr.Reader(['en'],gpu=True)
#sql connection
host='root@localhost:3306'
database='OCR'
username='Upload_User'
password='qwerty@26'


st.title("BizCardX: Extracting Business Card Data with OCR")
st.text("Welcome to my Optical Character Recognition application🤗\nEasyOCR, as the name suggests, is a Python package that allows computer vision\ndevelopers to effortlessly perform Optical Character Recognition.")

col2,col3 = st.columns(2)

#================================================================================================================================================================================
image = st.file_uploader(label="Upload here",type=['jpg','png','jpeg'])

@st.cache_data
def load_model(): 
    reader = ocr.Reader(['en'],model_storage_directory='.')
    return reader 

reader = load_model() #load model
result_text = [] #empty list for results

# with col2:
#     st.image(image,width=300)

if st.button("Click to Begin:"):
    if image is not None:
        with col2:
            input_image = Image.open(image) #read image
            st.image(input_image,width=300) #display image

            with st.spinner("Loading...."):
                result = reader.readtext(np.array(input_image))
                for text in result:
                    result_text.append(text[1:])
        #st.write(result_text)
    st.balloons()
else:
    st.write("Upload an Image")

with col3:
    ocr_df = pd.DataFrame(data =(result_text) ,columns=("Text","Confidence %"))
    ocr_df["Confidence %"] = ((ocr_df["Confidence %"])*100).round(2)
    st.dataframe(ocr_df,use_container_width=True)




#==============================================================================================================================================
def create_connection(host, username, password, database):
    connection = mysql.connector.connect()
    return connection


if st.button("Connect to MySQL"):
        connection = create_connection(host, username, password, database)
        if connection.is_connected():
            st.success("Successfully connected to MySQL")

            # Load data into dataframe
            data = pd.read_sql("SELECT * FROM mytable", connection)

            # Show data in Streamlit
            st.write(data)
        else:
            st.error("Failed to connect to MySQL")

    








    
  


    

















