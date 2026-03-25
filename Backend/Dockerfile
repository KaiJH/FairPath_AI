# 使用輕量級 Python 映像檔
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 複製依賴清單並安裝
# 這裡包含解決 proxies 與 httpx 相容性的套件 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製後端所有程式碼 (包含 main.py 與 app/ 目錄)
COPY . .

# 暴露 FastAPI 預設埠號
EXPOSE 8000

# 啟動後端服務
# 使用 main.py 作為進入點，並載入環境變數 
CMD ["python", "main.py"]