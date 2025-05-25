import tkinter as tk
from tkinter import simpledialog, messagebox
import os

# 단어 저장 리스트
searched_words = {"Korean": [], "English": [], "French": [], "German": []}

# 단어 저장 및 검색 기록 파일 경로
history_file = "words.txt"
like_file = "like.txt"

# 'words.txt' 파일에서 단어 읽기
def load_words_from_file():
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8", errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        # 각 언어를 분리하여 단어 리스트에 추가
                        parts = line.split("   ")  # 각 언어는 공백 3개로 구분되어 있다고 가정
                        if len(parts) == 4:
                            korean_part = parts[0].split(":")[1].strip()
                            english_part = parts[1].split(":")[1].strip()
                            french_part = parts[2].split(":")[1].strip()
                            german_part = parts[3].split(":")[1].strip()
                            searched_words["English"].append(english_part)
                            searched_words["French"].append(french_part)
                            searched_words["German"].append(german_part)
                            searched_words["Korean"].append(korean_part)
        except UnicodeDecodeError:
            with open(history_file, "r", encoding="ISO-8859-1") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        parts = line.split("   ")
                        if len(parts) == 4:
                            korean_part = parts[0].split(":")[1].strip()
                            english_part = parts[1].split(":")[1].strip()
                            french_part = parts[2].split(":")[1].strip()
                            german_part = parts[3].split(":")[1].strip()
                            searched_words["English"].append(english_part)
                            searched_words["French"].append(french_part)
                            searched_words["German"].append(german_part)
                            searched_words["Korean"].append(korean_part)

# 단어 검색 및 뜻을 출력하는 함수
def search_word():
    word = simpledialog.askstring("단어 검색", "검색할 단어를 입력하세요:")
    if word:
        word = word.strip().lower()  # 입력값 공백 제거 및 소문자로 변환
        found = False
        translations = {"English": "", "French": "", "German": "", "Korean": ""}
        
        for lang, words in searched_words.items():
            if word in words:
                found = True
                idx = words.index(word)
                translations["English"] = searched_words["English"][idx]
                translations["French"] = searched_words["French"][idx]
                translations["German"] = searched_words["German"][idx]
                translations["Korean"] = searched_words["Korean"][idx]

        if found:
            update_searched_words_display()
            messagebox.showinfo("단어 뜻", f"'{word}'의 번역:\n"
                                          f"Korean: {translations['Korean']}\n"
                                          f"English: {translations['English']}\n"
                                          f"French: {translations['French']}\n"
                                          f"German: {translations['German']}")
        else:
            messagebox.showinfo("단어 뜻", f"'{word}'에 대한 뜻을 찾을 수 없습니다.")
    else:
        messagebox.showwarning("경고", "단어를 입력하지 않았습니다.")

# 즐겨찾기 저장 (중복 방지)
def add_to_favorites(english_word, french_word, german_word, korean_word):
    # 이미 즐겨찾기에 추가된 단어인지 확인
    if os.path.exists(like_file):  # 파일 존재 여부 확인
        with open(like_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if korean_word in line and english_word in line and french_word in line and german_word in line:
                    # 이미 즐겨찾기에 있는 단어라면 메시지 출력
                    messagebox.showinfo("즐겨찾기", "해당 단어는 이미 즐겨찾기에 추가되었습니다.")
                    return

    # 중복이 없다면 즐겨찾기에 추가
    with open(like_file, "a", encoding="utf-8") as file:
        file.write(f"한국어:{korean_word} 영어:{english_word} 프랑스어:{french_word} 독일어:{german_word}\n")
    messagebox.showinfo("즐겨찾기", f"'{korean_word}', '{english_word}', '{french_word}', '{german_word}'을(를) 즐겨찾기에 추가했습니다.")



# 단어 삭제 (세 언어에서 동시에 삭제)
def delete_word(english_word, french_word, german_word, korean_word):
    with open(history_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(history_file, "w", encoding="utf-8") as file:
        for line in lines:
            if line.strip():
                if korean_word not in line and english_word not in line and french_word not in line and german_word not in line:
                    file.write(line)
    
    if english_word in searched_words["English"]:
        searched_words["English"].remove(english_word)
    if french_word in searched_words["French"]:
        searched_words["French"].remove(french_word)
    if german_word in searched_words["German"]:
        searched_words["German"].remove(german_word)
    if korean_word in searched_words["Korean"]:
        searched_words["Korean"].remove(korean_word)

    update_searched_words_display()
    messagebox.showinfo("삭제", "단어가 삭제되었습니다.")

# 메인 창에 검색 기록 표시
def update_searched_words_display():
    for widget in history_frame.winfo_children():
        widget.destroy()

    # 폰트 설정
    header_font = ("Arial", 12, "bold")
    content_font = ("Arial", 10)
    button_font = ("Arial", 8)

    # 전체 컨테이너 프레임
    container_frame = tk.Frame(history_frame, bg="white")
    container_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # 헤더 프레임
    header_frame = tk.Frame(container_frame, bg="lightgray")
    header_frame.pack(fill=tk.X)

    # 헤더
    header = tk.Frame(header_frame, bg="lightgray", relief="solid")
    header.pack(fill="x")

    tk.Label(header, text="한국어", bg="lightgray", font=("Arial", 12, "bold"), width=8, anchor="center").grid(row=0, column=0, padx=1)
    tk.Label(header, text="영어", bg="lightgray", font=("Arial", 12, "bold"), width=8, anchor="center").grid(row=0, column=1, padx=1)
    tk.Label(header, text="프랑스어", bg="lightgray", font=("Arial", 12, "bold"), width=9, anchor="center").grid(row=0, column=2, padx=1)
    tk.Label(header, text="독일어", bg="lightgray", font=("Arial", 12, "bold"), width=10, anchor="center").grid(row=0, column=3, padx=1)
    tk.Label(header, text="관리", bg="lightgray", font=("Arial", 12, "bold"), width=12, anchor="center").grid(row=0, column=4, padx=1)

    max_words = max(len(searched_words["English"]), len(searched_words["French"]),
                    len(searched_words["German"]), len(searched_words["Korean"]))

    for i in range(max_words):
        korean_word = searched_words["Korean"][i] if i < len(searched_words["Korean"]) else ""
        english_word = searched_words["English"][i] if i < len(searched_words["English"]) else ""
        french_word = searched_words["French"][i] if i < len(searched_words["French"]) else ""
        german_word = searched_words["German"][i] if i < len(searched_words["German"]) else ""

        word_row = tk.Frame(container_frame, bg="white")
        word_row.pack(fill=tk.X, pady=2)

        # 단어를 grid로 정렬
        tk.Label(word_row, text=korean_word, font=content_font, bg="white", width=9, anchor="center").grid(row=0, column=0, padx=5)
        tk.Label(word_row, text=english_word, font=content_font, bg="white", width=10, anchor="center").grid(row=0, column=1, padx=5)
        tk.Label(word_row, text=french_word, font=content_font, bg="white", width=10, anchor="center").grid(row=0, column=2, padx=5)
        tk.Label(word_row, text=german_word, font=content_font, bg="white", width=10, anchor="center").grid(row=0, column=3, padx=5)

        manage_frame = tk.Frame(word_row, bg="white")
        manage_frame.grid(row=0, column=4, padx=5)

        tk.Button(manage_frame, text="즐겨찾기", font=button_font,
                  command=lambda e=english_word, f=french_word, g=german_word, k=korean_word: add_to_favorites(e, f, g, k)).grid(row=0, column=0, padx=5)
        tk.Button(manage_frame, text="삭제", font=button_font,
                  command=lambda e=english_word, f=french_word, g=german_word, k=korean_word: delete_word(e, f, g, k)).grid(row=0, column=1, padx=5)



# GUI 인터페이스 만들기
root = tk.Tk()
root.title("단어 검색 프로그램")
root.geometry("550x400")
root.config(bg="lightblue")

# 제목 프레임
top_frame = tk.Frame(root, bg="lightblue")
top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

# 제목라벨
title_label = tk.Label(root, text="검색 기록", bg="lightblue", font=("Arial", 16, "bold"))
title_label.pack(pady=5)

# 단어 검색 버튼
search_button = tk.Button(top_frame, text="단어 검색", command=search_word, font=("Arial", 10, "bold"), bg="gray", fg="white")
search_button.pack(side=tk.RIGHT, padx=5)

# 종료 버튼
exit_button = tk.Button(top_frame, text="종료", command=root.quit, font=("Arial", 10, "bold"), bg="red", fg="white")
exit_button.pack(side=tk.LEFT, padx=5)

# 히스토리 프레임 (history_frame)
history_frame = tk.Frame(root, bg="white", bd=2, relief="solid")
history_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

load_words_from_file()
update_searched_words_display()

root.mainloop()