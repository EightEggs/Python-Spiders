from chaojiying import Chaojiying

# USERNAME = ''
# PASSWORD = ''
# SOFT_ID = '915502'
# CAPTCHA_KIND = '9004'
# FILE_NAME = 'captcha2.png'
# client = Chaojiying(USERNAME, PASSWORD, SOFT_ID)
# result = client.post_pic(open(FILE_NAME, 'rb').read(), CAPTCHA_KIND)
# print(result)

import cv2

image = cv2.imread('captcha2.png')
image = cv2.circle(image, (108, 133), radius=10, color=(0, 0, 255), thickness=-1)
image = cv2.circle(image, (227, 143), radius=10, color=(0, 0, 255), thickness=-1)
cv2.imwrite('captcha2_label.png', image)
