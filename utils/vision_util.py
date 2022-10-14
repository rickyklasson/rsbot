import random
import cv2

def find_object_points(img_path: str, img_offset: tuple, mask_color: tuple):
    img = cv2.imread(img_path)
    img_w = img.shape[1]
    img_h = img.shape[0]
    
    masked_img = cv2.inRange(img, mask_color, mask_color)

    #cv2.imshow('Image', thresh)
    #cv2.waitKey(0)
    
    contours, _ = cv2.findContours(image=masked_img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

    # Debug, visualize the contours.
    #img_copy = img.copy()
    #cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #cv2.imshow('Contours', img_copy)
    #cv2.waitKey(0)

    ret_points = []

    for contour in contours:
        # Find a point in the contour.
        while True:
            x = random.randint(0, img_w)
            y = random.randint(0, img_h)
            val = cv2.pointPolygonTest(contour, (x, y), False)
            if val >= 0:
                ret_points.append((x + img_offset[0], y + img_offset[1]))
                break
    
    return ret_points

def check_inv_empty(img_path: str):
    pass
