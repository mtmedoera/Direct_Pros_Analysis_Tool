#https://colab.research.google.com/drive/1eD_GnE-ffyYeR4vy857d2FrRDSEbaPNO#scrollTo=T1O3FFTkjgyo

import re
import fitz  # PyMuPDF
import streamlit as st

#テキストデータ抽出
#-----------------------------------------------------------------------------
def extract_text_from_pdf(temp_file_path):

    text_data = ""

    with fitz.open(temp_file_path) as doc:
    
        num_pages = doc.page_count
        for page_num in range(num_pages):
            page = doc[page_num]
            text_data += page.get_text()
    return text_data
        
# テキストファイルのうち「投資方針」の項目を抽出
#------------------------------------------------------------------------------
def investment_policy (text_data):

    Start_Inv_Policy = text_data.find("【投資方針】")
    Char_Fund = text_data.find("ファンドの特色")    

    extracted_text = ""
    extracted_text2 = ""
    extracted_text3 = ""

    if Start_Inv_Policy !=  -1:
        st.write("「投資方針」より")
        next_section_match = re.search(r'＜.*＞|\n\s*\n', text_data[Start_Inv_Policy:])
        end_index = next_section_match.start() if next_section_match else len(text_data)
        extracted_text = text_data[Start_Inv_Policy:Start_Inv_Policy + end_index].strip()

    if Char_Fund !=  -1:
        st.write("「ファンドの特色」より")
        next_section_match = re.search(r'＜.*＞|\n\s*\n', text_data[Char_Fund:])
        end_index = next_section_match.start() if next_section_match else len(text_data)
        extracted_text2 = text_data[Char_Fund:Char_Fund + end_index].strip()

    if Start_Inv_Policy ==  -1 and Char_Fund ==  -1:
        st.write("pdf全文より")
        extracted_text3 = text_data[Start_Inv_Policy:1 + end_index].strip()        

    text2gemini = extracted_text + extracted_text2 + extracted_text3
    text2gemini = text2gemini[:5000]

    return text2gemini
#-----------------------------------------------------