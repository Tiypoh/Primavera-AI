import pyautogui
import time
import pyperclip
import google.generativeai as genai
import PIL
from PIL import Image, ImageGrab 

import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')

genai.configure(api_key='AIzaSyABHI0UfHDsy1b9oxV590WrfhXvqYcDW5Y')
generation_config = {
  'temperature': 0.95,
  'max_output_tokens': 2048,
}
safety_settings = [
  {
    'category': 'HARM_CATEGORY_HARASSMENT',
    'threshold': 'BLOCK_NONE'
  },
  {
    'category': 'HARM_CATEGORY_HATE_SPEECH',
    'threshold': 'BLOCK_NONE'
  },
  {
    'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
    'threshold': 'BLOCK_NONE'
  },
  {
    'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
    'threshold': 'BLOCK_NONE'
  },
]

#---

def loadai(type):
    return(genai.GenerativeModel(model_name=f'{type}', generation_config=generation_config, safety_settings=safety_settings))
    
def show(title, text):
    print(f'---\n{title} = {text}\n---')

#-------------------------------------------------------------------------------------------


def copyquestion():
    pyautogui.click(200,200)
    pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
    pyautogui.press('esc'); pyautogui.press('end')
    question = 'Select the most correct answer from the following options for each part' + pyperclip.paste()
    return(question)


def askai(question):
    question = [question]
    model = loadai('gemini-pro')
    response = model.generate_content(question)
    response = response.text
    return(response)


def solve():
    question = copyquestion()
    correct = askai(question)

    show('Correct Answer', correct)
    return(correct)


#-------------------------------------------------------------------------------------------

solve()