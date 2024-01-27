#streamlit run app.py ; uvicorn main:app --reload
#Start-Process "cmd.exe" -ArgumentList "/k streamlit run app.py ; uvicorn main:app --reload"
#https://github.com/mtmedoera/pros_analysis_tool.git
#git@github.com:mtmedoera/pros_analysis_tool.git

from fastapi import FastAPI
from pydantic import BaseModel
import os
from pydantic import BaseModel
import google.generativeai as genai


app = FastAPI()

class RequestData(BaseModel):
    text2gemini: str
    condition_text: str

# トップページ
@app.get('/')
async def index(title):
    return {"Reading": 'read_disclosure'}

# POST が送信された時（入力）と予測値（出力）の定義
@app.post("/summary")
async def gemini_contact(request_data: RequestData):
    text2gemini = request_data.text2gemini
    condition_text = request_data.condition_text

    os.environ['GOOGLE_API_KEY'] = 'AIzaSyBtnV5l0VgMYie0sviM5nrgsNxL1UwBCfY'
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name='gemini-pro')
    chat = model.start_chat()

    response_text = chat.send_message(
    '最下部記載のファンドについて、以下の項目の情報をください '
    'あなたはファンドに詳しい優秀な証券会社の販売員です。ディスクレーマーを言ってはいけません。'
    'ポイントを「箇条書き」で「項目ごと」に「改行して」「下記の順」に教えてください。'
    'ⅰとⅱは必ず回答してください'
    
    '・【ⅰ．総合推奨度】私の投資性向にあったこのファンドの総合推奨度を★1～5段階（5が最大）で星の数で回答してください。ただし、下記の私の投資性向に合致する回答をお願いします。'
    '（改行）'

    '【ⅱ．特徴】80～100字でファンドの特徴を高校生でも理解できるよう簡記してください。その際は下記項目は触れず、推奨度の理由や背景を説明してください'
    '（改行）'

    '・ⅲ．推奨投資期間　：　（短期投資向けか、長期投資向けか）'
    '（改行）'
    '・ⅳ．主要投資商品　：　（株か、債券か、先物か、デリバティブか、その他か）ここはかなり重要なので確り確認してください。'
   '（改行）'
    '・ⅴ．主要投資国　：　（主要5か国まで記載）'
   '（改行）'
    '・ⅵ.主要投資通貨および為替ヘッジの有無　：　（主要5通貨まで記載）'
   '（改行）'
    '・ⅶ.収益タイプ：　ハイリスク・ハイリターン　か　ミドルリスク・ミドルリターン　か　ローリスク・ローリターンか'
   '（改行）'
    '・ⅷ.対象インデックス　：　（あれば記載、なければ「なし」）'    
    + condition_text + "   " + text2gemini
)

    return response_text.text
#-----------------------------------------------------
