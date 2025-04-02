@echo off
cd C:\Users\Laptopchik\web_data_pest_control
call C:\Users\Laptopchik\.virtualenvs\web_data_pest_control-M5_92B0w\Scripts\activate.bat
streamlit run main.py --server.port 8501 --server.headless true
pause

