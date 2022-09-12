import cv2

GAUSSIAN_BLUR_SIZE = (3, 5)
GAUSSIAN_BLUR_SIGMA = 0
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 450


def gaussian_blur(image):
    return cv2.GaussianBlur(image, GAUSSIAN_BLUR_SIZE, GAUSSIAN_BLUR_SIGMA)


def canny_edge_detect(image):
    return cv2.Canny(image, CANNY_THRESHOLD1, CANNY_THRESHOLD2)


def get_contours(image):
    contours, _ = cv2.findContours(
        image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_contour_area(image_width, image_height):
    contour_area_min = (image_width * 0.15) * (image_height * 0.25) * 0.8
    contour_area_max = (image_width * 0.15) * (image_height * 0.25) * 1.2
    return contour_area_min, contour_area_max


def get_arc_length(image_width, image_height):
    arc_length_min = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 0.8
    arc_length_max = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 1.2
    return arc_length_min, arc_length_max


def get_offset(image_width):
    offset_min = 0.2 * image_width
    offset_max = 0.85 * image_width
    return offset_min, offset_max


if __name__ == '__main__':
    # Read in the image
    image_raw = cv2.imread('captcha.png')
    height, width, _ = image_raw.shape

    # Process the image
    image_gaussian_blur = gaussian_blur(image_raw)
    image_canny = canny_edge_detect(image_gaussian_blur)
    contours = get_contours(image_canny)

    # Write out the process results
    cv2.imwrite('gaussian_blur.png', image_gaussian_blur)
    cv2.imwrite('canny.png', image_canny)

    # Constraint checking
    contour_area_min, contour_area_max = get_contour_area(width, height)
    arc_length_min, arc_length_max = get_arc_length(width, height)
    offset_min, offset_max = get_offset(width)
    offset = None

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if contour_area_min < cv2.contourArea(contour) < contour_area_max and \
                arc_length_min < cv2.arcLength(contour, True) < arc_length_max and \
                offset_min < x < offset_max:
            cv2.rectangle(image_raw, (x, y), (x + w, y + h), (0, 0, 255), 2)
            offset = x

    cv2.imwrite('image_label.png', image_raw)
    print('offset', offset)
