import streamlit as st
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import os
import PyPDF2
import tempfile
import requests

from model import extract_text_from_pdf, investment_policy  # model.py の関数をインポート

temp_file_path = None  # グローバル変数として宣言

#投資経験スライダー
#------------------------------------------------------------------
def show_sidebar():
    st.sidebar.markdown("<h1 style='color: blue;'>投資経験</h1>", unsafe_allow_html=True)

    ## スライダーによる値の動的変更
    condition = st.sidebar.slider('', 0, 4, 2, format="%d")

    # 特定の値に対してカスタムな表示
    if condition == 4:
        label = 'これで生計立ててます'
        condition_text = "私はプロ投資家。投資性向は「ハイリスクハイリターン」か「ベア型投資」か「珍しい投資手法（商品投資やデリバティブなど）」のいずれかであり、かつG7やG20の国には投資しません。短期の絶対収益を追求しますが長期投資はしません。"
    
    elif condition == 3:
        label = 'アマチュアだけど、自信あり'
        condition_text = "私はアマチュアですが投資経験と実績は豊富です。私の投資性向は「ミドルリスクミドルリターン」か「●倍の動きをするファンド（G7やG20の証券以外を希望）」か「珍しい投資手法（商品や現物やデリバティブなど）」です。長期か短期かは問いません。それ以外は推奨しないでください。先進国債券投資は絶対に嫌です。"
    
    elif condition == 2:
        label = 'そこそこ...'
        condition_text = "私は一般的な投資家で、投資経験は長いですがあまり細かく状況確認はしません。す。私の投資性向は、「ミドルリスクミドルリターンかローリスクローリターン」かつ「長期投資」か「リスクが一定程度に抑えられた分かりやすい投資」です。G20までの投資を希望します。それ以外は推奨しないでください。"
    
    elif condition == 1:
        label = '経験あるけど、自信がない'
        condition_text = "私は経験の少ない投資家です。す。私の投資性向は、「ローリスクローリターン」かつ「長期投資」かつ「インデックスに連動し」かつ「リスクが一定程度に抑えられた分かりやすい投資」かつ「G7への投資」です。それ以外は推奨しないでください。"
    
    else :
        label = '経験ゼロ'
        condition_text = "私は経験がありません。私の投資性向は、とにかく安全。よくわからないものには投資したくないです。「ローリスクローリターン」かつ「長期投資」かつ「有名なインデックスに連動し」かつ「G7への投資」かつ「為替リスクをヘッジする」投資です。それ以外は投資しません。"

    st.sidebar.write('レベル：', label)

    return condition, condition_text
#------------------------------------------------------------------


#pdfドラッグ&ドロップ
#------------------------------------------------------------------
def show_pdf_upload():
    st.sidebar.markdown("<h1 style='color: blue;'>PDFアップロード</h1>", unsafe_allow_html=True)
    # サイドバーにファイルアップロードを配置
    uploaded_file = st.sidebar.file_uploader("PDFファイルをドラッグのあと、「特徴をみる」ボタンを押下", type=["pdf"])

    return uploaded_file

    st.write(uploaded_file)

#処理開始用ボタン
#------------------------------------------------------------------
def show_button_read_pdf(button_label, uploaded_file, condition_text):
    with st.form(key="upload_file"):
        if uploaded_file is not None:
            
            st.write("ファイルアップロード完了")
            button_pressed = st.form_submit_button("特徴をみる")
        
            if button_pressed:

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name
                
                # PDFファイルの読み込み
                pdf_reader = PyPDF2.PdfReader(temp_file_path)

                #フォルダパスの取得
                folder_path = os.path.dirname(temp_file_path)
                
                # テキストデータの抽出
                text_data = extract_text_from_pdf(temp_file_path)
                text2gemini = investment_policy(text_data)

                # ここでsummaryを定義する
                summary = {
                    "text2gemini": text2gemini,
                    "condition_text": condition_text
                }

                url = "http://localhost:8000/summary"
                data_to_send = {"text2gemini": text2gemini, "condition_text": condition_text}
                response = requests.post(url, json=data_to_send)

                if response.status_code == 200:
                    response_json = response.json()
                    st.write(response_json)

                else:
                    # エラーが発生した場合の処理
                    st.error("サーバーからの応答が無効です")

        else:
            st.session_state.button_pressed = False
            button_pressed = False


# タイトルとテキストを記入
st.title('ファンドの特徴をみる')
st.write('サイドバーで「投資経験」と「PDFアップロード」のあと、「特徴をみる」')
st.text("==================================================================================\n\n")

# サイドバーの表示
condition, condition_text = show_sidebar()
uploaded_file = show_pdf_upload()
response = show_button_read_pdf("特徴をみる", uploaded_file, condition_text)
