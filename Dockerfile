# 使用官方 Python 映像檔作為基底
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製需求檔案並安裝套件
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製程式碼
COPY answeragent.py ./

# 開放容器的 8080 埠口
EXPOSE 8080

# 使用 gunicorn 啟動 Flask app，綁定 0.0.0.0:8080，並設定工作執行緒數
CMD ["gunicorn", "-b", "0.0.0.0:8080", "--workers", "3", "answeragent:app"]
