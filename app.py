from map import getSatelliteImage
from model import extractValue
import streamlit as st
import numpy as np
import cv2
import pandas as pd

def saveImage(byteImage):
    nparr = np.fromstring(byteImage, np.uint8)
    imgFile = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   
    return imgFile

st.set_page_config(
    page_title = 'Ponds Mapping',
    page_icon = '🌏'
)

st.header("Tambak Ikan Mapping")
st.subheader("Input Latitude, Longitude dan Zoom Level yang di inginkan")
latitude = st.text_input("Input Latitude:")
longitude = st.text_input("Input Longitude:")
zoomLevel = st.text_input("Input Zoom Level:", value=18)

if st.button("Show Satellite Image"):
    latitude, longitude, zoomLevel = float(latitude), float(longitude), int(zoomLevel)
    with st.spinner('Wait for it... Generating Satellite Image'):
        satImage, isError, messages = getSatelliteImage(latitudes=latitude, longitudes=longitude, zoomLevel=zoomLevel)
        st.subheader("Satellite Image Result")
        if isError == True:
            st.text(messages)
        else:
            imageSatelliteHolder = st.empty() 
            imageSatelliteHolder.image(satImage)
            st.text(messages)
    
    with st.spinner('Wait for it... Mapping Tambak Ikan'):
        processedSatImage, listAreaM, totalTambakIkan  = extractValue(satImage, latitude, zoomLevel)
        st.subheader("Satellite Image Result")
        imageDetectedHolder = st.empty() 
        imageDetectedHolder.image(processedSatImage)
        st.text(f"List of Tambak Ikan and its Estimated Area Calculation. Total Tambak Ikan: {totalTambakIkan}")
        df = pd.DataFrame.from_dict(listAreaM, orient="index", columns=["Approximately Area in Square Meters"])
        st.dataframe(df)
        