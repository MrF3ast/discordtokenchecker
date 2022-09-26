import os
import sys

import tkinter as tk
from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
from PIL import Image,ImageTk
import webbrowser
import requests

window = tk.Tk()

window.geometry("400x200")
window.maxsize(400, 200)
window.minsize(400, 200)
window.title("Token Checker")
window.iconbitmap("assets/discord.ico")
window.resizable(False, False)

canvas = Canvas(window, width=400, height=200)
canvas.pack()
canvas.config(background="#36393f")

discordFont = Font(family="Arial", size=18)
titleFont = Font(family="Arial", size=30)

userToken = tk.StringVar()

def runProgram():
	if userToken.get() == "" or userToken.get() == "Token":
		tk.messagebox.showerror(title="Error", message="Please enter a discord token to check!")
		return
	discordUserToken = userToken.get()
	ctrheaders = {'Authorization': discordUserToken, 'Content-Type': 'application/json'}
	checktokenr = requests.get('https://discordapp.com/api/v6/users/@me', headers=ctrheaders)
	if checktokenr.status_code == 200:
		checktokenrjson = checktokenr.json()
		UserName = f'{checktokenrjson["username"]}#{checktokenrjson["discriminator"]}'
		UserID = checktokenrjson['id']
		Email = checktokenrjson['email']
		PhoneNumber = checktokenrjson['phone']
		MfaEnabled = checktokenrjson['mfa_enabled']
		with open(f'cache/{UserName}.txt', 'w') as f:
			notepadContent = f"""Username: {UserName}
User ID: {UserID}
Email: {Email}
Phone Number: {PhoneNumber}
MFA-Enabled: {MfaEnabled}

Token: {discordUserToken}"""
			f.write(notepadContent)
		tk.messagebox.showinfo(title="Success", message=f"Valid Token, saved to cache/{UserName}.txt")
	else:
		tk.messagebox.showerror(title="Error", message="Invalid Token")
	Token.delete(0, 'end')
	Token.insert(0, 'Token')

def openLink(link):
	webbrowser.open(link, new=2)
def closeWindow():
	window.destroy()
def disableEvent():
	pass
def TokenDelete(*args):
	Token.delete(0, 'end')

title = Label(window, text="Token Checker", font=titleFont, bg="#32353b", fg="#ffffec")
title.place(x=97, y=12)

Token = tk.Entry(window, font=discordFont,justify=CENTER, textvariable=userToken, bg="#32353b", fg="#ffffec", insertbackground="#ffffec", insertwidth=1, borderwidth=0, highlightthickness=3, highlightcolor="#2f3136", highlightbackground="#2f3136", width=20)
Token.insert(0, 'Token')
Token.place(x=100, y=90)
Token.bind("<Button-1>", TokenDelete)

onebut = tk.Button(text="Check Token",width=12,height=1,bg="#7289da",activebackground="#7289da", activeforeground="#ffffec",fg="#ffffec",command=runProgram,borderwidth=2, font=discordFont)
onebut.place(x=145, y=135)

closebutton = tk.Button(text="X",width=2,height=1,bg="#32353b",fg="#ffffec",borderwidth=0,activebackground="#2f3136",activeforeground="#32353b",command=closeWindow,)
closebutton.place(x=378, y=2)

canvas.create_rectangle(0, 0, 70, 400, fill='#2f3136', outline='')
canvas.create_rectangle(0, 0, 400, 70, fill='#32353b', outline='')

discordIcon = ImageTk.PhotoImage(Image.open("assets/discord.ico"))
canvas.create_image(35,35,image=discordIcon)

discordServer = ImageTk.PhotoImage(Image.open("assets/discordServer.ico"))
discordServerButton = Button(window, image = discordServer, borderwidth=0, bg='#2f3136', activebackground="#2f3136", command=lambda: openLink("https://discord.com/invite/3sxXePZEMK"),)
discordServerButton.place(x=11, y=80,)

canvas.create_line(5, 84, 5, 127, width=3, fill='#ffffec')

window.eval('tk::PlaceWindow . center')
window.protocol("WM_DELETE_WINDOW", disableEvent)

window.mainloop()