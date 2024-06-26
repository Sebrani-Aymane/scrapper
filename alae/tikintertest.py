import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests


def fetch_stackoverflow_answer(url):
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
            answers_texts.append(f"Answer {index + 1}:\n{answer_text}\n")
    return question_text, answers_texts


def show_answer():
    question = text_entry.get("1.0", "end-1c")
    if question.strip():

        url = "https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python/6581949#6581949"
        question_text, answers_texts = fetch_stackoverflow_answer(url)
        answers_text = f"Question: {question_text}\n\n" + "\n\n".join(answers_texts)
        answer_text.delete("1.0", tk.END)
        answer_text.insert(tk.END, answers_text)
    else:
        answer_text.config(text="Please enter a question.")


root = tk.Tk()
root.title("Question and Answer App")


style = ttk.Style()
style.theme_use('clam')  
style.configure('TLabel', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12), padding=5)
style.configure('TText', font=('Helvetica', 12))

entry_label = ttk.Label(root, text="Enter your question:")
entry_label.pack(pady=(10, 0))

text_entry = tk.Text(root, height=5, width=50, font=('Helvetica', 12))
text_entry.pack(pady=5)

button = ttk.Button(root, text="Get Answer", command=show_answer)
button.pack(pady=10)

scrollable_frame = ttk.Frame(root)
scrollable_frame.pack(pady=0, fill=tk.BOTH, expand=True)


canvas = tk.Canvas(scrollable_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


# scrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL, command=canvas.yview)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Canvas to work with the Scrollbar
# canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

answer_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=answer_frame, anchor="nw")

answer_text = tk.Text(answer_frame, wrap=tk.WORD, font=('Helvetica', 12))
answer_text.pack(pady=3, padx=3, fill=tk.BOTH, expand=True)

root.mainloop()
