import streamlit as st 
import pandas as pd
import sweetviz as sv
import streamlit.components.v1 as components
import sys
import os

st.set_page_config(page_title="Data Profiler", layout="wide", page_icon="pageicon.webp")

# Validate extension
def validate_file(file):
    filename = file.name
    name, ext = os.path.splitext(filename)
    if ext in (".csv", ".xlsx"):
        return ext
    else:
        return False

# File size
def file_size(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

# Sidebar
with st.sidebar:
    upload_file = st.file_uploader("Upload a .csv or .xlsx file (max 10 MB)")
    st.write("Models of Operations")
    minimal = st.checkbox("Check if you want a minimal report")
    displaymode = st.radio("Display color mode:", options=("Dark", "Orange"))

    if displaymode == "Orange":
        pr1 = "#ff6f00"
    elif displaymode == "Dark":
        pr1 = "#141414"

# Main logic
if upload_file is not None:
    ext = validate_file(upload_file)
    if ext:
        filesize = file_size(upload_file)
        if filesize <= 10:
            if ext == ".csv":
                df = pd.read_csv(upload_file)
            else:
                excel_file = pd.ExcelFile(upload_file)
                sheet_tuple = tuple(excel_file.sheet_names)
                sheet_name = st.sidebar.selectbox("Select the sheet", sheet_tuple)
                df = excel_file.parse(sheet_name)

            st.dataframe(df.head())

            # Generate Sweetviz report
            with st.spinner("Generating report..."):
                report = sv.analyze(df)

                # Apply minimal mode
                if minimal:
                    report = sv.analyze(df, feat_cfg=sv.FeatureConfig(skip="ALL"))

                # Generate HTML
                report_path = "sweetviz_report.html"
                report.show_html(report_path, open_browser=False)

            # Display report inside Streamlit
            with open(report_path, "r", encoding="utf-8") as f:
                html_report = f.read()

            components.html(html_report, height=1200, scrolling=True)

        else:
            st.error(f"Maximum allowed filesize is 10 MB. Received: {filesize:.2f} MB")
    else:
        st.error("Kindly upload csv or xlsx files")
else:
    st.title("Data Profiler")
    st.info("Upload your data in the left sidebar to generate profiling")
