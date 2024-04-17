import pyautogui
import time
import pyperclip
import pathlib
import textwrap
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown
import PIL.Image

import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')

genai.configure(api_key='AIzaSyABHI0UfHDsy1b9oxV590WrfhXvqYcDW5Y')
generation_config = {
  'temperature': 0.8,
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
model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                              generation_config=generation_config,
                              safety_settings=safety_settings)
convo = model.start_chat(history=[
])

#---

def show(text, title):
    print(f'---\n{title} = {text}\n---')

def find(png, conf=0.85):
    return(pyautogui.locateCenterOnScreen(f'{png}.png', confidence=conf))

def click(png, conf=0.85):
    pyautogui.click(find(png, conf))

def checkfor(button, conf=0.85):
    try:
        find(button, conf)
        return(True)
    except:
        return(False)

def nextq():
    pyautogui.press('end')
    if checkfor('nextquestion'):
        click('nextquestion')
    elif checkfor('nextquestionsm'):
        click('nextquestionsm')
    elif checkfor('finish'):
        click('finish')
        yes = False
        while not yes:
            try:
                click('yes')
                yes = True
            except:
                time.sleep(1)
        print('Test Finished')
    else:
        print('Error: Could not locate button')

def nextpg():
    while not checkfor('strongmind'):
        time.sleep(1)
    if checkfor('yes'):
        click('yes')
    elif checkfor('start'):
        click('start')
    elif checkfor('next'):
        click('next', 0.92)
    else:
        pyautogui.press('end')

def qtype():
    if checkfor('check'):
        return('')
    elif checkfor('checks'):
        return('s')
    else:
        print('Error: Could not find checkboxes')

#---

def findboxes(type):
    boxes = []
    answers = []
    for box in pyautogui.locateAllOnScreen(f'check{type}.png', confidence=0.8):
        left = int(box.left + 20)
        width = int(find('topr').x - left)
        answer = pyautogui.screenshot(region=(left, int(box.top), width, 40))
        answer = pytesseract.image_to_string(answer).replace('\n','')
        if answer not in answers:
            answers.append(answer)
            boxes.append(box)
    
    #show(boxes, 'Boxes')
    #show(answers, 'OCR Responses')
    return(boxes, answers)


def filter(rawdata, filter):
    data = []
    for x in rawdata:
        if len(x) >> 0:
            while '   ' in x:
                x = x.replace('   ', '  ')
            if x.startswith(' '):
                x = x[1:]
            if x.endswith(' ') and not x.endswith('  '):
                x = x[:-1]
            y = x.split(filter)
            z = int(len(y)-1)
            x = y[z]
            if x == '' or x == ' ':
                z = int(len(y)-2)
                x = y[z]
            z = []
            for y in x:
                z.append(y)
            n = 0
            while n <= len(z):
                n += 1
                if z[0:n] == z[n:]:
                    x = x[n:]
            if x not in data:
                data.append(x)
    
    return(data)


def copyquestion():
    click('blank')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
    pyautogui.press('esc')

    question = pyperclip.paste().split('Question')[2].split('Skip')[0]
    responses = question.split('Responses')[1].split('\r\n\r\n')
    #show(responses, 'Raw Responses')
    responses = filter(responses, '\r\n')
    #show(responses, 'Filtered Raw Responses')
    responses = filter(responses, '  ')
    question = f'Question:{question.split('Responses')[0]}Respond with only the correct answer{qtype()} from the following options:\n{responses}'
    
    show(question.split('Respond')[0], 'Question')
    show(responses, 'Responses')
    return(question, responses)


def askai(question):
    convo.send_message(question)
    response = convo.last.text
    if '["' in response:
        response = convo.last.text.replace('["','').replace('"]','').split('", "')
    elif "['" in response:
        response = convo.last.text.replace("['","").replace("']","").split("', '")

    show(response, 'AI Response')
    return(response)


def select(response, responses, answers, boxes):
    test = True
    correct = []
    cbox = []
    [correct.append(x) for x in responses if x in response]
    if correct == []:
        print('Error: No correct anwers detected')
        responses = answers
        [correct.append(x) for x in responses if x in response]
    [cbox.append(boxes[responses.index(x)]) for x in responses if x in response]
    for x in cbox:
        show(x, 'Click')
        y = x.top + 13
        x = x.left + 10
        pyautogui.click(x, y)

    return(correct)


def solve():
    if checkfor('checkchk') or checkfor('checkschk'):
        show('Already Solved', 'Question')
        return()
    boxes, answers = findboxes(qtype())
    question, responses = copyquestion()
    response = askai(question)
    correct = select(response, responses, answers, boxes)
    show(correct, 'Correct Answer')


#---

try:
    click('strongmind')
    pyautogui.click(225, 150)
except:
    print('Error: Could not find tab')

while checkfor('chrome'):
    if checkfor('discussion'):
        input('Discussion Detected')
    elif checkfor('topr') or checkfor('botl'):
        solve()
        nextq()
    else:
        nextpg()