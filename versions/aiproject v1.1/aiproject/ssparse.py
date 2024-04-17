import time
import pyautogui


import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = (r"C:\Program Files\Tesseract-OCR\tesseract.exe")

def find(png, conf=0.85):
    return(pyautogui.locateCenterOnScreen(f'{png}.png', confidence=conf))

def click(png, conf=0.85):
    pyautogui.click(find(png, conf))

click('blank')
pyautogui.hotkey('ctrl', 'a')
pyautogui.hotkey('ctrl', 'c')
time.sleep(1)
pyautogui.click()
pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
pyautogui.press('esc')