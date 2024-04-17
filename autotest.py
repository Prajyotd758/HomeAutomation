import pyttsx3
import speech_recognition as sr
import serial
import datetime
from bardapi import BardCookies
import keyboard

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import warnings

warnings.simplefilter("ignore")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty("rate", 200)

# ser = serial.Serial('COM3', '9600')

switches = {
    "hall_switch": False,
    "bedroom_switch": False,
    "kitchen_switch": False,
    "fan_switch": False,
}


# chatgpt

try:
    # Define the URL
    url = "https://dictation.io/speech"

    # Set up Chrome options
    chrome_driver_path = 'python\\chromedriver.exe'
    chrome_options = Options()
    # chrome_options.headless = True
    chrome_options.add_argument('--headless=new')
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    service = Service(chrome_driver_path)
    # Disable UI pop-ups for media access
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--use-fake-device-for-media-stream")

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # driver.maximize_window()
    driver.get(url)

    try:
        driver.find_element(
            by=By.XPATH, value="/html/body/div[1]/div").click()

    except:
        pass

    # Wait for the page to load
    sleep(15)

    # Execute JavaScript to enable microphone access
    driver.execute_script(
        'navigator.mediaDevices.getUserMedia({ audio: true })')
    sleep(1)

    # Click the "Clear" button to reset
    clear_button_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[2]/a[8]'
    driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
    sleep(1)

    # Click the start button
    start_button_xpath = "/html/body/div[3]/section/div/div/div[2]/div/div[3]/div[1]/a"
    driver.find_element(by=By.XPATH, value=start_button_xpath).click()
    print("Microphone is turned on")

except Exception as e:
    print("Error: Unable to configure the ChromeDriver properly.")
    print("To resolve this error, make sure to set up the ChromeDriver correctly.")
    print(e)

# CD = {
#     "__Secure-1PSID":
#         "dQiFtUIDXIG7dNDITvcpysyMv63QRLkBrcuLKiAbw_2nkgHF0UrYF5tv6PJslxpvEjF2kA.",
#     "__Secure-1PSIDTS":
#         "sidts-CjEBNiGH7uI26FqFT4ordgSimSVSvu5EkJgdzrdvKvVkUAlfVuxSlMeTPYQx66UPAH7FEAA",
#     "__Secure-1PSIDCC":
#         "ACA-OxOB-PeQnhDY8r925GGKEestonaHWOzt2Mnd3YCXN0PmfrUeJxcE7RCEVITh-chncjZArQ"
# }

# Bard = BardCookies(cookie_dict=CD)


def speak(audio):
    # rate = engine.getProperty("rate")
    engine.say(audio)
    engine.runAndWait()


def takecommands():
    cmd = sr.Recognizer()
    command = ""
    try:
        with sr.Microphone(device_index=1) as source:
            print("listening...")
            cmd.pause_threshold = 1
            audio = cmd.listen(source)

            print("recognizing...")

            command = cmd.recognize_google(audio, language="en-in")
            print(command)

    except Exception as e:
        print(e)

    return command


def greet():
    x = datetime.datetime.now()
    h = x.time().hour

    if h < 5 or h > 22:
        speak("good night sir")
    elif h < 12 and h > 5:
        speak("good morning sir")
    elif h < 17 and h > 12:
        speak("good afternoon sir")
    elif h < 22 and h > 17:
        speak("good evening sir")


def mybard():
    speak("hello i'm jarvis how can i help you")
    # bardquery = takecommands().lower()
    # reply = Bard.get_answer(f"{bardquery} in 100 words")['content']
    # if keyboard.is_pressed("esc"):
    #     engine.stop()
    # speak(reply)


if __name__ == "__main__":
    greet()

    while True:
        # cmds = takecommands().lower()

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

        if cmds == "":
            continue

        if "hey jarvis" in cmds:
            engine.setProperty('voice', voices[0].id)
            # mybard()
            # turn on all light

        elif "call jarvis" in cmds:
            engine.setProperty('voice', voices[0].id)
            speak(
                "hello there, i'm here to assist you , if you want to talk to siri again just say call siri")
            pass

        elif "call siri" in cmds:
            engine.setProperty('voice', voices[1].id)
            speak(
                "hello there, i'm here to assist you , if you want to talk to jarvis again just say call jarvis")
            pass
            # ser.write(b'A')

        elif "turn on all" in cmds or "light chalu kar" in cmds:
            speak("turning on all lights")
            # ser.write(b'A')

            # turn off all the light
        elif "turn off light" in cmds or "light band kar" in cmds:
            speak("turning off all light")
            # ser.write(b'B')

            # turn on FAn
        elif "turn on fan" in cmds:
            if switches["fan_switch"] == True:
                speak("the fan is already on")
            else:
                speak("turning on fan")
                # ser.write(b'I')
                switches["fan_switch"] = True

        # turn OFF FAN
        elif "turn off fan" in cmds:
            if switches["fan_switch"] == False:
                speak("the fan is already off")
            else:
                speak("turning off fan")
                # ser.write(b'J')
                switches["fan_switch"] = False

            # turn on 2 light - bedroom and hall
        elif "turn on bedroom and halls light" in cmds or "turn on hall and bedrooms light" in cmds:
            speak("turning on halls and bedrooms light")
            # ser.write(b'K')

            # turn OFF 2 light - bedroom and hall
        elif "turn off bedroom and halls light" in cmds or "turn off hall and bedrooms light" in cmds:
            speak("turning off halls and bedrooms light")
            # ser.write(b'L')

            # turn on 2 light - bedroom and kitchen
        elif "turn on bedroom and kichens light" in cmds or "turn on kitchen and bedrooms light" in cmds:
            speak("turning on bedrooms and kitchens light")
            # ser.write(b'M')

            # turn OFF 2 light - bedroom and kitchen
        elif "turn off bedroom and kichens light" in cmds or "turn off kitchen and bedrooms light" in cmds:
            speak("turning off bedroom and kitchens light")
            # ser.write(b'N')

            # turn on 2 light - hall and kitchen
        elif "turn on hall and kitchen light" in cmds or "turn on kitchen and halls light" in cmds:
            speak("turning on halls and kitchens light")
            # ser.write(b'O')

            # turn OFF 2 light - hall and kitchen
        elif "turn off hall and kitchen light" in cmds or "turn off kitchen and halls light" in cmds:
            speak("turning off halls and kitchens light")
            # ser.write(b'P')

            # turn ON light of hall
        elif "turn on hall light" in cmds:
            speak("turning on halls light")
            # ser.write(b'C')
            speak("should i turn on fan as well")
            cmd = ""
            # text_element_xpath = '/html/body/div[3]/section/div/div/div[2]/div/div[2]'
            text = driver.find_element(by=By.XPATH, value=text_element_xpath).text

            # if len(text) == 0:
            #     pass
            # else:
                # Click the "Clear" button to reset
            driver.find_element(by=By.XPATH, value=clear_button_xpath).click()
            text = text.strip()

            output_file_path = "SpeechRecognition.txt"
                # output_file_path = "python\\SpeechRecognition.txt"
            with open(output_file_path, "w") as file_write:
                file_write.write(text)

                # print("recognizing")
            with open(output_file_path, "r") as file_write:
                cmd = file_write.read().lower()
                print(cmd)
            
            if "yes" in cmd:
                speak("turning on fan")
                # ser.write(b'I')
            elif "no" in cmd:
                speak("ok")

            # turn OFF light of hall
        elif "turn off hall light" in cmds:
            speak("turning off halls light")
            # ser.write(b'D')

            # turn on light of bedroom
        elif "turn on bedroom light" in cmds:
            speak("turning on bedrooms light")
            # ser.write(b'E')

            # turn OFF light of bedroom
        elif "turn off bedroom light" in cmds:
            speak("turning off bedrooms light")
            # ser.write(b'F')

            # turn on light of bedroom
        elif "turn on kitchen light" in cmds:
            speak("turning on kitchens light")
            # ser.write(b'G')

            # turn OFF light of bedroom
        elif "turn off kitchen light" in cmds:
            speak("turning off kitchens light")
            # ser.write(b'H')

            # turn off everything
        elif "offline" in cmds:
            speak("going off! have a nice day! see you soon..")
            # ser.write(b'B')
            # ser.write(b'J')
            quit()
