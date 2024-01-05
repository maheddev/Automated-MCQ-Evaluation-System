import os
import xlsxwriter
import grading
from tkinter import messagebox


def generate(path, questions, choices, answer):
    workbook = xlsxwriter.Workbook("scores.xlsx")
    worksheet = workbook.add_worksheet("scores")
    worksheet.write(0, 0, "Sr.No.")
    worksheet.write(0, 1, "Registration No.")
    worksheet.write(0, 2, "Score")

    listOfFiles = os.listdir(path)
    for index, file in enumerate(listOfFiles):
        score, rollNo = grading.detection((path + "/" + file), questions, choices, answer)

        worksheet.write(index + 1, 0, str(index + 1))
        worksheet.write(index + 1, 1, rollNo)
        worksheet.write(index + 1, 2, score)

    workbook.close()
    result = messagebox.askyesno("Excel Sheet Generated", "Excel sheet has been generated.\nDo you want to open it?")
    
    if result:
        file_path = os.path.abspath("scores.xlsx")
        os.system(f'start excel "{file_path}"')

