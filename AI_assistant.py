from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys,json,random,webbrowser,time,datetime,face_recognition,os,cv2,math,serial,requests
from bs4 import BeautifulSoup as soup
from AppOpener import run

port = serial.Serial('COM6',9600)
with open("intents.json") as f:
    global data
    data = json.load(f)

access = False

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome',None,webbrowser.BackgroundBrowser(chrome_path))
recognizer = speech_recognition.Recognizer()
speaker = tts.init()
speaker.setProperty('rate',162)


def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            global master_name,access,name
            access = False
            master_name = ""
            ret, frame = video_capture.read()

            if self.process_current_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1]

                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                master_name = self.face_names[0].split()[0]

            cv2.imshow('Granting access', frame)

            if master_name == "Sang.jpg":   
                speaker.say("Access accepted")
                speaker.runAndWait()
                access = True
                break
            elif master_name == "Unknown":
                speaker.say("Access denied")
                speaker.runAndWait()                
            elif cv2.waitKey(1) == ord('q'):
                speaker.say("Access denied")
                speaker.runAndWait()
                break

        video_capture.release()
        cv2.destroyAllWindows()
        cv2.waitKey(2)

def hello():
    global data
    hello_data =[i["responses"] for i in data["intents"] if i["tag"] == "greeting"]
    random_choice = random.randint(0,len(hello_data[0])-1)
    speaker.say(hello_data[0][random_choice])
    speaker.runAndWait()

def quit():
    global data,access,exit
    quit_data = [i["responses"] for i in data["intents"] if i["tag"] == "exit"]
    random_choice = random.randint(0,len(quit_data[0])-1)
    speaker.say(quit_data[0][random_choice])
    speaker.runAndWait()
    exit = True

def web_browsing():
    global message
    user = message.split()
    if ".com" in user[-1]:
        try:
            user = user[-1].split(".com")
            speaker.say("openning  {}".format(user[0]))
            webbrowser.open_new(user[0]+".com")
            speaker.runAndWait()
        except:
            pass
    else:
        speaker.say("openning {}".format(user[-1]))
        webbrowser.open_new(user[-1]+".com")
        speaker.runAndWait()

def my_canvas():
    speaker.say("Opennig canvas")
    webbrowser.open_new("rmit.instructure.com") 
    speaker.runAndWait()  

def get_time():
    curr_time = time.strftime("%H:%M", time.localtime())
    curr_time = "It is {}".format(curr_time)
    speaker.say(curr_time)
    speaker.runAndWait()

def get_date():
    curr_time = datetime.datetime.now()
    year = curr_time.year
    day = curr_time.day
    month = curr_time.month
    curr_time = "{}-{}-{}".format(year,day,month)
    speaker.say(curr_time)
    speaker.runAndWait()

def well():
    global data
    well_data = [i["responses"] for i in data["intents"] if i["tag"] == "well"]
    random_choice = random.randint(0,len(well_data[0])-1)
    speaker.say(well_data[0][random_choice])
    speaker.runAndWait()

def thank_you():
    global data
    well_data = [i["responses"] for i in data["intents"] if i["tag"] == "thank you"]
    random_choice = random.randint(0,len(well_data)-1)
    speaker.say(well_data[0][random_choice])
    speaker.runAndWait()

def bedroom_light_on():
    speaker.say("Lights on")
    port.write("1".encode(encoding='UTF-8'))
    speaker.runAndWait()

def reading_news():
    global message
    try:
        url = 'https://www.bbc.com/news'
        response = requests.get(url)
        unwantedtitle = ['BBC World News TV', 'BBC World Service Radio', 'News daily newsletter', 'Mobile app', 'Get in touch']
        soups = soup(response.text, 'html.parser')
        headlines = soups.find('body').find_all('h3')
        headlines = [x.text.strip() for x in headlines if x.text.strip() not in unwantedtitle]
        for i in headlines[:12]:
            speaker.say(i)
            speaker.runAndWait()
    except:
        speaker.say("Sir, there is an error while I'm trying to connect to the BBC news")
        speaker.runAndWait()

def your_self():
    global data
    self_data = [i["responses"] for i in data["intents"] if i["tag"] == "yourself"]
    random_choice = random.randint(0,len(self_data[0])-1)
    speaker.say(self_data[0][random_choice])
    speaker.runAndWait()

def bedroom_light_off():
    speaker.say("lights off")
    port.write("0".encode(encoding='UTF-8'))
    speaker.runAndWait()

def application():
    global message
    app = message.split()
    app = app[app.index("application")+1]
    speaker.say(f"running {app}")
    speaker.runAndWait()
    run(app)

def toilet_light_on():
    speaker.say("toilet lights on")
    port.write("2".encode(encoding='UTF-8'))
    speaker.runAndWait()

def toilet_light_off():
    speaker.say("toilet lights off")
    port.write("3".encode(encoding='UTF-8'))
    speaker.runAndWait()

def open_window():
    speaker.say("Windows opened")
    port.write("4".encode(encoding='UTF-8'))
    speaker.runAndWait()

def close_window():
    speaker.say("Windows closed")
    port.write("5".encode(encoding='UTF-8'))
    speaker.runAndWait()


def main():
    global access,recognizer,message,exit,assistant,start
    mappings = {
    "greeting":hello,
    "exit":quit,
    "web browsing":web_browsing,
    "assignments":my_canvas,
    "time":get_time,
    "date":get_date,
    "well":well,
    "thank you":thank_you,
    "bedroom_light_on":bedroom_light_on,
    "new":reading_news,
    "yourself":your_self,
    "bedroom_light_off":bedroom_light_off,
    "application":application,
    "toilet_light_on":toilet_light_on,
    "toilet_light_off":toilet_light_off,
    "open_window":open_window,
    "close_window":close_window
    }
    if access == False:
        fr = FaceRecognition()
        fr.run_recognition()
        speaker.say("Initializing.....")
        speaker.runAndWait()
        assistant = GenericAssistant('intents.json',intent_methods=mappings)
        assistant.train_model()
        speaker.say("finished Initializing")
        speaker.say("welcome master")
        speaker.runAndWait()
        while access == True and exit == False:
            try:
                with speech_recognition.Microphone() as mic:
                        recognizer.adjust_for_ambient_noise(mic,duration=0.7)
                        audio = recognizer.listen(mic,timeout=30)
                        message = recognizer.recognize_google(audio).lower()
                        print(message)
                        assistant.request(message)
            except speech_recognition.UnknownValueError:
                recognizer = speech_recognition.Recognizer()
            except speech_recognition.WaitTimeoutError:
                print("wait too long")
                break
    else:
        speaker.say("Welcome master")
        speaker.runAndWait()
        while access == True and exit == False:
            try:
                with speech_recognition.Microphone() as mic:
                    recognizer.adjust_for_ambient_noise(mic,duration=0.7)
                    audio = recognizer.listen(mic,timeout=30)

                    message = recognizer.recognize_google(audio).lower()

                    print(message)
                    assistant.request(message)
            except speech_recognition.UnknownValueError:
                    recognizer = speech_recognition.Recognizer()
            except speech_recognition.WaitTimeoutError:
                    print("wait too long")
                    break


if __name__ == "__main__":
    while True:
        exit = False
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic,duration=0.7)
                audio = recognizer.listen(mic)

                awake_message = recognizer.recognize_google(audio).lower()
                if "wake up" in awake_message:
                    print(awake_message)
                    main()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()



