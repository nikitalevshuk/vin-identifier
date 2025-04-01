from openai import OpenAI
from app.config import settings
from app.logger import get_logger
import base64


client = OpenAI(
    api_key=settings.QWEN_API_KEY,
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)
logger = get_logger(__name__)

def encode_image(image_bytes: bytes):
    logger.info("Началась работа функции encode_image")
    return base64.b64encode(image_bytes).decode("utf-8")

test_prompt = """
🔹 **Задача**: Найди и прочитай VIN-код на изображении.  
- VIN-код всегда состоит из **17 символов** (буквы A-Z, цифры 0-9, но **без I, O, Q**).   

🔹 **Точность превыше всего!**  
- Если символ плохо виден, используй **максимальный контекст изображения**.  
- Учитывай **физические характеристики** VIN-кодов: их шрифт, расположение, контрастность.  
- Если несколько символов похожи, выбери **наиболее вероятный вариант**.  

🔹 **Будь особенно внимателен к сложным случаям**:  
- **B** и **8** (не путай!)  
- **S** и **5**  
- **G** и **6**  
- **C** и **G**  
- **N** и **H**  
- **V** и **Y**  
- **J не должна пропадать!**  
- **VIN всегда 17 символов – не больше, не меньше!**  

Пусть в ответе будет только VIN номер.
"""

async def qwen_get_vin(image_bytes: bytes):
    logger.info("Началась работа функции qwen_get_vin")
    completion = await client.chat.completions.create(
        model="qwen2.5-vl-7b-instruct",
        messages=[
            {
                "role": "system",
                "content": [{"type": "text", "text": f"{test_prompt}"}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(image_bytes)}"
                        },
                    },
                ],
            },
        ],
    )

    return completion.choices[0].message.content