import pyautogui

im = pyautogui.screenshot(region=(190*2,410*2, 210*2,420*2)) 
im.save('test.png')