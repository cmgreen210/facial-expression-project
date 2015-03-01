import cv2


def resize(image, fx, fy):
    return cv2.resize(image, (0, 0), fx=fx, fy=fy)


def convert_to_grey_scale(path):
    image = cv2.imread(path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def save_to_file(image, path):
    cv2.imwrite(path, image)


#
# if __name__ == '__main__':
#     gray_sg = convert_to_grey_scale('data/sg.jpg')
#     gray_sg = resize(gray_sg, .25, .25)
#     save_to_file(gray_sg, 'data/sg.png')
