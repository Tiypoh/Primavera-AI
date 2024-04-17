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
  'temperature': 0.75,
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

def error(text):
    print(f'***\nError Detected - {text}\n***')
    
def show(text, title):
    print(f'---\n{title} = {text}\n---')

def wait(type):
    input(f'---\n{type} Detected - Press Enter when you are ready to continue...')
    click('strongmind')
    click('empty')
    print('---')

def find(png, conf=0.85):
    return(pyautogui.locateCenterOnScreen(f'img/{png}.png', confidence=conf))

def findcorner(png, conf=0.85):
    return(pyautogui.locateOnScreen(f'img/{png}.png', confidence=conf))

def checkfor(button, conf=0.85):
    try:
        find(button, conf)
        return(True)
    except:
        return(False)

def click(png, conf=0.85):
    if checkfor(png):
        pyautogui.click(find(png, conf))
    else:
        error(f'Could not find {png} to click')

def parsescreen(left, top, width, height):
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)
    return(pytesseract.image_to_string(pyautogui.screenshot(region=(left, top, width, height))).replace('\n',''))

def checkans():
    x=True
    while x:
        if checkfor('botlfaded', 0.95):
            x = False
            return()
        if checkfor('yes'):
            x = False
            return()
        if checkfor('checkx') or checkfor('checksx'):
            try:
                click('botl')
            except:
                click('botl')
        else:
            solve()

def nextq():
    pyautogui.press('end')
    if checkfor('nextquestion'):
        click('nextquestion')
    elif checkfor('nextquestionsm'):
        click('nextquestionsm')
    elif checkfor('finish'):
        click('finish')
        print('Assignment Finished')
    else:
        error('Could not locate button')

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
        error('Could not find checkboxes')

def filter(x):
    for n in range(len(x)):
        for n4 in range(len(x), n, -1):
            for n3 in range(10):
                for n2 in range(n, n4):
                    x1 = x[n:n4][:n2]
                    x2 = x[n:n4][n2+n3:]
                    if x1 == x2 and len(x1) > 0:
                        return(x[n:n2])

def filterall(rawdata):
    data = []
    for x in rawdata:
        if len(x) > 0:
            x = x.replace('\r','\n').replace('\n',' ')
            x = x.strip()
            x = filter(x)
            if x not in data:
                data.append(x)
    
    #show(rawdata, 'Unfiltered Data')
    #show(data, 'Filtered Data')
    return(data)

def percentage():
    time.sleep(1)
    perc = findcorner('percentage')
    top = int(perc.top) - int(perc.height)
    try:
        percentage = parsescreen(perc.left, top, perc.width, perc.height)
        #show(percentage, 'OCR Percentage')
        percentage = int(percentage.split('.')[0])
    except Exception as e:
        error('Error on percentage')
        if checkfor('100'):
            percentage = 100
        else:
            percentage = int(input('---\nInput Percentage Manually\nPercentage = '))
            click('strongmind')
            click('empty')
            print('---')

    show(percentage, 'Percentage')
    return(percentage)

def finish():
    x = True
    while x:
        if checkfor('yes'):
            if not checkfor('unanswered'):
                click('yes')
                while x:
                    if checkfor('percentage'):
                        x = False
                        if percentage() >= 70:
                            return()
                        elif percentage() < 70:
                            click('retake')
                            time.sleep(0.5)
                            click('retake2')
                            time.sleep(1)
                    else:
                        time.sleep(0.1)
            else:
                click('no')
                checkans()
        else:
            time.sleep(1)

#-------------------------------------------------------------------------------------------


def findboxes(type):
    boxes = []
    answers = []
    for box in pyautogui.locateAllOnScreen(f'img/check{type}.png', confidence=0.8):
        left = box.left + 20
        try:
            width = find('topr').x - left
        except:
            width = find('nextquestionsm').x - left
        answer = parsescreen(left, box.top, width, 40)
        if answer not in answers:
            answers.append(answer)
            boxes.append(box)
    
    #show(boxes, 'Boxes')
    #show(answers, 'OCR Responses')
    return(boxes, answers)


def copyquestion():
    try:
        click('blank')
    except:
        time.sleep(1)
        click('blank')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
    pyautogui.press('esc')
    pyautogui.press('end')
    question = pyperclip.paste()
    questionnumber = question.split('Question')[0].splitlines()
    question = question.split('Question')[2].split('Skip')[0]
    responses = question.split('Responses')[1].split('\r\n\r\n')
    responses = filterall(responses)
    question = f'Question:{question.split('Responses')[0]}Respond with only the correct answer{qtype()} from the following options:\n{responses}'
    showquestion = question.split('Respond')[0].replace('\r','\n').replace('\n',' ')
    
    show(filter(questionnumber[2]), questionnumber[1])
    show(showquestion, 'Question')
    show(responses, 'Responses')
    return(question, responses)


def askai(question):
    boxes = findboxes(qtype())[0]
    pyautogui.moveTo(boxes[0])
    pyautogui.move(100, -200)
    pyautogui.click(button='right')
    time.sleep(0.1)
    if checkfor('copyimage'):
        click('copyimage')
        image = ImageGrab.grabclipboard()
        print('---\nImage Question\n---')
        model = loadai('gemini-pro-vision')
        response = model.generate_content([question, image])
        response = response.text
    else:
        pyautogui.click()
        model = loadai('gemini-pro')
        response = model.generate_content([question])
        response = response.text
    if '["' in response:
        return(response.replace('["','').replace('"]','').split('", "'))
    elif "['" in response:
        return(response.replace("['","").replace("']","").split("', '"))

    #show(response, 'AI Response')
    return(response)


def select(response, responses, answers, boxes):
    test = True
    correct = []
    cbox = []
    [correct.append(x) for x in responses if x in response]
    if correct == []:
        error('No correct anwers detected')
        responses = answers
        [correct.append(x) for x in responses if x in response]
    [cbox.append(boxes[responses.index(x)]) for x in responses if x in response]
    for x in cbox:
        #show(x, 'Click')
        y = x.top + 13
        x = x.left + 10
        pyautogui.click(x, y)

    return(correct)


def solve():
    boxes, answers = findboxes(qtype())
    question, responses = copyquestion()
    response = askai(question)
    correct = select(response, responses, answers, boxes)

    show(correct, 'Correct Answer')
    return(correct)


#-------------------------------------------------------------------------------------------

click('strongmind')
click('empty')

while checkfor('chrome'):
    try:
        if checkfor('yes'):
            finish()
        elif checkfor('locked'):
            if checkfor('previous'):
                click('previous')
        elif checkfor('discussion'):
            wait('Discussion')
        elif checkfor('project'):
            wait('Project')
        elif checkfor('quiz'):
            wait('Quiz')
        elif checkfor('topr') or checkfor('botl'):
            pyautogui.press('end')
            solve()
            if not checkfor('checkx') or not checkfor('checksx'):
                error('Correct answer not selected')
                solve()
            nextq()
        else:
            nextpg()
    except Exception as e:
        input([e, 'Fatal Error, press Enter to continue'])
        click('strongmind')
        click('empty')