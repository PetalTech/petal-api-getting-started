PYTHON README 6/27/21 JG


===== How to run =====

1. Open the Petal GUI.

2. Turn on your Muse.

3. Start the stream.

4. Run the python script!


===== Important Note =====
DON'T edit your metrics call! It is set for all detections by default (necessary for apiClickerEMG.py and apiClickerBandpower.py):
	Line: metricsCall = ['bandpower', 'eye', 'blink', 'artifact_detect']


===== Scripts =====

1. apiHelper.py
	Only helper functions for the other scripts, ignore this one

2. apiClickerEMG.py
	Run: python apiClickerEMG.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
	Output: prints API output

3. apiClickerBandpower.py and wxDisplay.py
	Run: These scripts need to be run togheter in two separate windows:
		python apiClickerBandpower.py -k WmPFfy1pAtkX6t_KuSCxOV9xH4TEmp25RK9mWFANkZQ
		python wxDisplay.py
	Output: Displays bandpower graph:
		Click button to switch windows between average channel and average alpha power
		Displays alpha power (blue), interpolated alpha power (yellow), eye movements (green), blinks (yellow), and bad data (red)
		Saves PNG figure of output: click button to refresh the save function


===== Installation Requirements Python =====
1. pip install numpy
2. pip install lsl
3. pip install pyautogui
4. pip install matplotlib
5. pip install wx


===== Choose Your Own Click Adventure =====

Clicking code in apiClickerEMG.py:
    if 'True' in str(apiOutput['blink']):
        pyautogui.click(button='left') #mouse left click
    if 'True' in str(apiOutput['eye']):
        pyautogui.click(button='right') #mouse right click

# Try adding your own pyautogui code in here!
	# keyboard: https://pyautogui.readthedocs.io/en/latest/keyboard.html
	# mouse: https://pyautogui.readthedocs.io/en/latest/mouse.html
	# full documentation: https://pyautogui.readthedocs.io/en/latest/

# some examples:

##    if 'True' in str(apiOutput['blink']):
##        pyautogui.write('I saw you blink!') #write something
##        pyautogui.press('enter', presses=3) #press enter 3 times
##        pyautogui.press('browserhome') #when a browser is open, go to homepage

# you can also combine stuff!
# for example, in this one if you blink and you have the browser open, we'll send you to a google search of "petal technology"

##    if 'True' in str(apiOutput['blink']):
##        pyautogui.press('browsersearch')
##        pyautogui.write('Petal Technology')
##        pyautogui.press('enter')


