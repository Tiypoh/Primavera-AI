screen = pyautogui.screenshot(region=(225, 325, 700, 600))

data=pytesseract.image_to_data(screen, output_type='data.frame')



for x in ans:
    datals = zip(data[text], data[text][1:])
    ansls = zip(ans, ans[1:])
    x, y = data[datals == ansls]['left'].iloc[0], data[datals == ansls]['top'].iloc[0] # may need to change to data[text]


    for x in data:
        if str(x[text]) in str(ans[1]):
            options = options.append(x)
            print(options)


def vision():
    model = genai.GenerativeModel(model_name='gemini-1.0-pro-vision',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    convo = model.start_chat(history=[])
    return(model, convo)

try:
    side = find('topr')
except:
    try:
        side = find('nextquestion')
    except:
        side = find('nextquestionsm')
left = findcorner('listen').left
top = find('listen').y
width = int(findcorner('listen').left)
height = int(find('copywright').y - find('listen').y)


        response = model.generate_content([question, image], stream=True)


if "Part B" in question:
    read = question.split("Question")[0]
    questiona = question.split("Question")[1]
    questionb = question.split("Question")[2]
    questiona = f"{read}Question{questiona}\nRespond with only the correct answer"
    questionb = f"{read}Question{questionb}\nRespond with only the correct answer"
    var = 1
else:
    question = question.split("Read")[1].split("Skip")[0]
    question = f"Read{question}\nRespond with only the correct answer"
    
if var == 1:
    convo.send_message(questiona)
    print(convo.last.text)
    convo.send_message(questionb)
    print(convo.last.text)
    
---

    topr = pyautogui.locateOnScreen('topr.png', confidence=0.85)
    try:
        botl = pyautogui.locateOnScreen('botl.png', confidence= 0.85)
    except:
        botl = pyautogui.locateOnScreen('botllg.png', confidence= 0.85)
    width = int(topr.left - botl.left)
    height = int(botl.top - topr.top)
    top = int(topr.top)
    left = int(botl.left)
    screen = pyautogui.screenshot(region=(left, top, width, height))

---

def checkbox(box, boxes):
    left = int(box.left + box.width)
    width = int(topr.x - box.left - box.width)
    answer = pyautogui.screenshot(region=(left, int(box.top), width, int(box.height)))
    answer = pytesseract.image_to_string(answer).replace('\n','')
    if answer not in answers:
        answers.append(answer)
        return(box)

---

            y = x.split(filter)
            z = int(len(y)-1)
            x = y[z]
            if x == '' or x == ' ':
                z = int(len(y)-2)
                x = y[z]
            z = []
            for y in x:
                z.append(y)
                
                
img = ImageGrab.grabclipboard()
print(img)
---
            ##this is overly complicated and checks if they have extra characters before or after and up to 10 characters in between, and makes sure the answer is more than one character
def filter(x):
    for n in range(len(x)):
        for n4 in range(len(x), n, -1):
            for n3 in range(10):
                for n2 in range(n, n4):
                    x1 = x[n:n4][:n2]
                    x2 = x[n:n4][n2+n3:]
                    if x1 == x2 and len(x1) > 0:
                        return(x[n:n2])

            #this is much less complicated and checks unlimited spaces in between, spaces before and after have already been filtered
            for n in range(0, len(x)):
                for n2 in range(n, len(x)):
                    if x.replace(' ','')[:n] == x.replace(' ','')[n2:]:
                        x = x[:n]
                        break
---
