import tkinter as tk
from tkinter import messagebox
import os

# 즐겨찾기 단어 목록을 저장할 파일 경로
like_file = "like.txt"

# 즐겨찾기 단어 목록
favorite_words = []

# like.txt 파일에서 즐겨찾기 목록을 불러오는 함수
def load_favorites_from_file():
    """like.txt 파일에서 즐겨찾기 목록을 불러오는 함수"""
    global favorite_words
    favorite_words = []  # 초기화
    if os.path.exists(like_file):
        with open(like_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip():
                    parts = line.split()  # 공백으로 나누기
                    try:
                        korean_word = parts[0].split(":")[1]
                        english_word = parts[1].split(":")[1]
                        french_word = parts[2].split(":")[1]
                        german_word = parts[3].split(":")[1]
                        favorite_words.append({
                            "Korean": korean_word,
                            "English": english_word,
                            "French": french_word,
                            "German": german_word,
                        })
                    except IndexError:
                        print(f"파일 형식 오류: {line.strip()}")

# 즐겨찾기에서 단어를 삭제하는 함수
def remove_from_favorites(index):
    """즐겨찾기에서 단어를 삭제하는 함수"""
    del favorite_words[index]
    save_favorites_to_file()  # 삭제 후 파일에 저장
    update_favorites_display()  # 단어 목록을 갱신
    messagebox.showinfo("삭제 ", "단어가 삭제되었습니다.")  # 삭제 알림

# 즐겨찾기 목록을 like.txt 파일에 저장하는 함수
def save_favorites_to_file():
    """즐겨찾기 단어 목록을 like.txt 파일에 저장하는 함수"""
    try:
        with open(like_file, "w", encoding="utf-8") as file:
            for word_data in favorite_words:
                # 올바른 형식으로 저장
                file.write(f"한국어:{word_data['Korean']} 영어:{word_data['English']} 프랑스어:{word_data['French']} 독일어:{word_data['German']}\n")
    except Exception as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def update_favorites_display():
    """즐겨찾기 단어 목록을 업데이트하고 화면에 표시"""
    for widget in word_frame.winfo_children():
        widget.destroy()  # 기존의 모든 위젯을 삭제

    # 헤더
    header = tk.Frame(word_frame, bg="lightgray", relief="solid")
    header.pack(fill="x")

    tk.Label(header, text="한국어", bg="lightgray", font=("Arial", 12, "bold"), width=8, anchor="center").pack(side="left", padx=1)
    tk.Label(header, text="영어", bg="lightgray", font=("Arial", 12, "bold"), width=8, anchor="center").pack(side="left", padx=1)
    tk.Label(header, text="프랑스어", bg="lightgray", font=("Arial", 12, "bold"), width=9, anchor="center").pack(side="left", padx=1)
    tk.Label(header, text="독일어", bg="lightgray", font=("Arial", 12, "bold"), width=10, anchor="center").pack(side="left", padx=1)
    tk.Label(header, text="관리", bg="lightgray", font=("Arial", 12, "bold"), width=12, anchor="center").pack(side="left", padx=5)

    # 단어 목록
    if favorite_words:
        for index, word_data in enumerate(favorite_words):
            word_row = tk.Frame(word_frame, bg="white", relief="solid")
            word_row.pack(fill="x", pady=2)

            tk.Label(word_row, text=word_data["Korean"], bg="white", font=("Arial", 10), width=10, anchor="center").pack(side="left", padx=1)
            tk.Label(word_row, text=word_data["English"], bg="white", font=("Arial", 10), width=9, anchor="center").pack(side="left", padx=1)
            tk.Label(word_row, text=word_data["French"], bg="white", font=("Arial", 10), width=12, anchor="center").pack(side="left", padx=1)
            tk.Label(word_row, text=word_data["German"], bg="white", font=("Arial", 10), width=14, anchor="center").pack(side="left", padx=1)

            # 삭제 버튼
            delete_button = tk.Button(word_row, text="삭제", command=lambda idx=index: remove_from_favorites(idx))
            delete_button.pack(side="left", padx=5)
    else:
        tk.Label(word_frame, text="즐겨찾기된 단어가 없습니다.", bg="white", font=("Arial", 12)).pack(pady=20)


# 즐겨찾기 화면 표시
def display_favorites_screen():
    """즐겨찾기 단어 화면을 표시"""
    load_favorites_from_file()  # 즐겨찾기 목록 불러오기

    global word_frame
    window = tk.Tk()
    window.title("단어 모음집")
    window.geometry("500x400")  # 창 크기를 400x400으로 설정
    window.config(bg="lightblue")

    # 제목 프레임
    top_frame = tk.Frame(window, bg="lightblue")
    top_frame.pack(fill="x")

    # 종료 버튼 (왼쪽 상단)
    exit_button = tk.Button(top_frame, text="종료", font=("Arial", 10, "bold"), bg="red", fg="white", command=window.destroy)
    exit_button.pack(side="left", padx=5, pady=5)

    # 제목 라벨
    title_label = tk.Label(window, text="단어 모음집", bg="lightblue", font=("Arial", 16, "bold"))
    title_label.pack(pady=5)

    # 단어 표시 프레임
    word_frame = tk.Frame(window, bg="white", bd=2, relief="solid")
    word_frame.pack(fill="both", expand=True, padx=20, pady=10)

    update_favorites_display()  # 단어 목록 표시

    window.mainloop()


# 프로그램 실행
if __name__ == "__main__":
    display_favorites_screen()
