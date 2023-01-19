from flask import Flask, request, render_template, redirect
import os.path
import csv
from more_itertools import last
import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime


app = Flask(__name__)
global user_id
user_id = str(uuid.uuid4())
chosen_colour = None
offset = 0

global prolific_id

def get_paragraphs():
    global offset 
    paras = pd.read_csv("topic_paragraphs.csv", encoding="utf-8")
    ids = range(0+offset, 6+offset)
    texts = []
    for id in ids:
        texts.append(paras["text"][id])
    return ids, texts


def generate_id():
    path_name = "./query_gen_results/query_gen_results.csv"
    df = pd.read_csv(path_name)
    last_id = df['Participant_ID'].max()
    if np.isnan(last_id):
        last_id = 0
    return last_id + 1


def save_results(r1, r2, r3, r4, r5, ids, attention1):
    global user_id
    global prolific_id
    path_name = "./query_gen_results/" + user_id + ".csv"
    results = [[user_id, ids[0]+1, r1],
               [user_id, ids[1]+1, r2],
               [user_id, ids[2]+1, r3],
               [user_id, ids[3]+1, r4],
               [user_id, ids[4]+1, r5],
               [user_id, "attention1", attention1],
               ["prolific_id", prolific_id]]

    with open(path_name, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)


def get_new_paras():
    ids, texts = get_paragraphs()
    query_1 = texts[0]
    query_2 = texts[1]
    query_3 = texts[2]
    query_4 = texts[3]
    query_5 = texts[4]
    return query_1, query_2, query_3, query_4, query_5, ids


global query_1
global query_2
global query_3
global query_4
global query_5
global ids
global texts
ids, texts = get_paragraphs()
query_1 = texts[0]
query_2 = texts[1]
query_3 = texts[2]
query_4 = texts[3]
query_5 = texts[4]

@app.route("/form", methods=["GET", "POST"])
def query_gen():
    global query_1
    global query_2
    global query_3
    global query_4
    global query_5
    global ids
    global texts
    global chosen_colour
    global offset
    
    if request.method == 'POST':
        if "redirect_button" or "refresh_button" in request.form:
            result1 = str(request.form['query_1'])
            result2 = str(request.form['query_2'])
            result3 = str(request.form['query_3'])
            result4 = str(request.form['query_4'])
            result5 = str(request.form['query_5'])
            attention1 = str(request.form['attention_1'])
            attention_result = str(attention1.lower()==chosen_colour.lower())
            offset += 5
            save_results(result1, result2, result3, result4, result5, ids, attention_result)
            query_1, query_2, query_3, query_4, query_5, ids = get_new_paras()
            if "redirect_button" in request.form:
                return redirect('/final-thanks')
            if "refresh_button" in request.form:
                print(offset)
                return redirect('/form')
    else:
            possible_colours =  ["Red","Blue","Green","Orange","Brown"]
            chosen_colour = random.choice(possible_colours)
            return render_template("query_gen.html", query_1=query_1, query_2=query_2, query_3=query_3, query_4=query_4, query_5=query_5,random_attention=chosen_colour)

# Consent form testing
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # Create a PDF resource manager object that stores shared resources
        rsrcmgr = PDFResourceManager()
        # Create a string buffer for the extracted text
        text = StringIO()
        # Create a PDF device object
        device = TextConverter(rsrcmgr, text, laparams=LAParams())
        # Create a PDF interpreter object
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        # Process each page contained in the PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            interpreter.process_page(page)
        # Release the resources
        device.close()
        text = text.getvalue()
    return text

@app.route('/', methods=['GET', 'POST'])
def info_sheet():
    #out_text = extract_text_from_pdf("sas_enron_information_sheet.pdf")
    #out_text = out_text.replace('\n', '<br>')
    out_text = ""
    if request.method == 'POST':
        input_text = request.form['input_box']
    return render_template('info_sheet.html', text=out_text)

@app.route('/redirect', methods=['GET'])
def redirect_page():
    global prolific_id
    prolific_id = request.args.get('input_box')
    return redirect('/next')

@app.route('/next', methods=['GET', 'POST'])
def next_page():
    if request.method == 'POST':
        checkbox_state = request.form.get('checkbox')
        path_name = "./consent_checks/" + user_id + ".csv"

        with open(path_name, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            time_signed = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            writer.writerows([[user_id,time_signed]])
            print([user_id,time_signed])
        return redirect("/form")
    return render_template('consent_form.html')

@app.route('/final-thanks', methods=['GET','POST'])
def final_thanks():
    if request.method == "POST":
        return redirect("https://app.prolific.co/submissions/complete?cc=CSP88M3M")
    return render_template('final_thanks.html')