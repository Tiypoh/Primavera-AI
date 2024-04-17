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

