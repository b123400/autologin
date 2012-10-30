#!/usr/local/bin/python     
from Tkinter import *
import urllib
import tkMessageBox
import shelve
import time

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        global username,password,running
        self.status=StringVar()
        self.status.set("Not running")
        self.statusLabel= Label(self, textvariable=self.status)
        self.statusLabel.grid()

        Label(self, text="Username:").grid()
        self.usernameField= Entry(self)
        self.usernameField.grid()
        Label(self, text="Password:").grid()
        self.passwordField= Entry(self,show="*")
        self.passwordField.grid()

        d = shelve.open('autologin.data',writeback=True)
        if 'username' in d.keys():
            self.usernameField.insert(0,d['username'])
            username=d['username']
        if 'password' in d.keys():
            self.passwordField.insert(0,d['password'])
            password=d['password']

        self.doneButton=Button(self,text="Done",command=self.doneClicked)
        self.doneButton.grid()

        self.consoleBox= Text(self,width=50,height=5,borderwidth=0,highlightthickness=0)
        self.consoleBox.grid()
        self.consoleBox.insert("1.0","yo start now\n")

        self.after(1,self.timerCalled)

    def timerCalled(arg):
        global app,interval
        app.after(interval,app.timerCalled)
        if app.shouldRunTimer() :
            try:
                response=urllib.urlopen('http://www.apple.com/library/test/success.html')
                if response.geturl().find("securelogin.net.cuhk.edu.hk") != -1:
                    print('fucking login thing')
                    #Hell it's cuhk login!
                    param={'user':username,'password':password,'cmd':'authenticate'}
                    autologinHAHAHAHAHA=urllib.urlopen('http://securelogin.net.cuhk.edu.hk/cgi-bin/login?'+urllib.urlencode(param))
                    app.consoleLog("AUTO LOGGED IN")
                    if interval!=2000 :
                        interval=2000
                        app.consoleLog("increase frequence")
            except IOError as e:
                app.consoleLog("IOError, not connected to internet?")
                app.consoleLog("Slow down now")
                interval=30000
            except :
                pass
            app.status.set("Running: "+time.ctime())
        else:
            app.status.set("Not running")
            

    def doneClicked(sender):
        global app,username,password
        if app.usernameField.get()!="" and app.passwordField.get()!="" :
            username=app.usernameField.get()
            password=app.passwordField.get()
            d = shelve.open('autologin.data',writeback=True)
            d['username']=username
            d['password']=password
            d.close()
        else:
            d = shelve.open('autologin.data',writeback=True)
            if app.usernameField.get()=="":
                app.usernameField.delete(0,len(app.usernameField.get()))
                app.usernameField.insert(0,d['username'])
            if app.passwordField.get()=="" :
                app.passwordField.delete(0,len(app.passwordField.get()))
                app.passwordField.insert(0,d['password'])
            tkMessageBox.showerror("HA?!", "username and password must not be empty ar!")

    def shouldRunTimer(sender):
        if username!="" and password!="" :
            return True
        return False

    def consoleLog(sender,_text):
        global app
        app.consoleBox.insert(END,time.ctime()+":"+_text+'\n')
        app.consoleBox.see(END)

interval=2000
username=""
password=""

app = Application()
app.master.title("CUHK always ask me to login!!!") 
app.mainloop()