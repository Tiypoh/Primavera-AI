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
