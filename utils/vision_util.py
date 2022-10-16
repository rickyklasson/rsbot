import random
import cv2

def get_object_point(img_path: str, img_offset: tuple, mask_color: tuple):
    # Read image and create color mask.
    img = cv2.imread(img_path)
    masked_img = cv2.inRange(img, mask_color, mask_color)

    #cv2.imshow('Image', masked_img)
    #cv2.waitKey(0)
    
    # Find contours of mask.
    contours, _ = cv2.findContours(image=masked_img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

    # Debug, visualize the contours.
    #img_copy = img.copy()
    #cv2.drawContours(img_copy, contours, -1, color=(255, 255, 255), thickness=cv2.FILLED)
    #cv2.drawContours(image=img_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #cv2.imshow('Contours', img_copy)
    #cv2.waitKey(0)


    # Randomize a contour and get its bounding rect.
    print(f'Found {len(contours)} contours')
    if len(contours) == 0:
        return None

    choice_idx = random.randrange(len(contours))
    chosen_cont = contours[choice_idx]
    rect_x, rect_y, rect_w, rect_h = cv2.boundingRect(chosen_cont)

    print(rect_x, rect_y, rect_w, rect_h)

    # Find a point in the contour bounding rect and check that its really in the contour.
    while True:
        x = random.randint(rect_x, rect_x + rect_w)
        y = random.randint(rect_y, rect_y + rect_h)

        val = cv2.pointPolygonTest(chosen_cont, (x, y), False)
        if val >= 0:
            return (x + img_offset[0], y + img_offset[1])
    
def check_inv_empty(img_path: str):
    pass
