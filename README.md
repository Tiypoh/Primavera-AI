# Primavera AI
 A program that utilizes google's Gemini AI API to answer multi-choice questions on Primavera or Strongmind online courses.

# Latest about.txt

AI-Based Primavera Automation Version 2.3
Created by Kyle Sebring
*©DESAD Tech Group 2024*


## Updates:

- ***Huge accuracy fix*** Lots of points were lost from misselecting boxes
	- v2.3 always selects the box it wants
- Only clicks next if question has been answered 
	- Used to (v2.1) solve again then press next regardless if none selected
- Minimum Percentage is customizable in main function
- Added cf as shorthand for checkfor
- Added graceful hotkey start/stop and exit
- Added logic to find the answer with the most matching words on no correct answer error
	- Removed OCR backup responses
- Fixed issue, discussion reply png
- Fixed issue, perecentage read error
	- Fixed issue, cant read 0
- Fixed issue, returns None on qtype() error
	- Added wait and quit, as well as lower tolerance
- Fixed issue, loses box positions between findboxes() and select()
	- Moved findboxes() inside of select()
- Fixed issue, stops for matching question when going to next page
	- Moved match check inside of test check and added else for normal questions
- Fixed issue, single letter responses arent caught by OCR
	- Seperated box and ocr append conditions
- Long Description is able to be copied
- Added .strip() to question number to select correct line in case of empty line
- Added notepadai.py 
- Increased OCR Region for answers
- Delete spaces and lower OCR responses for better checking
- Doesnt check for image question on every question, only if theres a copywright
- Improved checkans() finding when its reached first question
- Fixed finish() by adding returns
- Added error() for Fatal Error instead of regular print()
- Added wait() for match questions
	- Increased threshold for detection
- Made checkfor and wait into one line
- Removed while loop in nextpg() so it uses main loop
- Added another SEL identifier
- Only retries test twice
- Replaces responses with ocr responses if one of the responses is empty
- Added text replacement to numbers for the filter for questions with special formats
- Added 'select all that apply' to ai question for multiple choice


## Features:

- Starts/stops/exits with hotkey press gracefully
	- Start/Stop = alt + s
	- Exit = alt + q
- Uses Google Gemini to process questions
- Works on:
	- Workbooks
	- Checkpoints
	- Exams
- Waits for input on:
	- Discussion
	- Project
	- Quiz
- Processes image questions
- Clicks answers automatically
- Clicks next question automatically
- Clicks next page automatically
- Goes back when pages are locked
- Handles exceptions with notification and wait for input
- Organized Graphic Output
- Distinguishes between multi choice and single choice
- Only clicks next if question has been answered 
- Minimum Percentage is customizable in main function
- Catches unanswered questions when submitting, goes back through questions to find it
- Finds the most correct answer if none are correct


## Issues:

- Cannot do questions with matching boxes
- Uses top button or bottom button to identify test
- OCR for responses limited to narrow viewfield
- Blank section to select isnt optimal
- Misses images without copywright
- Loops when locked typically
- Cannot filter chemical equation responses
- If the wrong response is part of the correct response it will be selected
- Clicks next before reading percentage
	- Temporary fix, added if locked go back to finish()
- Percent happens twice sometimes?
- Definately cannot parse image responses
- Skips necessary SEL style questions
- New code needs cleaned


## Display:

- Options for display of:
	- Unfiltered Data
	- Filtered Data
	- Percentage OCR
	- Percentage*
	- Box Position Data
	- Responses from OCR
	- Question and Assignment Number
	- Question*
	- Responses*
	- AI Response
	- Sorted Responses
	- Correct Box Clicks
	- Correct Answer*
	- Assignment Finished*
	- Image Question*
	- Retry Count
- Defined errors for:
	- Could not find {png} to click
	- Could not locate button
	- Could not find checkboxes
	- Error on percentage
	- No correct anwers detected
	- Correct answer not selected
	- Fatal Error


## Written Process:

- Define a main loop to try to run the function if run condition is True
- Run condition starts as False
- Define hotkey alt+s to set run condition True/False
- Define hotkey alt+q to set exit condition True for main loop
- Open loop in a thread
- Clicks tab then empty space when starting
- Finishes assignment if available
	- Checks assignment percentage
- Goes back when pages are locked
- Waits for input on:
	- Discussion
	- Project
	- Quiz
	- Match Question
- Checks for assignment
	- Goes to end of page then solves
		- Checks if anything is already selected
		- Grabs box positions
			- Checks type of box to discern single vs multiple choice questions
			- Uses OCR to check for duplicate scanned boxes by reading text next to box
		- Copies question using select all, copy, and pyperclip paste
			- Unselects selection when done
			- Sorts out and filters duplicate text in responses
			- Inserts long description for image into question if available
			- Checks for image copywright 
				- Selects a position above copywright and sees if it can copy image and append
		- Sends question and respones to AI
		- Selects correct boxes
			- Creates lists of correct answers and boxes
				- Checks how many words from each response are in the correct answer
			- For each correct answer number it selects the box of the same number
	- Checks to make sure a checkbox is selected
		- Clicks next question if condition is met
- Clicks next page if nothing detected on screen
	- Presses end page if no next page button is detected
	- Stops next page process while loading