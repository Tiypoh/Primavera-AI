import pyautogui
import time
import pyperclip
import google.generativeai as genai
import PIL.Image

import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')

genai.configure(api_key='AIzaSyABHI0UfHDsy1b9oxV590WrfhXvqYcDW5Y')
generation_config = {
  'temperature': 0.9,
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

def vision():
    return(genai.GenerativeModel(model_name='gemini-pro-vision', generation_config=generation_config, safety_settings=safety_settings))

def text():
    return(genai.GenerativeModel(model_name='gemini-pro', generation_config=generation_config, safety_settings=safety_settings))
    
def show(text, title):
    print(f'---\n{title} = {text}\n---')

def find(png, conf=0.85):
    return(pyautogui.locateCenterOnScreen(f'img/{png}.png', confidence=conf))

def findcorner(png, conf=0.85):
    return(pyautogui.locateOnScreen(f'img/{png}.png', confidence=conf))

def click(png, conf=0.85):
    pyautogui.click(find(png, conf))

def checkfor(button, conf=0.85):
    try:
        find(button, conf)
        return(True)
    except:
        return(False)

def percentage():
    perc = findcorner('percentage')
    left = int(perc.left)
    top = int(perc.top - 30)
    width = int(perc.width)
    height = 30
    percentage = int(pytesseract.image_to_string(pyautogui.screenshot(region=(left, top, width, height))))
    show(percentage, 'Percentage')
    return(percentage)

def checkans():
    x=True
    while x:
        if checkfor('botlfaded'):
            x = False
            return()
        if checkfor('checkchk') or checkfor('checkschk'):
            try:
                click('botl')
            except:
                click('botl')
        else:
            solve()

def finish():
    x = True
    while x:
        if checkfor('yes'):
            if not checkfor('unanswered'):
                click('yes')
                while x:
                    if checkfor('percentage'):
                        x = False
                        if percentage() <= 60:
                            click('retake')
                    else:
                        time.sleep(0.1)
            else:
                click('no')
                checkans()
            return()
        else:
            time.sleep(1)

def nextq():
    pyautogui.press('end')
    if checkfor('nextquestion'):
        click('nextquestion')
    elif checkfor('nextquestionsm'):
        click('nextquestionsm')
    elif checkfor('finish'):
        click('finish')
        print('Test Finished')
    else:
        print('Error: Could not locate button')

def nextpg():
    while not checkfor('strongmind'):
        time.sleep(1)
    if checkfor('start'):
        if checkfor('SEL'):
            try:
                click('next', 0.92)
            except:
                pyautogui.press('end')
        else:
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

def parseimage():
    x=True
    while x:
        try:
            side = find('topr')
            x=False
        except:
            pyautogui.scroll(1)
    left = int(findcorner('listen').left)
    top = int(find('listen').y)
    width = int(findcorner('listen').left)
    height = int(find('copywright').y - find('listen').y)
    image = pyautogui.screenshot(region=(left, top, width, height))
    pyautogui.press('end')
    return(image)


def findboxes(type):
    boxes = []
    answers = []
    for box in pyautogui.locateAllOnScreen(f'img/check{type}.png', confidence=0.8):
        left = int(box.left + 20)
        try:
            width = int(find('topr').x - left)
        except:
            width = int(find('nextquestionsm').x - left)
        answer = pytesseract.image_to_string(pyautogui.screenshot(region=(left, int(box.top), width, 40))).replace('\n','')
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
    #click('blank')
    pyautogui.click(400, 400)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
    pyautogui.press('esc')

    question = pyperclip.paste()#.split('Question')[2].split('Skip')[0]
    responses = question.split('Responses')#[1].split('\r\n\r\n')
    #show(responses, 'Raw Responses')
    responses = filter(responses, '\r\n')
    #show(responses, 'Filtered Raw Responses')
    responses = filter(responses, '  ')
    #question = f'Question:{question.split('Responses')[0]}Respond with only the correct answer{qtype()} from the following options:\n{responses}'
    
    #show(question.split('Respond')[0], 'Question')
    #show(responses, 'Responses')
    return(question, responses)


def askai(question):
    #if 'diagram' in question or 'image' in question:
        #print('---\nImage Question\n---')
        #image = parseimage()
        #model = vision()
        #response = model.generate_content([question, image], stream=True)
        #response.resolve()
        #response = response.text
    #else:
        model = text()
        response = model.generate_content([question], stream=True)
        response.resolve()
        response = response.text
    #if '["' in response:
        #response = response.replace('["','').replace('"]','').split('", "')
    #elif "['" in response:
        #response = response.replace("['","").replace("']","").split("', '")

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
    #if checkfor('checkchk') or checkfor('checkschk'):
        #show('Already Solved', 'Question')
        #return()
    #boxes, answers = findboxes(qtype())
    question, responses = copyquestion()
    response = askai(question)
    #correct = select(response, responses, answers, boxes)
    #show(correct, 'Correct Answer')
    return(response)#correct)


#---

solve()