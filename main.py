import os
import sys
import cv2

def read_folder_contents(folder_path):
    contents = []
    for path in os.listdir(folder_path):
        full_path = os.path.join(folder_path, path)
        if path.startswith("."):
            continue

        if os.path.isfile(full_path):
            contents.append(full_path)
    
    return contents

def image_center(image):
    height, width, _ = image.shape
    return int(height/2), int(width/2)

def resize(watermark):
    print('Original Dimensions : ',watermark.shape)

    width = int(watermark.shape[1] * 60 / 100)
    height = int(watermark.shape[0] * 60 / 100)
    dim = (width, height)

    resized = cv2.resize(watermark, dim, interpolation = cv2.INTER_AREA)
    print('Resized Dimensions : ',resized.shape)

    return resized

def show(img):
    cv2.imshow("Invert1",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def append_watermark_to_image(name, image, watermark_image):
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    resized_watermark = resize(watermark_image)
    height, width, _ = image.shape
    center_y, center_x = image_center(image)

    watermark_height, watermark_width, _ = resized_watermark.shape

    # calculating from top, bottom, right and left
    top_y = center_y - int(watermark_height/2)
    bottom_y = top_y + watermark_height
    left_x = center_x - int(watermark_width/2)
    right_x = left_x + watermark_width
    
    destination = image[top_y:bottom_y, left_x:right_x]
    result = cv2.addWeighted(destination, 1, resized_watermark, 0.1, 0)
    image[top_y:bottom_y, left_x:right_x] = result

    cv2.imwrite(name + "watermarked.jpg", image)
    cv2.destroyAllWindows()

def run_watermark(folder_path, watermark_path):
    contents = read_folder_contents(folder_path)
    watermark_image = cv2.imread(watermark_path)
    watermark_image = cv2.bitwise_not(watermark_image)
    for image_path in contents:
        loaded_image = cv2.imread(image_path)
        image_name = os.path.splitext(image_path)[0]
        append_watermark_to_image(image_name, loaded_image, watermark_image)


[folder_path, watermark_path] = sys.argv[1:]
run_watermark(folder_path, watermark_path)
    