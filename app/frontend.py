import streamlit
import requests
from config import settings


FASTAPI_URL = settings.FASTAPI_URL + "vin/"

streamlit.title("VIN-распознание")
streamlit.write("Загрузите фото VIN-номера, и система распознает его.")

uploaded_file = streamlit.file_uploader("Загрузите изображение", type=["jpg", "png", "jpeg"])

if uploaded_file:
    streamlit.image(uploaded_file, caption="Загруженное изображение", use_column_width=True)

    if streamlit.button("Распознать VIN"):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(FASTAPI_URL, files = {"file": uploaded_file})

        if response.status_code == 200:
            vin = response.json().get("vin", "VIN не найден")
            streamlit.success(f"✅ Распознанный VIN: `{vin}`")
        else:
            streamlit.error("❌ Не удалось распознать VIN. Попробуйте другое фото.")

