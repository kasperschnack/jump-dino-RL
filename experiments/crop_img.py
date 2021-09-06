import cv2

# 285,190
# 114, 39
# x, y, w, h
look_zone = 285, 190, 114, 39

im = cv2.imread("screendump.png")

crop_img = im[
    look_zone[1] : look_zone[1] + look_zone[3],
    look_zone[0] : look_zone[0] + look_zone[2],
]

cv2.imshow("Game", crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
