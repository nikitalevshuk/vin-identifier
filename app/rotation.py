import PIL.ImageFile
from openai import AsyncOpenAI
from app.config import settings
from app.logger import get_logger
from PIL import Image
from io import BytesIO
import base64

client = AsyncOpenAI(
    api_key=settings.OPENAI_API_KEY
)

logger = get_logger(__name__)
PIL.ImageFile.LOAD_TRUNCATED_IMAGES = True


async def get_rotation_angle(image_bytes: bytes) -> str:
    logger.info("Отправляем в gpt-4o фотографию")
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "На сколько градусов и в каком направлении (по или против "
                                "часовой стрелки) нужно повернуть изображение, чтобы текст на "
                                "нём был читаем слева направо, горизонтально? Укажи в ответе"
                                " только угол поворота по часовой стрелке(без точки), если"
                                " поворачивать картинку не нужно(или текста на ней нет), то"
                                " ответь 0"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                        }}
                ]
            }
        ]
    )

    logger.info(f"Получили ответ от gpt-4o: {response.choices[0].message.content}")
    return response.choices[0].message.content

def rotate_image(image_bytes: bytes, angle: int) -> bytes:
    logger.info(f"Началось выполнение функции rotate_image, переворачиваем на {angle} "
                 "градусов")
    image_buffer = BytesIO(image_bytes)
    with Image.open(image_buffer) as pil_image:
        rotated_pil_image = pil_image.rotate(angle=angle)
        image_buffer = BytesIO()
        format = rotated_pil_image.format if rotated_pil_image.format else "JPEG"
        rotated_pil_image.save(image_buffer, format=format)
        logger.info("Первернули картинку, отправляем байты дальше")
        image_buffer.seek(0)
        response = image_buffer.read()

        return response

