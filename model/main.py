import tkinter as tk
from PIL import Image, ImageTk  # Pillow 라이브러리 임포트
import subprocess

# 각 파일을 실행하는 함수들
def open_quiz():
    subprocess.Popen(["python", "quiz.py"])

def open_interface():
    subprocess.Popen(["python", "interface.py"])

def open_history():
    subprocess.Popen(["python", "history.py"])

def open_vocabulary():
    subprocess.Popen(["python", "vocabulary.py"])

# 메인 윈도우 생성
main_window = tk.Tk()
main_window.title("다국어 공부 단어장")
main_window.geometry("400x400")

# Canvas 생성
canvas = tk.Canvas(main_window, width=400, height=400,bg="lightblue") 
canvas.pack(fill="both", expand=True)

# 배경 이미지 설정 (Pillow 사용)
bg_image = Image.open("배경.png")  # 이미지 저작권-작가 catalyststuff 출처 Freepik
bg_image = bg_image.resize((400, 300)) 
bg_image_tk = ImageTk.PhotoImage(bg_image, master=main_window)  # master 속성 사용

# 이미지 객체를 유지하기 위해 main_window에 할당
main_window.bg_image_tk = bg_image_tk  # 이미지 객체를 main_window의 속성으로 저장

# 배경 이미지 설정
canvas.create_image(0, 0, image=bg_image_tk, anchor="nw")

# 버튼들을 배경 이미지 바로 아래에 배치하기 위해 새로운 프레임 생성
button_frame = tk.Frame(main_window,bg="lightblue")
button_frame.place(relx=0.5, rely=0.85, anchor="center")  # 이미지 아래에 배치

# 버튼들을 수평으로 배치 (pack 사용)
button_1 = tk.Button(button_frame, text="단어 퀴즈", command=open_quiz)
button_1.pack(side="left", padx=10)

button_2 = tk.Button(button_frame, text="대화형 인터페이스", command=open_interface)
button_2.pack(side="left", padx=10)

button_3 = tk.Button(button_frame, text="검색 기록", command=open_history)
button_3.pack(side="left", padx=10)

button_4 = tk.Button(button_frame, text="단어 모음집", command=open_vocabulary)
button_4.pack(side="left", padx=10)

# mainloop()
main_window.mainloop()
