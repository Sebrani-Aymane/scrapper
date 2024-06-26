import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

def fetch_stackoverflow_answer(urls):
    all_questions_answers = []

    for url in urls:
        page_to_scrape = requests.get(url)
        soup = BeautifulSoup(page_to_scrape.text, "html.parser")

        question_div = soup.find('div', id="question")
        question_text = "No question found."
        if question_div:
            p = question_div.find('p')
            if p:
                question_text = p.text

        answers_div = soup.find('div', id="answers")
        answers_texts = []

        if answers_div:
            answer_divs = answers_div.find_all('div', class_='answer', limit=3)
            for index, answer_div in enumerate(answer_divs):
                paragraphs = answer_div.find_all('p')
                answer_text = "\n".join(p.text for p in paragraphs)
                answers_texts.append("Answer {}:\n{}\n".format(index + 1, answer_text))

        all_questions_answers.append((question_text, answers_texts))

    return all_questions_answers

def show_answers():
    urls = [url.strip() for url in text_entry.get("1.0", "end-1c").splitlines() if url.strip()]
    if urls:
        all_questions_answers = fetch_stackoverflow_answer(urls)

        answer_text.config(state=tk.NORMAL)
        answer_text.delete("1.0", tk.END)

        for i, (question_text, answers_texts) in enumerate(all_questions_answers, start=1):
            answers_text = "Question {}:\n{}\n\n".format(i, question_text)
            answers_text += "\n\n".join(answers_texts)
            answers_text += "\n\n" 

            answer_text.insert(tk.END, answers_text)

        answer_text.config(state=tk.DISABLED)
    else:
        answer_text.config(state=tk.NORMAL)
        answer_text.delete("1.0", tk.END)
        answer_text.insert(tk.END, "Please enter at least one Stack Overflow question URL.")
        answer_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Stack Overflow Answer Fetcher")


style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TText', font=('Helvetica', 12))


entry_label = ttk.Label(root, text="Enter Stack Overflow question URLs (one per line):")
entry_label.pack(pady=(10, 0))

text_entry = tk.Text(root, height=5, width=50, font=('Helvetica', 12))
text_entry.pack(pady=5)

button = ttk.Button(root, text="Get Answers", command=show_answers)
button.pack(pady=10)

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(pady=0, fill=tk.BOTH, expand=True)

canvas = tk.Canvas(scrollable_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

answer_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=answer_frame, anchor="nw")

answer_text = tk.Text(answer_frame, wrap=tk.WORD, font=('Helvetica', 12), state=tk.DISABLED)
answer_text.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

root.mainloop()
