from fastapi import FastAPI, UploadFile, File, HTTPException
from app.logger import get_logger
from app.vin_reader import qwen_get_vin
from app.vin_validator import check_vin

app = FastAPI()
logger = get_logger(__name__)

@app.post("/vin/")
async def recognize_vin(file: UploadFile = File(...)):
    try:
        logger.info("Началась работа /vin/ эндпоинта")

        image_bytes = await file.read()
        logger.info(str(image_bytes))

        vin = await qwen_get_vin(image_bytes)

        vin_valid = check_vin(vin)

        if vin_valid:
            return {"vin": vin, "isValid": vin_valid}
        else:
            return {"vin": 0, "isValid": vin_valid}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обработки: {e}")