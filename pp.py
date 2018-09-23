# -*- coding: utf-8 -*- 
from flask import Flask, url_for, render_template, redirect, request
import subprocess
import os
import re
 
app = Flask(__name__)

folder_stack = []
regex = r'\d+:\d+'


@app.route("/")
def index():
    return "hellow flask!"

@app.route("/run")
def runcommand():
    current_path, formatted_result, item_count_int_current_folder, exception_in = run()
    return render_template('file_list.html', result=formatted_result, current_path=current_path)  

@app.route("/temp")
def temp():
    return render_template('main.html', name="name")

def whoami(command = "whoami"):
    result =subprocess.run([command, "", "/dev/null"], capture_output=True)
    return result

@app.route("/cdin")
def cdin(): 
    folder = request.args.get('submit_button') 
    folder_stack.append(folder) 
    return redirect(url_for('runcommand'))

@app.route("/cdout")
def cdout():
    back_format()
    return redirect(url_for('runcommand'))

def back_format():
    if folder_stack==[]:
        folder_stack.append("/home")

    if len(folder_stack) > 1:
        folder_stack.pop()

def format_folder_path():
    if folder_stack == []:
        folder_stack.append("/home")
    return '/'.join(folder_stack)
      
def format_result(result):
    result_temp = []
    excpetion_in = False
    formatted_result = []

    try:
        result_temp = result.decode('utf-8').strip().split('\n')
        result_temp.pop(0)
        print(result_temp)
    except Exception:
        excpetion_in = True

    if len(result_temp) == 0 or excpetion_in:
        return formatted_result

    for line in result_temp:
        file_name = None
        try:
            ## example string for regex ( "drwxrwxr-x  2 burhanc burhanc 4096 Eyl 22 16:21 local/" )
            ## regex '\d+:\d+', bulmasını istedigim yer ise örnek stringdeki 16:21 parçası, no such group exception atıyor
            emem = re.search(regex, line)
            file_name = line.split(emem.group(0))[1].strip()
        except Exception as ex:
            file_name = line.split(" ")[-1]
    
        if line.startswith("d"): 
            formatted_result.append(TemplateItem(file_name, True))
        else:
            formatted_result.append(TemplateItem(file_name, False))

    for i in formatted_result:
        print(i)

    return formatted_result

#run the list command and return the result 
def run():
    current_path = format_folder_path()
    all_files = None
    exception_in = False
    formatted_result = []
    item_count_int_current_folder = 0
    try:
        all_files = subprocess.check_output(['ls', '-l', current_path])
    except Exception as ex:
        exception_in = True

    if exception_in:
        back_format() #fail in the target folder so stay in current
        return current_path, formatted_result, item_count_int_current_folder, exception_in
    else:
        if all_files == None:
            all_files = []
        formatted_result = format_result(all_files)
        item_count_int_current_folder = len(formatted_result)
        return current_path, formatted_result, item_count_int_current_folder, exception_in


### directory and file name object
class TemplateItem:

    def __init__(self, name="", dirr =False):
        self.name = name
        self.dirr = dirr

    def __repr__(self):
        return repr(self.name)


if __name__ == '__main__':
    app.run()
