import cv2

GAME_CORNER_DIST_FROM_TEMPLATE = 435
GAME_WIDTH = 600
GAME_HEIGHT = 130


rex_game_img = cv2.imread("rex_games.png")

template = cv2.imread("hi.png")
h, w, dims = template.shape
res = cv2.matchTemplate(rex_game_img, template, cv2.TM_CCOEFF_NORMED)

_, max_val, _, max_loc = cv2.minMaxLoc(res)

game_corner = max_loc[0] - GAME_CORNER_DIST_FROM_TEMPLATE

# draw a rectangle around the template
# cv2.rectangle(rex_game_img, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)

crop_img = rex_game_img[
    max_loc[1] : max_loc[1] + GAME_HEIGHT, game_corner : game_corner + GAME_WIDTH
]

cv2.imshow("Game", crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("game_screen.png", crop_img)
