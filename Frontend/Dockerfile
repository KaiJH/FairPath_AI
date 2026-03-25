FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# 🚀 啟動指令：加入關閉 CORS 的參數，確保在反向代理下能正常運作
CMD ["streamlit", "run", "Info_Submission🙋‍♂️🙋‍♀️.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]