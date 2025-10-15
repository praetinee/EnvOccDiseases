import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Function to connect to Google Sheets
def connect_to_gsheet():
    """Establishes a connection to the Google Sheet using credentials from st.secrets."""
    try:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        client = gspread.authorize(creds)
        # --- IMPORTANT CORRECTION ---
        # The name inside client.open() MUST EXACTLY match your Google Sheet file name.
        # Please double-check the name of your file in Google Drive.
        spreadsheet = client.open("EnvOccDiseasesDB") # Example name, replace with your actual file name
        return spreadsheet
    except gspread.exceptions.SpreadsheetNotFound:
        st.error("ไม่พบไฟล์ Google Sheet: 'EnvOccDiseasesDB'. กรุณาตรวจสอบว่าชื่อไฟล์ถูกต้องและได้แชร์อีเมล Service Account ให้เป็น Editor แล้ว")
        return None
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อกับ Google Sheets: {e}")
        return None

# Function to save data to a specific sheet (tab)
def save_to_sheet(sheet_name, form_data):
    """
    Saves the form data to the specified worksheet.
    The worksheet must have headers in the first row that match the keys in form_data.
    """
    spreadsheet = connect_to_gsheet()
    if not spreadsheet:
        return

    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        
        # Get headers from the sheet to ensure correct order
        headers = worksheet.row_values(1)
        
        # Add a timestamp for the submission
        form_data_with_timestamp = form_data.copy()
        form_data_with_timestamp['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new row with data in the order of the headers
        # Use .get(header, "") to avoid errors if a key is missing; it will leave the cell blank.
        if 'timestamp' not in headers:
            headers.append('timestamp')
            
        new_row = [form_data_with_timestamp.get(header, "") for header in headers]
        
        # Append the new row to the sheet
        worksheet.append_row(new_row)
        
        return True # Indicate success
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"ไม่พบแท็บชีตชื่อ '{sheet_name}' ใน Google Sheet ของคุณ กรุณาตรวจสอบว่าสร้างแท็บและตั้งชื่อตรงกันแล้ว")
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการบันทึกข้อมูล: {e}")
    
    return False # Indicate failure
