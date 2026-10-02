import streamlit as st 
import pandas as pd
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components
import sys
import os

st.set_page_config(page_title="Data Profiler",layout="wide", page_icon="pageicon.webp")

#we define a function in a way to identify the extension of the file and verify it
def validate_file(file):
    filename=file.name
    name,ext=os.path.splitext(filename)
    if ext in (".csv",".xlsx"):
        return ext
    else:
        return False
def file_size(file):
    size_bytes=sys.getsizeof(file)
    size_mb=size_bytes/(1024**2)
    return size_mb

#Creation of the sidebar
with st.sidebar:
    upload_file=st.file_uploader("Upload a .csv, .xlsx files not exceeding 10 MB")
    #we add the possibility for the user to choose the color and o minimize the large amount of output in a smaller view
    st.write("Models of Operatons")
    minimal=st.checkbox("Check if you want a minimal report")
    displaymode=st.radio("Display color mode:", options=("Dark", "Orange"))
    if displaymode == "Orange":
        pr1 = ["#ff6f00"]
    elif displaymode == "Dark":
        pr1 = ["#141414"]

if upload_file is not None:
    ext=validate_file(upload_file)
    if ext: 
        filesize=file_size(upload_file)
        if filesize <= 10:
            if ext==".csv":
                df=pd.read_csv(upload_file)
            else:
                df=pd.ExcelFile(upload_file)
                sheet_tuple=tuple(df.sheet_names)
                sheet_name=st.sidebar.selectbox("Select the sheet", sheet_tuple)
                df= df.parse(sheet_name)
    
            st.dataframe(df.head())
            #generate report
            with st.spinner("Generating report"):
                pr=ProfileReport(df , minimal=minimal)
            pr.config.html.style.primary_colors = pr1
            st.iframe(pr.to_html(),height=1200)
        else: 
            st.error("Maximum allowed filesize is 10 MB. But recieved is {filsesize} MB ")    
    else:
        
        st.error("Kindly upload csv or xlsx files")
else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate profiling")