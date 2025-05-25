import random
import tkinter as tk
from tkinter import messagebox
import os

# 파일에서 단어 목록 불러오기
def load_words_to_dict(filename):
    words_dict = {'ko': {}, 'en': {}, 'fr': {}, 'de': {}}

    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:  # 빈 줄이 아닌 경우 처리
                    parts = line.split()
                    word_pair = {}
                    for part in parts:
                        if ':' in part:  # ":"가 포함된 경우만 처리
                            lang, word = part.split(':', 1)  # ":" 기준으로 분리
                            word_pair[lang] = word
                    # 각 언어의 단어들이 모두 존재할 경우에만 추가
                    if '한국어' in word_pair and '영어' in word_pair:
                        words_dict['ko'][word_pair['한국어']] = word_pair
                        words_dict['en'][word_pair['영어']] = word_pair
                    if '한국어' in word_pair and '프랑스어' in word_pair:
                        words_dict['ko'][word_pair['한국어']] = word_pair
                        words_dict['fr'][word_pair['프랑스어']] = word_pair
                    if '한국어' in word_pair and '독일어' in word_pair:
                        words_dict['ko'][word_pair['한국어']] = word_pair
                        words_dict['de'][word_pair['독일어']] = word_pair
                    if '영어' in word_pair and '프랑스어' in word_pair:
                        words_dict['en'][word_pair['영어']] = word_pair
                        words_dict['fr'][word_pair['프랑스어']] = word_pair
                    if '영어' in word_pair and '독일어' in word_pair:
                        words_dict['en'][word_pair['영어']] = word_pair
                        words_dict['de'][word_pair['독일어']] = word_pair
                    if '프랑스어' in word_pair and '독일어' in word_pair:
                        words_dict['fr'][word_pair['프랑스어']] = word_pair
                        words_dict['de'][word_pair['독일어']] = word_pair
    else:
        print(f"'{filename}' 파일이 존재하지 않습니다.")
    
    # 단어가 없는 경우 알림
    if not any(words_dict.values()):
        return None  # 빈 단어 사전 반환

    return words_dict


# 다국어 퀴즈 생성 함수
def translation_quiz(language_choice, words_dict):
    # 선택한 언어에 따라 문제와 정답을 다르게 생성
    if language_choice == 'ko':  # 한국어를 선택한 경우
        target_language = random.choice(['en', 'fr', 'de'])  # 영어, 프랑스어, 독일어 중 하나 선택
        word = random.choice(list(words_dict[target_language].keys()))  # 선택된 언어에서 단어 하나 선택
        correct_answer = words_dict[target_language][word]['한국어']  # 한국어 번역어
        question = word  # 선택된 언어의 단어를 보고 한국어를 맞추는 문제
    elif language_choice == 'en':  # 영어를 선택한 경우
        target_language = random.choice(['ko', 'fr', 'de'])
        word = random.choice(list(words_dict[target_language].keys()))
        correct_answer = words_dict[target_language][word]['영어']  # 영어 번역어
        question = word  # 선택된 언어의 단어를 보고 영어를 맞추는 문제
    elif language_choice == 'fr':  # 프랑스어를 선택한 경우
        target_language = random.choice(['ko', 'en', 'de'])
        word = random.choice(list(words_dict[target_language].keys()))
        correct_answer = words_dict[target_language][word]['프랑스어']  # 프랑스어 번역어
        question = word  # 선택된 언어의 단어를 보고 프랑스어를 맞추는 문제
    elif language_choice == 'de':  # 독일어를 선택한 경우
        target_language = random.choice(['ko', 'en', 'fr'])
        word = random.choice(list(words_dict[target_language].keys()))
        correct_answer = words_dict[target_language][word]['독일어']  # 독일어 번역어
        question = word  # 선택된 언어의 단어를 보고 독일어를 맞추는 문제
    else:
        target_language = 'en'
        word = random.choice(list(words_dict[target_language].keys()))
        correct_answer = word  # 영어 단어를 맞추는 문제
        question = word

    return correct_answer, question


# UI 업데이트 및 결과 처리 함수
def start_quiz(language_choice):
    filename = 'like.txt'
    words_dict = load_words_to_dict(filename)

    if words_dict is None:  # 단어 목록이 비어있으면
        messagebox.showerror("오류", "단어 목록이 비어있습니다. 퀴즈를 시작할 수 없습니다.")
        return

    # 선택한 언어의 단어 리스트 가져오기
    words = words_dict.get(language_choice, {})
    if not words:  # 단어 목록이 비어 있으면 오류 메시지 표시
        messagebox.showerror("오류", f"'{filename}' 파일에서 '{language_choice}' 언어의 단어를 찾을 수 없습니다.")
        return

    correct_count = 0
    total_count = 0

    def next_question():
        nonlocal correct_count, total_count

        # 다음 문제 생성
        correct_answer, question = translation_quiz(language_choice, words_dict)
        question_label.config(text=question)
        answer_entry.delete(0, tk.END)

        def check_answer():
            nonlocal correct_count, total_count

            user_answer = answer_entry.get().strip()

            if not user_answer:  # 입력 값이 비어있으면
                messagebox.showwarning("입력 오류", "단어를 입력해주세요.")
                return  # 함수 종료

            # 정답을 비교할 때 'correct_answer'와 비교
            if user_answer.lower() == correct_answer.lower():
                messagebox.showinfo("정답", f"정답입니다! 정답은 '{correct_answer}'입니다.")
                correct_count += 1
            else:
                messagebox.showinfo("틀림", f"틀렸습니다. 정답은 '{correct_answer}'입니다.")

            total_count += 1
            continue_quiz = messagebox.askyesno("계속?", "계속 퀴즈를 풀겠습니까?")
            if continue_quiz:
                next_question()  # 새로운 문제로 넘어감
            else:
                accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
                messagebox.showinfo("결과", f"퀴즈가 종료되었습니다.\n총 {total_count}문제 중 {correct_count}문제를 맞추셨습니다.\n정답률: {accuracy:.2f}%")
                # 퀴즈 종료 후 다시 시작할 수 있도록 창 초기화
                restart_quiz()

        check_button.config(command=check_answer)

    next_question()


# 퀴즈를 다시 시작하는 함수
def restart_quiz():
    start_button.config(state=tk.NORMAL)  # 퀴즈 시작 버튼을 다시 활성화


# UI 설정
root = tk.Tk()
root.title("다국어 번역 퀴즈")
root.geometry("500x400")
root.config(bg="lightblue")

language_label = tk.Label(root, text="언어를 선택하세요", bg="lightblue", font=("Arial", 12))
language_label.pack(pady=10)

language_choice = tk.StringVar()
language_choice.set("en")

language_ko = tk.Radiobutton(root, text="한국어", variable=language_choice, value="ko", bg="lightblue", font=("Arial", 10))
language_fr = tk.Radiobutton(root, text="프랑스어", variable=language_choice, value="fr", bg="lightblue", font=("Arial", 10))
language_de = tk.Radiobutton(root, text="독일어", variable=language_choice, value="de", bg="lightblue", font=("Arial", 10))
language_en = tk.Radiobutton(root, text="영어", variable=language_choice, value="en", bg="lightblue", font=("Arial", 10))

language_ko.pack()
language_fr.pack()
language_de.pack()
language_en.pack()

start_button = tk.Button(root, text="퀴즈 시작", command=lambda: start_quiz(language_choice.get()), font=("Arial", 12), bg="#87CEEB", width=20)
start_button.pack(pady=20)

question_label = tk.Label(root, text="", bg="lightblue", font=("Arial", 12))
question_label.pack(pady=10)

answer_entry = tk.Entry(root, font=("Arial", 12))
answer_entry.pack(pady=10)

check_button = tk.Button(root, text="정답 제출", font=("Arial", 12), bg="#87CEEB")
check_button.pack(pady=10)

# 종료 버튼 추가
quit_button = tk.Button(root, text="종료", command=root.destroy, font=("Arial", 10), bg="red", fg="white")
quit_button.place(x=10, y=10)  # 왼쪽 위 모서리에 배치 (x=10, y=10)

root.mainloop()
