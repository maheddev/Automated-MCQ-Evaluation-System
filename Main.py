import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import GenerateExcel


def selectFolder():
    path = filedialog.askdirectory()
    path = r'{}'.format(path)
    path = rf'{path}'
    return path


def submit_answers():
    selected_responses = [var_list[i].get()
                          for i in range(num_questions.get())]
    print("Selected Responses:", selected_responses)
    generate(num_questions.get(), choices_per_question.get(), selected_responses)


def generate(questions, choices, answers):
    path = selectFolder()
    GenerateExcel.generate(path, questions, choices, answers)


root = tk.Tk()
root.title("Automated MCQ Evaluation System")


def add_padding(widget, padx=5, pady=5):
    widget.pack(padx=padx, pady=pady)


# Center-align horizontally and vertically
root.geometry("500x950")  # Set a fixed size for the window

# Center the components vertically
for _ in range(5):
    tk.Label(root, text="").pack()

# Title Label
title_label = tk.Label(
    root, text="Automated MCQ Evaluation System", font=("Helvetica", 18), pady=10)
add_padding(title_label)

# Number of Questions Section
num_questions_frame = tk.Frame(root)
add_padding(num_questions_frame, pady=10)

num_questions_label = tk.Label(
    num_questions_frame, text="Number of Questions: ", font=("Arial", 13))
num_questions_label.pack(side=tk.LEFT)

num_questions = tk.IntVar()
num_questions_entry = ttk.Entry(
    num_questions_frame, textvariable=num_questions, width=20, font=("Arial", 13))
num_questions_entry.pack(side=tk.RIGHT)

# Number of Choices Section
choices_frame = tk.Frame(root)
add_padding(choices_frame, pady=10)

choices_label = tk.Label(choices_frame, text="Number of Choices:   ", font=("Arial", 13))
choices_label.pack(side=tk.LEFT)

choices_per_question = tk.IntVar()
choices_entry = ttk.Entry(
    choices_frame, textvariable=choices_per_question, width=20, font=("Arial", 13))
choices_entry.pack(side=tk.RIGHT)

create_questions_button = tk.Button(
    root, text="Generate Response Sheet", command=lambda: create_questions())
create_questions_button.configure(
        width=34,              
        bg="black",             
        fg="white",            
        font=("Cursive", 12, "bold")  
    )
add_padding(create_questions_button)

var_list = []


def create_questions():
    num_choices = choices_per_question.get()

    num_questions_frame.pack_forget()
    choices_frame.pack_forget()
    create_questions_button.pack_forget()
    tk.Label(root, text="Select the correct choices", font=("Arial", 12, "bold")).pack(pady=10)

    for i in range(num_questions.get()):
        question_frame = tk.Frame(root)
        add_padding(question_frame, pady=5)

        question_label = tk.Label(question_frame, text=f"{i + 1}:", font=("Arial", 10), foreground="green")
        question_label.pack(side=tk.LEFT)

        var = tk.IntVar()
        var_list.append(var)

        for j in range(num_choices):
            radio_button = tk.Radiobutton(
                question_frame, text=f"{j + 1}", variable=var, value=j, font=("Arial", 10), foreground="green")
            radio_button.pack(side=tk.LEFT)

    submit_button = tk.Button(
        root, text="Select Folder", command=submit_answers)
    submit_button.configure(
        width=20,              
        bg="black",             
        fg="white",            
        font=("Cursive", 12, "bold")  
    )
    add_padding(submit_button)


root.mainloop()
