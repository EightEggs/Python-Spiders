import cv2


image = cv2.imread('captcha3.png')
image = cv2.circle(image, (167, 55), radius=10, color=(0, 0, 255), thickness=-1)
cv2.imwrite('captcha3_label.png', image)
