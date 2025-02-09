import streamlit as st
import pandas as pd
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import dotenv_values
from pypdf import PdfReader
import json
import requests
import base64
import google.generativeai as genai
import hashlib
import datetime as dt
import random
import string
import os

class SheetManager:

    @staticmethod
    def authenticate_google_sheets():
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.getenv('GS_KEYS')), scope)
        client = gspread.authorize(creds)
        return client
    
    @staticmethod
    def extract_sheet_id(sheet_url):
        try:
            return sheet_url.split("/d/")[1].split("/")[0]
        except IndexError:
            st.error("無效的試算表連結，請檢查 URL 格式。")
            return None
        
    @staticmethod
    def fetch(client, sheet_id, worksheet):
        if sheet_id:
            try:
                sheet = client.open_by_key(sheet_id)
                ws = sheet.worksheet(worksheet)
                data = ws.get_all_records()
                
                return pd.DataFrame(data)
            except:
                st.write("Connection Failed")

    @staticmethod
    def insert_rows(client, sheet_id, worksheet, rows: list):
        if sheet_id:
            try:
                sheet = client.open_by_key(sheet_id)
                worksheet = sheet.worksheet(worksheet)
                worksheet.freeze(rows = 1)
                worksheet.append_rows(rows)

                records = worksheet.get_all_records()
                
            except Exception as e:
                st.write(f"Connection Failed: {e}")

client = SheetManager.authenticate_google_sheets()
print(SheetManager.fetch(client, SheetManager.extract_sheet_id('https://docs.google.com/spreadsheets/d/1-0oYvj2aB4zVrb_DLZn4sDWSytScoy6cgXrDqqflOhI/edit?gid=0#gid=0'), 'ws1'))