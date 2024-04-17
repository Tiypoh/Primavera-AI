import pyautogui
import time
import pyperclip
import threading
import keyboard
import google.generativeai as genai
import PyHotKey
from PyHotKey import Key, keyboard_manager as manager
import PIL
from PIL import Image, ImageGrab

import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = (r'C:\Program Files\Tesseract-OCR\tesseract.exe')

genai.configure(api_key='AIzaSyABHI0UfHDsy1b9oxV590WrfhXvqYcDW5Y')
generation_config = {
  'temperature': 0.5,
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

run = True; exit = False; retries = 0

#---

def loadai(type):
    return(genai.GenerativeModel(model_name=f'{type}', generation_config=generation_config, safety_settings=safety_settings))

def error(text):
    print(f'***\nError Detected - {text}\n***')
    
def show(title, text):
    print(f'---\n{title} = {text}\n---')

def wait(type):
    input(f'---\n{type} Detected - Press Enter when you are ready to continue...')
    if cf('match', 0.95): nextq()
    click('strongmind')
    click('empty')
    print('---')

def find(png, conf=0.85):
    return(pyautogui.locateCenterOnScreen(f'img/{png}.png', confidence=conf))

def findall(png, conf=0.85):
    return(pyautogui.locateAllOnScreen(f'img/{png}.png', confidence=conf))

def findcorner(png, conf=0.85):
    return(pyautogui.locateOnScreen(f'img/{png}.png', confidence=conf))

def checkfor(button, conf=0.85):
    try:
        find(button, conf)
        return(True)
    except:
        return(False)

def cf(button, conf=0.85):
    return(checkfor(button, conf))

def click(png, conf=0.85):
    if cf(png):
        pyautogui.click(find(png, conf))
    else:
        error(f'Could not find {png} to click')
    # show('Click', find(png, conf))

def parsescreen(left, top, width, height):
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)
    return(pytesseract.image_to_string(pyautogui.screenshot(region=(left, top, width, height))).replace('\n',''))

def nextq():
    pyautogui.press('end')
    if cf('nextquestion'):
        click('nextquestion')
    elif cf('nextquestionsm'):
        click('nextquestionsm')
    elif cf('finish'):
        click('finish')
    else:
        error('Could not locate button')

def nextpg():
    global retries
    if not cf('strongmind'):
        return()
    if cf('yes'): retries = finish(70, retries)
    elif cf('locked') and cf('previous'): click('previous')
    elif cf('start'):
        if cf('SEL') or cf('SEL2'):
            try:
                click('next', 0.92)
            except:
                pyautogui.press('end')
        else:
            click('start')
    elif cf('next'):
        click('next', 0.92)
    else:
        pyautogui.press('end')

def qtype():
    if cf('check', 0.75):
        return('')
    elif cf('checks', 0.75):
        return('s')
    else:
        error('Could not find checkboxes')
        quit()

def filter(x):
    for n in range(len(x)):
        for n4 in range(len(x), n, -1):
            for n3 in range(10):
                for n2 in range(n, n4):
                    x1 = x[n:n4][:n2]
                    x2 = x.replace(' textsf comma ',',')[n:n4][n2+n3:]
                    if ' point ' not in x1:
                        x2 = x.replace(' textsf comma ',',').replace(' point ','.')[n:n4][n2+n3:]
                    if x1.replace(' ','') == x2.replace(' ','') and len(x1) > 0:
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
    for x in data:
        if x == '':
            data = findboxes()[1]
            break
    
    # show('Unfiltered Data', rawdata)
    # show('Filtered Data', data)
    return(data)

def percentage():
    time.sleep(1)
    perc = findcorner('percentage')
    top = int(perc.top) - int(perc.height)
    try:
        percentage = parsescreen(perc.left, top, perc.width, perc.height)
        # show('OCR Percentage', percentage)
        percentage = int(percentage.split('.')[0])
    except Exception as e:
        error('Error on percentage')
        if cf('100'):
            percentage = 100
        if cf('0'):
            percentage = 1
        else:
            percentage = int(input('---\nInput Percentage Manually\nPercentage = '))
            click('strongmind')
            click('empty')
            print('---')

    show('Percentage', percentage)
    return(percentage)

def finish(minpercent, retries):
    while run:
        if cf('yes'):
            if not cf('unanswered', 0.9):
                click('yes')
                while run:
                    if cf('percentage'):
                        if percentage() >= minpercent or retries >= 2:
                            retries = 0
                        elif percentage() < minpercent and retries < 2:
                            click('retake')
                            time.sleep(0.5)
                            click('retake2')
                            time.sleep(3)
                            retries += 1
                        # show('Retries', retries)
                        return(retries)
                    else:
                        time.sleep(0.1)
            else:
                click('no')
                checkans()
                return()
        else:
            time.sleep(1)

def checkans():
    while run:
        if cf('checkx') or cf('checksx'):
                click('botl')
        if '1 of' in copyquestion()[2]:
            solve()
            return()
        if cf('yes'):
            return()
        else:
            solve()

def checkimg(question, n):
    copywright = find(f'copywright{n}')
    pyautogui.moveTo(copywright)
    pyautogui.move(50, -50)
    pyautogui.click(button='right')
    time.sleep(0.1)
    if cf('copyimage'):
        click('copyimage')
        image = ImageGrab.grabclipboard()
        print('---\nImage Question\n---')
        question.append(image)
    else:
        pyautogui.click()
    
    return(question)

def clicklinks(question):
    links = []
    linktexts = []
    for link in findall('link', 0.75):
        linkrange = []
        for x in links:
            for n in range(-10, 10):
                linkrange.append(int(x.top+n))
        if link.top not in linkrange:
            links.append(link)
            pyautogui.click(link)
            while run:
                if cf('linkicon'):
                    pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c'); pyautogui.hotkey('ctrl', 'w')
                    linktext = pyperclip.paste().replace('\r','\n').replace('\n',' ')
                    linktexts.append(linktext)
                    break
    question = question + '\nRead these texts:\n' + str(linktexts)
    
    # show('Link Text', linktexts)
    return(question)

def findboxes():
    boxes = []
    ocrresponses = []
    for box in findall(f'check{qtype()}', 0.75):
        # show('Box', box)
        left = box.left + 20
        top = box.top - 22
        try:
            width = find('topr').x - left
        except:
            width = find('nextquestionsm').x - left
        ocrresponse = parsescreen(left, top, width, 60).replace(' ','').lower().replace('’','').replace('‘','').replace(',','').replace('.','').replace('y','v')
        # show('OCR Response', ocrresponse)
        boxrange = []
        for x in boxes:
            for n in range(-20, 20):
                boxrange.append(int(x.top+n))
        if box.top not in boxrange:
            boxes.append(box)
        if ocrresponse not in ocrresponses:
            ocrresponses.append(ocrresponse)

    # show('Boxes', boxes)
    # show('OCR Responses', ocrresponses)
    return(boxes, ocrresponses)


#-------------------------------------------------------------------------------------------


def copyquestion():
    try:
        click('blank')
    except:
        time.sleep(1)
        click('blank')
    responses = []
    pyautogui.hotkey('ctrl', 'a'); pyautogui.hotkey('ctrl', 'c')
    pyautogui.hotkey('ctrl', 'shiftleft', 'shiftright', 'home')
    pyautogui.press('esc'); pyautogui.press('end')
    question = pyperclip.paste()
    if "Part B" in question:
        read = question.split("Question")[1]
        questiona = question.split("Question")[2]
        questionb = question.split("Question")[3]
        show('Part A', questiona)
        show('Part B', questionb)
        responsesa = questiona.split('Responses')[1].split('\r\n\r\n')
        responsesa = filterall(responses)
        questiona = f"Question{questiona}\nRespond with only the correct answer from the following options:\n{responsesa}"
        responsesb = questionb.split('Responses')[1].split('\r\n\r\n')
        responsesb = filterall(responses)
        questionb = f"Question{questionb}\nRespond with only the correct answer from the following options:\n{responsesb}"
        question = [read, questiona, questionb]
        for x in responsesa:
            responses.append(x)
        for x in responsesb:
            responses.append(x)
    else:
        question = question.split("Read")[1].split("Skip")[0]
        responses = question.split('Responses')[1].split('\r\n\r\n')
        responses = filterall(responses)
        question = [f"Read{question}\nRespond with only the correct answer from the following options:\n{responses}"]
    for part in question:
        for x in part.split('Responses')[1].split('\r\n\r\n'):
            responses.append(x)
    responses = filterall(responses)
    showquestion = question.split('Respond')[0].replace('\r','\n').replace('\n',' ')
    question = [str(question)]
    
    show('Question', showquestion)
    show('Responses', responses)
    return(question)

#-------------------------------------------------------------------------------------------

def askai(question):
    question = [question]
    model = loadai('gemini-pro')
    response = model.generate_content(question)
    response = response.text
    return(response)


def solve():
    click('strongmind')
    question = copyquestion()
    correct = askai(question)

    show('Correct Answer', correct)
    return(correct)

def main():
    while run:
        time.sleep(1)

manager.register_hotkey([Key.alt_l, 's'], None, solve)

thread = threading.Thread(target=main())
thread.start()