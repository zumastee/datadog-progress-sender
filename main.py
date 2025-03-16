import os
import time
import requests
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")

if not DATADOG_API_KEY:
    raise ValueError("DATADOG_API_KEY is not set in environment variables.")

# Datadog API URL
url = "https://api.ap1.datadoghq.com/api/v1/series"

# 進捗送信関数
def send_progress(progress: int):
    timestamp = int(time.time())
    payload = {
        "series": [
            {
                "metric": "custom.job.progress", # Datadog上で表示されるメトリクス名
                "points": [[timestamp, progress]], # 測定データ（時刻と値のペア） 
                "type": "gauge", #メトリクスの種類
                "host": "macbook-pro", # 送信元のホスト
                "tags": ["job:python-cursor"] # タグ。フィルタにつ
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 202:
        print(f"[OK] Progress {progress}% sent to Datadog.")
    else:
        print(f"[ERROR] Failed to send progress: {response.text}")

# 例: 5%ずつ進捗送信
if __name__ == "__main__":
    for progress in range(5, 101, 5):
        send_progress(progress)
        time.sleep(5)  # 5秒ごとに進捗を送信
        
