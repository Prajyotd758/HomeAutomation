import pyttsx3
import speech_recognition as sr
import serial
import datetime
from bardapi import BardCookies
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import warnings

from playsound import playsound

warnings.simplefilter("ignore")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 150)


ser = serial.Serial('COM3', '9600')

switches = {
    "hall_switch": False,
    "bedroom_switch": False,
    "kitchen_switch": False,
    "fan_switch": False,
}

import pyperclip
import pyautogui
import webbrowser
from time import sleep
import json
import keyboard

# def CookieScrapper():
#     webbrowser.open("https://bard.google.com")-
#     sleep(3)
#     pyautogui.click(x=1559, y=68)
#     sleep(1)
#     pyautogui.click(x=1366, y=158)
#     sleep(1)
#     pyautogui.click(x=1257, y=101)
#     sleep(1)
#     keyboard.press_and_release('ctrl + w')

#     data = pyperclip.paste()

#     try:
#         json_data = json.loads(data)
#         pass

#     except json.JSONDecodeError as e:
#         print(f"Error parsing JSON data: {e}")

#     SID = "__Secure-1PSID"
#     TS = "__Secure-1PSIDTS"
#     CC = "__Secure-1PSIDCC"

#     SIDValue = next((item for item in json_data if item["name"] == SID), None)
#     TSValue = next((item for item in json_data if item["name"] == TS), None)
#     CCValue = next((item for item in json_data if item["name"] == CC), None)

#     if SIDValue is not None:
#         SIDValue = SIDValue["value"]
#     else:
#         print(f"{SIDValue} not found in the JSON data.")

#     if TSValue is not None:
#         TSValue = TSValue["value"]
#     else:
#         print(f"{TSValue} not found in the JSON data.")

#     if CCValue is not None:
#         CCValue = CCValue["value"]
#     else:
#         print(f"{CCValue} not found in the JSON data.")

#     cookie_dict = {
#         "__Secure-1PSID": SIDValue ,
#         "__Secure-1PSIDTS": TSValue,
#         "__Secure-1PSIDCC": CCValue,
#     }

#     return cookie_dict

# cookie_dict = CookieScrapper()

# Bard = BardCookies(cookie_dict=cookie_dict)


try:
    # Define the URL
    url = "https://dictation.io/speech"
    # Set up Chrome options
    chrome_driver_path = 'chromedriver.exe'
    chrome_options = Options()
    # chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    service = Service(chrome_driver_path)
    # Disable UI pop-ups for media access
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()
    driver.get(url)

    parrent_window = driver.current_window_handle

    try:
        driver.find_element(
            by=By.XPATH, value="/html/body/div[1]/div").click()

    except:
        pass

    # Wait for the page to load
    sleep(12)

    # Execute JavaScript to enable microphone access
    driver.execute_script(
        'navigator.mediaDevices.getUserMedia({ audio: true })')
    sleep(1)

    # Click the "Clear" button to reset
    clear_button_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[2]/a[8]'
    driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
    # creating a new tab for youtube

except Exception as e:
    print("Error: Unable to configure the ChromeDriver properly.")
    print("To resolve this error, make sure to set up the ChromeDriver correctly.")
    print(e)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takecommands():
    cmd = sr.Recognizer()
    command = ""
    try:
        with sr.Microphone(device_index=1) as source:
            # cmd.pause_threshold = 1
            print("listening...")
            cmd.adjust_for_ambient_noise(source , duration= 1)
            audio = cmd.listen(source)

            print("recognizing...")
            try:
                command = cmd.recognize_google(audio, language="en-in")
            except:
                command = ""
                
            print(command)

    except Exception as e:
        print(e)

    return command


def split_and_save_paragraphs(data, filename):
    paragraphs = data.split('\n\n')
    with open(filename, 'w') as file:
        file.write(data)
    data = paragraphs[:2]
    separator = ', '
    joined_string = separator.join(data)
    return joined_string


def greet():
    x = datetime.datetime.now()
    h = x.time().hour

    if h <= 5 or h > 22:
        speak("hello sir")
    elif h <= 12 and h > 5:
        speak("good morning sir")
    elif h <= 17 and h > 12:
        speak("good afternoon sir")
    elif h <= 22 and h > 17:
        speak("good evening sir")


# def mybard():
#     speak("hello i'm jarvis how can i help you")
#     cmd = ""
#     stop = True
#     while stop:
#         cmd = takecommands().lower()
#         print("started")
#         if "shutdown" in cmd:
#             stop = False
#             break
#         elif cmd == "":
#             continue
#         else:
#             RealQuestion = str(cmd)
#             results = Bard.get_answer(
#                 f'{RealQuestion} , without images and any links')['content']
#             current_datetime = datetime.datetime.now()
#             formatted_time = current_datetime.strftime("%H%M%S")
#             filenamedate = str(formatted_time) + str(".txt")
#             filenamedate = "DataBase\\" + filenamedate
#             print(split_and_save_paragraphs(results, filename=filenamedate))
#             reply = split_and_save_paragraphs(results, filename=filenamedate)
#             speak(reply)

def speechonoff():
    stop_button_xpath = "/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[1]/a"
    driver.find_element(by=By.XPATH, value=stop_button_xpath).click()

def realtimecmd():
    cmds = ""
    text_element_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[2]'
    text = driver.find_element(by=By.XPATH, value=text_element_xpath).text

    if len(text) == 0:
        pass
    else:
        # Click the "Clear" button to reset
        driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
        text = text.strip()

        output_file_path = "SpeechRecognition.txt"
        # output_file_path = "python\\SpeechRecognition.txt"
        with open(output_file_path, "w") as file_write:
            file_write.write(text)

        # print("recognizing")
        with open(output_file_path, "r") as file_write:
            cmds = file_write.read().lower()
            print(cmds)  

    return str(cmds)


def playmusic(songname):
    serchbox = driver.find_element(
        by=By.XPATH, value='/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[1]/input')
    serchbox.send_keys(f'{songname}')

    sleep(1)

    searchbtn = driver.find_element(
        by=By.XPATH, value='/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/button/yt-icon/yt-icon-shape/icon-shape/div').click()

    sleep(4)

    video = driver.find_element(
        by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-image/img').click()

    sleep(3)

    closebtn = driver.find_element(
        by=By.XPATH, value='/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[2]/ytd-button-renderer/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click()

    sleep(7)
    try:
        adbtn = driver.find_element(
            by=By.XPATH, value='/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[23]/div/div[3]/div/div[2]/span/button').click()
    except Exception as e:
        print(e)

def cleartext():
    driver.find_element(by=By.XPATH, value=clear_button_xpath).click()

def play():
    speak("please give me a song name")
    sleep(2)
    while True:
        songname = takecommands().lower()
        # songname = realtimecmd()

        if songname == "":
            continue
        elif "exit" in songname:
            break
        elif "pause" in songname or "resume" in songname:
            driver.find_element(
                by=By.XPATH, value="/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[1]/video").click()
        elif "play" in songname:
            playmusic(songname)
                 

def remove(string):
    newstr = "".join(string.split())
    newstr = newstr.replace("attherate", "@")
    newstr = newstr.replace("dot", ".")
    return newstr


def sendmail():
    sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    # email address
    speechonoff()
    speak("please provide email address")
    speechonoff()
    sleep(10)
    email = realtimecmd().lower()
    email = remove(email)
    print(email)
    driver.switch_to.window(driver.window_handles[1])
    # email = takecommands().lower()
    driver.find_element(
        by=By.XPATH, value="/html/body/form/input[2]").send_keys(f"{email}")
    
    # subject
    driver.switch_to.window(driver.window_handles[0])
    speechonoff()
    speak("subject of the email")
    speechonoff()
    sleep(10)
    subject = realtimecmd().lower()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(
        by=By.XPATH, value="/html/body/form/input[1]").send_keys(f"{subject}")
    
    
    # body of email
    driver.switch_to.window(driver.window_handles[0])
    speechonoff()
    speak("body of the email")
    speechonoff()
    sleep(10)
    body = realtimecmd().lower()
    # body = takecommands().lower()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element(
        by=By.XPATH, value="/html/body/form/textarea").send_keys(f"{body}")
    
    # send button
    driver.find_element(by=By.XPATH, value="/html/body/form/input[3]").click()
    sleep(1)
    speak("the email has been sent")
    sleep(5)
    driver.switch_to.window(driver.window_handles[0])


if __name__ == "__main__":
    greet()
    sleep(2)
    start_button_xpath = "/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[1]/a"
    driver.find_element(by=By.XPATH, value=start_button_xpath).click()

    print("Microphone is turned on")
    while True:
        cmds = realtimecmd()

        if cmds == "":
            continue

        elif "play music" in cmds or "gane law" in cmds:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("https://youtube.com")
            play()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            cleartext()

        elif ("write" in cmds and "email" in cmds):
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get("http://localhost:3000")
            sendmail()
            cleartext()
            # driver.quit()

        elif ("pagal" in cmds and "jarvis" in cmds) or ("yeda" in cmds and "jarvis" in cmds):
            playsound('jethalal.mp3')
            sleep(3)

        # elif "hey jarvis" in cmds:
        #     engine.setProperty('voice', voices[0].id)
        #     mybard()
        #     cleartext()
        # turn on all light

        elif "call jarvis" in cmds:
            engine.setProperty('voice', voices[0].id)
            speak(
                "hello there, i'm here to assist you")
            continue

        elif "call siri" in cmds:
            engine.setProperty('voice', voices[1].id)
            speak(
                "hello there, i'm here to assist you")
            continue

        # turn on all light
        elif "turn on all" in cmds or "light chalu kar" in cmds:
            speak("turning on all lights")
            ser.write(b'A')
            switches["bedroom_switch"], switches["hall_switch"], switches["kitchen_switch"] = True, True, True

        # turn off all the light
        elif "turn off all" in cmds or "light band kar" in cmds:
            speak("turning off all light")
            ser.write(b'B')
            switches["bedroom_switch"], switches["hall_switch"], switches["kitchen_switch"] = False, False, False

        # turn on FAn
        elif "turn on fan" in cmds or "fan chalu kar" in cmds:
            if switches["fan_switch"] == True:
                speak("the fan is already on")
            else:
                speak("turning on fan")
                ser.write(b'I')
                switches["fan_switch"] = True

        # turn OFF FAN
        elif "turn off fan" in cmds or "fan band kar" in cmds:
            if switches["fan_switch"] == False:
                speak("the fan is already off")
            else:
                speak("turning off fan")
                ser.write(b'J')
                switches["fan_switch"] = False

        elif "turn on bedroom and halls light" in cmds or "turn on hall and bedrooms light" in cmds:
            if switches["bedroom_switch"] and switches["hall_switch"]:
                speak("the lights are already on")
            else:
                speak("turning on halls and bedrooms light")
                ser.write(b'K')
                switches["bedroom_switch"], switches["hall_switch"] = True, True

        # turn OFF 2 light - bedroom and hall
        elif "turn off bedroom and halls light" in cmds or "turn off hall and bedrooms light" in cmds:
            if switches["bedroom_switch"] == False and switches["hall_switch"] == False:
                speak("the lights are already off")
            else:
                speak("turning off halls and bedrooms light")
                ser.write(b'L')
                switches["bedroom_switch"], switches["hall_switch"] = False, False

        # turn on 2 light - bedroom and kitchen
        elif "turn on bedroom and kitchens light" in cmds or "turn on kitchen and bedrooms light" in cmds:
            if switches["bedroom_switch"] and switches["hall_switch"]:
                speak("the lights are already on")
            else:
                speak("turning on bedrooms and kitchens light")
                ser.write(b'M')
                switches["bedroom_switch"], switches["kitchen_switch"] = True, True

        # turn OFF 2 light - bedroom and kitchen
        elif "turn off bedroom and kitchens light" in cmds or "turn off kitchen and bedrooms light" in cmds:
            if switches["bedroom_switch"] == False and switches["kitchen_switch"] == False:
                speak("the lights are already off")
            else:
                speak("turning off bedroom and kitchens light")
                ser.write(b'N')
                switches["bedroom_switch"], switches["kitchen_switch"] = False, False

        # turn on 2 light - hall and kitchen
        elif "turn on hall and kitchen light" in cmds or "turn on kitchen and halls light" in cmds:
            if switches["kitchen_switch"] and switches["hall_switch"]:
                speak("the lights are already on")
            else:
                speak("turning on halls and kitchens light")
                ser.write(b'O')
                switches["hall_switch"], switches["kitchen_switch"] = True, True

        # turn OFF 2 light - hall and kitchen
        elif "turn off hall and kitchen light" in cmds or "turn off kitchen and halls light" in cmds:
            if switches["hall_switch"] == False and switches["kitchen_switch"] == False:
                speak("the lights are already off")
            else:
                speak("turning off halls and kitchens light")
                ser.write(b'P')
                switches["hall_switch"], switches["kitchen_switch"] = False, False

        # turn ON light of hall
        elif "turn on hall light" in cmds:
            if switches["hall_switch"] == True:
                speak("the hall light is already on")
            else:
                speak("turning on halls light")
                ser.write(b'C')
                switches["hall_switch"] = True

        # turn OFF light of hall
        elif "turn off hall light" in cmds:
            if switches["hall_switch"] == False:
                speak("the hall light is already off")
            else:
                speak("turning off halls light")
                ser.write(b'D')
                switches["hall_switch"] = False

        # turn on light of bedroom
        elif "turn on bedroom light" in cmds:
            if switches["bedroom_switch"] == True:
                speak("the bedroom light is already on")
            else:
                speak("turning on bedrooms light")
                ser.write(b'E')
                switches["bedroom_switch"] = True

        # turn OFF light of bedroom
        elif "turn off bedroom light" in cmds:
            if switches["bedroom_switch"] == False:
                speak("the bedroom light is already off")
            else:
                speak("turning off bedrooms light")
                ser.write(b'F')
                switches["bedroom_switch"] = False

        # turn on light of bedroom
        elif "turn on kitchen light" in cmds:
            if switches["kitchen_switch"] == True:
                speak("the kitchen light is already on")
            else:
                speak("turning on kitchens light")
                ser.write(b'G')
                switches["kitchen_switch"] = True

        # turn OFF light of bedroom
        elif "turn off kitchen light" in cmds:
            if switches["kitchen_switch"] == False:
                speak("the kitchen light is already off")
            else:
                speak("turning off kitchens light")
                ser.write(b'H')
                switches["kitchen_switch"] = False

        # turn off everything
        elif "offline" in cmds:
            speak("going off! have a nice day! see you soon..")
            ser.write(b'B')
            ser.write(b'J')
            quit()

        else:
            # speak("sorry i didn't understand , please repeat")
            continue
