import pyautogui
import keyboard
from PIL import ImageGrab

# jump position: x = 199, y = 417
# debug position: x = 536 y =  434
# "white" pixels: RGB: (247, 247, 247)
# "black" pixels: RGB: (83, 83, 83)
x = 199*2
y = 417*2

while True: 
    im = pyautogui.screenshot(region=(190*2,410*2, 210*2,420*2)) 
    pixel_value = im.getpixel((199*2, 417*2))
    if pixel_value == (83, 83, 83):
        pyautogui.press('space')
        print("jumpy!")
    else:
        print("no match")
        print(pixel_value)