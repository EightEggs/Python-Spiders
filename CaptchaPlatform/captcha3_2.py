from chaojiying import Chaojiying

import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import io


def cv2_add_text(image, text, left, top, textColor=(255, 0, 0), text_size=20):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('simsun.ttc', text_size, encoding="utf-8")
    draw.text((left, top), text, textColor, font=font)
    return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)


USERNAME = 'Germey'
PASSWORD = ''
SOFT_ID = '915502'
CAPTCHA_KIND = '9101'
FILE_NAME = 'captcha3.png'
image = cv2.imread(FILE_NAME)
image = cv2_add_text(image, '请点击目标滑块左上角', int(
    image.shape[1] / 10), int(image.shape[0] / 2), (255, 0, 0), 40)
client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
result = client.post_pic(io.BytesIO(cv2.imencode(
    '.png', image)[1]).getvalue(), CAPTCHA_KIND)
print(result)
