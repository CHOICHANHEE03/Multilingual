import numpy as np
import tensorflow as tf
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import winsound
from gtts import gTTS
import playsound
import os
import cv2

# CNN 모델 로드
cnn = tf.keras.models.load_model("my_cnn_for_deploy.h5") #저장된 모델 파일(dataset.py)에서 Keras 모델을 로드

# 클래스 이름 (한국어, 영어, 프랑스어, 독일어)
class_names_kr = ['비행기', '자동차', '새', '고양이', '사슴', '강아지', '개구리', '말', '배', '트럭']
class_names_en = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
class_names_fr = ['avion', 'voiture', 'oiseau', 'chatte', 'biche', 'chienne', 'grenouille', 'jument', 'navire', 'un camion']
class_names_de = ['flugzeug', 'automobil', 'Vogel', 'katze', 'Hirsch', 'Hund', 'Frosch', 'Pferd', 'Schiff', 'LKW']

class_id = 0
tk_img = ''


# 비디오를 처리하고 결과를 예측하는 함수
def process_video():
    global class_id, tk_img
    
    video = cv2.VideoCapture(0)
    while video.isOpened():
        success, frame = video.read()
        if success:
            cv2.imshow('Camera', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC 키로 종료
                break
    video.release()
    cv2.destroyAllWindows()
    
    # 이미지 처리
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame)
    
    # Tkinter에 표시할 이미지 준비
    tk_img = img.resize([256, 256])
    tk_img = ImageTk.PhotoImage(tk_img)
    canvas.create_image(
        (canvas.winfo_width() / 2, canvas.winfo_height() / 2),
        image=tk_img, anchor='center'
    )
    
    # CNN 모델로 예측
    x_test = []
    x = np.asarray(img.resize([32, 32])) / 255.0
    x_test.append(x)
    x_test = np.asarray(x_test)
    res = cnn.predict(x_test)
    class_id = np.argmax(res)
    
    # 번역 결과 업데이트
    label_kr['text'] = '한국어: ' + class_names_kr[class_id]
    label_en['text'] = '영어: ' + class_names_en[class_id]
    label_fr['text'] = '프랑스어: ' + class_names_fr[class_id]
    label_de['text'] = '독일어: ' + class_names_de[class_id]
    winsound.Beep(frequency=500, duration=250)


# 한국어 음성 출력
def tts_korean():
    tts = gTTS(text=class_names_kr[class_id], lang='ko')
    if os.path.isfile('word.mp3'):
        os.remove('word.mp3')
    tts.save('word.mp3')
    playsound.playsound('word.mp3', True)


# 영어 음성 출력
def tts_english():
    tts = gTTS(text=class_names_en[class_id], lang='en')
    if os.path.isfile('word.mp3'):
        os.remove('word.mp3')
    tts.save('word.mp3')
    playsound.playsound('word.mp3', True)


# 프랑스어 음성 출력
def tts_french():
    tts = gTTS(text=class_names_fr[class_id], lang='fr')
    if os.path.isfile('word.mp3'):
        os.remove('word.mp3')
    tts.save('word.mp3')
    playsound.playsound('word.mp3', True)


# 독일어 음성 출력
def tts_deutsch():
    tts = gTTS(text=class_names_de[class_id], lang='de')
    if os.path.isfile('word.mp3'):
        os.remove('word.mp3')
    tts.save('word.mp3')
    playsound.playsound('word.mp3', True)


# 단어 저장 (중복 방지)
def save_words():
    # 단어 리스트 (한국어, 영어, 프랑스어, 독일어)
    words_to_save = [
        '한국어: ' + class_names_kr[class_id],
        '영어: ' + class_names_en[class_id],
        '프랑스어: ' + class_names_fr[class_id],
        '독일어: ' + class_names_de[class_id]
    ]
    
    # 파일에서 이미 저장된 단어를 읽어들여 중복 체크
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as file:
            existing_words = file.readlines()
    
        # 단어가 이미 파일에 존재하는지 확인
        for word in words_to_save:
            if any(word.strip() in line.strip() for line in existing_words):
                # 중복된 단어가 있으면 알림 창 표시
                messagebox.showinfo("알림", "해당 단어는 이미 저장되어 있습니다.")
                return  # 이미 저장된 단어가 있으면 중지
    
    # 단어를 'words.txt' 파일에 가로로 저장 (구분자는 공백)
    with open("words.txt", "a", encoding="utf-8") as file:
        file.write("   ".join(words_to_save) + "\n")

        # 단어 저장 완료 후 알림 창 표시
    messagebox.showinfo("저장 완료", "단어가 저장되었습니다.")
    print("단어가 저장되었습니다.")


# 프로그램 종료
def quit_program():
    win.destroy()


# Tkinter 윈도우 설정
win = tk.Tk()
win.title('다국어 단어 공부')
win.geometry('400x400')

# 배경색 설정
win.config(bg='lightblue')

# 버튼, 캔버스, 레이블 생성
process_button = tk.Button(win, text='비디오 선택', command=process_video)
quit_button = tk.Button(win, text='종료', bg="red", fg="white", command=quit_program)
save_button = tk.Button(win, text='단어 저장', command=save_words)
canvas = tk.Canvas(win, width=256, height=256, bg='lightgray', bd=4)
label_kr = tk.Label(win, width=16, height=1, bg='white', bd=4, text='한국어', anchor='w')
label_en = tk.Label(win, width=16, height=1, bg='white', bd=4, text='영어', anchor='w')
label_fr = tk.Label(win, width=16, height=1, bg='white', bd=4, text='프랑스어', anchor='w')
label_de = tk.Label(win, width=16, height=1, bg='white', bd=4, text='독일어', anchor='w')
tts_kr = tk.Button(win, text='듣기', command=tts_korean)
tts_en = tk.Button(win, text='듣기', command=tts_english)
tts_fr = tk.Button(win, text='듣기', command=tts_french)
tts_de = tk.Button(win, text='듣기', command=tts_deutsch)


# 위젯 배치
process_button.grid(row=0, column=0)
quit_button.grid(row=1, column=0)
save_button.grid(row=1, column=1, sticky='w', padx=35)
canvas.grid(row=0, column=1)
label_kr.grid(row=1, column=1, sticky='e')
label_en.grid(row=2, column=1, sticky='e')
label_fr.grid(row=3, column=1, sticky='e')
label_de.grid(row=4, column=1, sticky='e')
tts_kr.grid(row=1, column=2, sticky='w')
tts_en.grid(row=2, column=2, sticky='w')
tts_fr.grid(row=3, column=2, sticky='w')
tts_de.grid(row=4, column=2, sticky='w')

# 메인 루프 시작
win.mainloop()