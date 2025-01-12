# from flask_ngrok import run_with_ngrok   # colab 使用，本機環境請刪除
from flask import Flask, request
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)               # 印出 json_data
    return 'OK'

if __name__ == "__main__":
    # run_with_ngrok(app)        # colab 使用，本機環境請刪除
    app.run()