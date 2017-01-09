import Tkinter as tk
from Tkinter import *
import ttk

import base64
import urllib

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

#imports webScrape.py for web scraping 
import webScrape
from webScrape import *

import time

from decimal import *

class candidate(object):
    candidates = {}
    def __init__(self, state, name):
        self.state = state
        self.name = name
        self.data = webScrape.scrape([self.state]) #pulls data on that state
        for i in range(len(self.data)):
            if self.data[i][3] == self.name: #matches state to candidate
                self.x = self.data[i][1]
                self.y = self.data[i][2]

    """
    Applies linear regression to the data. Adds the state,
    the y-intercept and the slope to candidate.candidates
    """
    def linearReg(self):
        xy = 0
        xSquared = 0
        for i in range(len(self.x)): #creates term xy for linear regression
            xy += (self.x[i] * self.y[i])
        for i in range(len(self.x)): #creates term xSquared for linear regression
            xSquared += self.x[i] ** 2
        getcontext().prec = 6
        #equation for finding the intercept through linear regression
        self.intercept = (sum(self.y) * (xSquared) - sum(self.x) *  xy + 0.0) / (len(self.x) *  xSquared - sum(self.x) ** 2 + 0.0)
        #Finds slope through linear regression
        self.slope = (len(self.x) * xy - sum(self.x) * sum(self.y) + 0.0) / (len(self.x) * xSquared - sum(self.x) ** 2 + 0.0)
        #candidate.candidates[self.state + "/" + self.name] = self.intercept, self.slope, self.primaryDate
        return self.intercept, self.slope

def drawGraph(x, y, name, state, chance):  #Uses matplotlib to create a graph of polls and best fit line
    plt.plot(x, y,'ro')
    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    plt.plot(x, y, 'yo', x, fit_fn(x), linewidth = 2)
    plt.title('Chance of %s winnning %s: %.2f' % (name, state, chance))
    plt.ylabel('Chance of winning')
    plt.xlabel('Poll date')
    plt.show()

def findResult(lst):
    #y-intercept + run(date of primary) * slope
    #returns predicted chance of winning at the time of the election
    return lst[0] + int(time.strftime("%m%d")) * lst[1]

FONT= ("Arial 20 bold")


# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter

###################################
# Top level init
###################################

class main(tk.Tk):

    def __init__(self):
        
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        self.states = ["New Jersey", "Conn", "Maryland", "Penn.", "Rhode Island","Indiana","California","New Jersey"]
        self.wm_title("Predicting the Primaries")
        self.frames = {}

        for page in (StartPage, Democrats, Republicans, Hillary, Bernie, Trump, Cruz, Kasich): #Creates a new page

            frame = page(container, self)

            self.frames[page] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont): #Brings new page to the front

        frame = self.frames[cont]
        frame.tkraise()

###################################
# Start page
###################################

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Primary Predictor", font="Arial 24 bold")
        label.pack(pady=10,padx=10)

        label = tk.Label(self, text="Choose a Party to Continue:", font="Helvetica 14")
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Democrats",
                            command=lambda: controller.show_frame(Democrats))
        button.pack(pady = 20)

        button2 = ttk.Button(self, text="Republicans",
                            command=lambda: controller.show_frame(Republicans))
        button2.pack()



class Democrats(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Democrats", font=FONT, fg = "blue")
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Hillary",
                            command=lambda: controller.show_frame(Hillary))
        button2.pack()
        label = tk.Label(self, text="Hillary has 81% of the delgates needed to win", font="Arial 13")
        label.pack(pady=10,padx=10)
        
        button3 = tk.Button(self, text="Bernie",
                            command=lambda: controller.show_frame(Bernie))
        button3.pack()

        #Information taken from http://www.slate.com/blogs/the_slatest/2016/04/20/bernie_sanders_won_t_win_here_s_the_math.html
        label = tk.Label(self, text="Bernie has 50% of the needed delgates", font="Arial 13")
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady = 50)


class Republicans(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Republicans", font=FONT, fg = "red")
        label.pack(pady=10,padx=10)

        button2 = tk.Button(self, text="Trump",
                            command=lambda: controller.show_frame(Trump))
        button2.pack(pady = 10)

        #source: "http://projects.fivethirtyeight.com/election-2016/delegate-targets/""
        label = tk.Label(self, text="Trump has 97% of the needed delgates", font="Arial 13")
        label.pack(pady=10,padx=10)

        button3 = tk.Button(self, text="Cruz",
                            command=lambda: controller.show_frame(Cruz))
        button3.pack(pady = 10)

        #source: "http://projects.fivethirtyeight.com/election-2016/delegate-targets/""
        label = tk.Label(self, text="Cruz has 56% of the needed delgates", font="Arial 13")
        label.pack(pady=10,padx=10)

        button4 = tk.Button(self, text="Kasich",
                            command=lambda: controller.show_frame(Kasich))
        button4.pack(pady = 10)

        #source: "http://projects.fivethirtyeight.com/election-2016/delegate-targets/""
        label = tk.Label(self, text="Kasich has 17% of the needed delgates", font="Arial 13")
        label.pack(pady=10,padx=10)
  
        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady = 50)
        
class Hillary(tk.Frame):
    def __init__(self, parent, controller):
        self.name = "Clinton"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Hillary Clinton", font=FONT)
        label.pack()

        label = tk.Label(self, text="Select a state to see %s's chances \n of winning that primary:" % self.name, font="Arial 13")
        label.pack(pady = 20)

        lb = Listbox(self, height=6)
        lb.pack(padx = 40, pady = 20)
        lb.insert(END,"Connecticut")
        lb.insert(END,"Maryland")
        lb.insert(END,"Pennsylvania")
        lb.insert(END,"Rhode Island")
        lb.insert(END,"Indiana")
        lb.insert(END,"California")
        lb.insert(END,"New Jersey")
        sb = Scrollbar(self,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        

        def get_state(event):
            index = lb.curselection()[0]
            self.state = lb.get(index)
            temp = candidate(self.state, self.name)
            chance = findResult(temp.linearReg())
            drawGraph(temp.x, temp.y, self.name, self.state, chance)


        button3 = tk.Button(self,text="Select")
        button3.pack(pady = 10)

        button3.bind('<ButtonRelease-1>', get_state)

        button2 = tk.Button(self, text="Back to Party",
                                    command=lambda: controller.show_frame(Democrats))
        button2.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Bernie(tk.Frame):
    def __init__(self, parent, controller):
        self.name = "Sanders"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Bernie", font=FONT)
        label.pack()

        button2 = tk.Button(self, text="Party",
                                    command=lambda: controller.show_frame(Democrats))
        button2.pack()

        label = tk.Label(self, text="Select a state to see %s's chances \n of winning that primary:" % self.name, font="Arial 13")
        label.pack(pady = 20)

        lb = Listbox(self, height=6)
        lb.pack(padx = 40, pady = 40)
        lb.insert(END,"Connecticut")
        lb.insert(END,"Maryland")
        lb.insert(END,"Pennsylvania")
        lb.insert(END,"Rhode Island")
        lb.insert(END,"Indiana")
        lb.insert(END,"California")
        lb.insert(END,"New Jersey")
        sb = Scrollbar(self,orient=VERTICAL)
        sb.pack(side=RIGHT)
        sb.configure(command=lb.yview)
        lb.configure(yscrollcommand=sb.set)


        def get_state(event): #draws graph of selected state
            index = lb.curselection()[0] #Gets which state has been selected
            self.state = lb.get(index)
            temp = candidate(self.state, self.name) #creates instance of candidate
            chance = findResult(temp.linearReg())
            drawGraph(temp.x, temp.y, self.name, self.state, chance)

        button3 = tk.Button(self,text="Select")
        button3.pack(pady = 10)

        button3.bind('<ButtonRelease-1>', get_state)

        button2 = tk.Button(self, text="Back to Party",
                                    command=lambda: controller.show_frame(Democrats))
        button2.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Trump(tk.Frame):
    def __init__(self, parent, controller):
        self.name = "Trump"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Donald Trump", font=FONT)
        label.pack()

        label = tk.Label(self, text="Select a state to see %s's chances \n of winning that primary:" % self.name, font="Arial 13")
        label.pack(pady = 20)

        lb = Listbox(self, height=6)
        lb.pack(padx = 40, pady = 40)
        lb.insert(END,"Connecticut")
        lb.insert(END,"Maryland")
        lb.insert(END,"Pennsylvania")
        lb.insert(END,"Rhode Island")
        lb.insert(END,"Indiana")
        lb.insert(END,"California")
        lb.insert(END,"New Jersey")
        sb = Scrollbar(self,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        

        def get_state(event):
            index = lb.curselection()[0]
            self.state = lb.get(index)
            temp = candidate(self.state, self.name)
            chance = findResult(temp.linearReg())
            drawGraph(temp.x, temp.y, self.name, self.state, chance)


        button3 = tk.Button(self,text="Select")
        button3.pack(pady = 10)

        button3.bind('<ButtonRelease-1>', get_state)

        button2 = tk.Button(self, text="Back to Party",
                                    command=lambda: controller.show_frame(Republicans))
        button2.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class Cruz(tk.Frame):
    def __init__(self, parent, controller):
        self.name = "Cruz"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Ted Cruz", font=FONT)
        label.pack()

        label = tk.Label(self, text="Select a state to see %s's chances \n of winning that primary:" % self.name, font="Arial 13")
        label.pack(pady = 20)

        lb = Listbox(self, height=6)
        lb.pack(padx = 40, pady = 40)
        lb.insert(END,"Connecticut")
        lb.insert(END,"Maryland")
        lb.insert(END,"Pennsylvania")
        lb.insert(END,"Rhode Island")
        lb.insert(END,"Indiana")
        lb.insert(END,"California")
        lb.insert(END,"New Jersey")
        sb = Scrollbar(self,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        

        def get_state(event):
            index = lb.curselection()[0]
            self.state = lb.get(index)
            temp = candidate(self.state, self.name)
            chance = findResult(temp.linearReg())
            drawGraph(temp.x, temp.y, self.name, self.state, chance)


        button3 = tk.Button(self,text="Select")
        button3.pack(pady = 10)

        button3.bind('<ButtonRelease-1>', get_state)

        button2 = tk.Button(self, text="Back to Party",
                                    command=lambda: controller.show_frame(Republicans))
        button2.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()


class Kasich(tk.Frame):
    def __init__(self, parent, controller):
        self.name = "Kasich"
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Jon Kasich", font=FONT)
        label.pack()


        label = tk.Label(self, text="Select a state to see %s's chances \n of winning that primary:" % self.name, font="Arial 13")
        label.pack(pady = 20)

        lb = Listbox(self, height=6)
        lb.pack(padx = 40, pady = 40)
        lb.insert(END,"Connecticut")
        lb.insert(END,"Maryland")
        lb.insert(END,"Pennsylvania")
        lb.insert(END,"Rhode Island")
        lb.insert(END,"Indiana")
        lb.insert(END,"California")
        lb.insert(END,"New Jersey")
        sb = Scrollbar(self,orient=VERTICAL)
        sb.pack(side=RIGHT,fill=Y)
        sb.configure(command=lb.yview)
        lb.configure(yscrollcommand=sb.set)
        

        def get_state(event):
            index = lb.curselection()[0]
            self.state = lb.get(index)
            temp = candidate(self.state, self.name)
            chance = findResult(temp.linearReg())
            drawGraph(temp.x, temp.y, self.name, self.state, chance)


        button3 = tk.Button(self,text="Select")
        button3.pack(pady = 10)

        button3.bind('<ButtonRelease-1>', get_state)

        button2 = tk.Button(self, text="Back to Party",
                                    command=lambda: controller.show_frame(Republicans))
        button2.pack()

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

app = main()
photo = PhotoImage(file="image.gif") #source: "http://i.huffpost.com/gen/1551535/images/o-REPUBLICAN-VS-DEMOCRAT-facebook.jpg"
label = Label(image=photo)
label.pack()
app.mainloop()