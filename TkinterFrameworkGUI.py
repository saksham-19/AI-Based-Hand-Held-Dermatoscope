from tkinter import *

from tkinter import messagebox

from PIL import Image

from PIL import ImageTk

import datetime

import threading

from imutils.video import WebcamVideoStream

import cv2

import time

import numpy as np

import math

import socket

from os import listdir

from os.path import isfile, join

from functools import reduce


###################

from Google import Create_Service

from googleapiclient.http import MediaFileUpload

#import RPi.GPIO as GPIO

import time

import os



################





# Here, we are creating our class, Window, and inheriting from the Frame

# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)

class Window(Frame):



    # Define settings upon initialization. Here you can specify

    def __init__(self, master=None):

        #print("\ninit_settings");

        self.frame = None

        self.panel = None

        self.vs= None

        self.count_sele=0

        # parameters that you want to send through the Frame class.

        Frame.__init__(self, master)



        #reference to the master widget, which is the tk window

        self.master = master

                

        #loading the required logos

        load = Image.open("video.png")

        load = load.resize((45, 45), Image.ANTIALIAS)

        self.vid_img = ImageTk.PhotoImage(load)

        

        load = Image.open("power.png")

        load = load.resize((45, 45), Image.ANTIALIAS)

        self.power_img = ImageTk.PhotoImage(load)

        

        load = Image.open("cor.png")

        load = load.resize((45, 45), Image.ANTIALIAS)

        self.cor_img = ImageTk.PhotoImage(load)

        

        load = Image.open("wrong.png")

        load = load.resize((45, 45), Image.ANTIALIAS)

        self.wrong_img = ImageTk.PhotoImage(load)

        

        load = Image.open("add_p1.png")

        load = load.resize((50, 50), Image.ANTIALIAS)

        self.add_p_img = ImageTk.PhotoImage(load)

        

        load = Image.open("manual.png")

        load = load.resize((32, 32), Image.ANTIALIAS)

        self.manual_img = ImageTk.PhotoImage(load)

        

        load = Image.open("warning.png")

        load = load.resize((30, 30), Image.ANTIALIAS)

        self.warning_img = ImageTk.PhotoImage(load)

        

        load = Image.open("home.png")

        load = load.resize((55, 60), Image.ANTIALIAS)

        self.home_img = ImageTk.PhotoImage(load)

        

        load = Image.open("camera.png")

        load = load.resize((55, 60), Image.ANTIALIAS)

        self.camera_img = ImageTk.PhotoImage(load)

        

        load = Image.open("spacing.png")

        load = load.resize((474, 146), Image.ANTIALIAS)

        self.spacing_img = ImageTk.PhotoImage(load)

        

                

        #Declaring required variables

        self.eye_video_thread = True

        self.date_time_thread = True

#        self.wifi_thread = True

#        self.wifi_connected = False

        self.thread_number = 0

        self.PatientID_StrVar = StringVar(value='Patient ID: ')

        self.button_pressed = "Home"

        self.last_start = 0

        self.diseases = ["nv", "mel", "bkl", "bcc", "akiec", "vasc", "df"]

        self.entryVar = StringVar(value='')

        self.diag_diseases = ''

        self.custom_diseases = ''

#        self.fps = False



        ###############################

        self.CLIENT_SECRET_FILE = 'client_secret.json'

        self.API_NAME = 'drive'

        self.API_VERSION = 'v3'

        self.SCOPES = ['https://www.googleapis.com/auth/drive']

        self.service = None
        
        self.connect_to_drive()
        
        self.folder_id = '1P3iwaA5Y3nVcmmiY5OVnMTrVlCefZfrJ'

        self.CENTRE=21

        self.UP=26

        self.DOWN=16

        self.LEFT=19

        self.RIGHT=20

        
        #######################################
        
##        GPIO.setmode(GPIO.BCM)
##        
##        
##        
##        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##        
##        GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##        
##        GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##        
##        GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
##        
##        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        self.active_page_buttons = None
        self.active_page_active_button = None

        self.unactive_color = 'LightBlue3'
        self.active_color   = 'LightGray'

        self.up_idx     = 4
        self.down_idx   = 5
        self.left_idx   = 2
        self.right_idx  = 3
        self.centre_idx = 0
        self.button_idx = 1
        self.params_idx = 6
        
##        GPIO.add_event_detect(self.UP    , GPIO.FALLING, callback=lambda x: self.navigation(self.up_idx)   , bouncetime=500)
##        GPIO.add_event_detect(self.DOWN  , GPIO.FALLING, callback=lambda x: self.navigation(self.down_idx) , bouncetime=500)
##        GPIO.add_event_detect(self.LEFT  , GPIO.FALLING, callback=lambda x: self.navigation(self.left_idx) , bouncetime=500)
##        GPIO.add_event_detect(self.RIGHT , GPIO.FALLING, callback=lambda x: self.navigation(self.right_idx), bouncetime=500)
##        GPIO.add_event_detect(self.CENTRE, GPIO.FALLING, callback=lambda x: self.select(1)                 , bouncetime=1500)
##        

        

        #######################################



        #with that, we want to then run init_window, which doesn't yet exist

        self.init_window(-1)

        

    def close_button(self, a):
        self.button_pressed = False
    
    def connect_to_drive(self):
        try:
            self.service = Create_Service(self.CLIENT_SECRET_FILE, self.API_NAME, self.API_VERSION, self.SCOPES)
        except:
            print("cannot connect to drive")
    #PAGES:

    #page_no == 0 Home page

    #page_no == 1 Camera page

    #page_no == 2 Add Patient (Numeric)

    #page_no == 3 Add Patient (Characters)

    def navigation(self, direction_idx):
    
        if self.active_page_active_button != None and self.active_page_buttons[self.active_page_active_button][direction_idx] != -1:
            if self.active_page_buttons[self.active_page_active_button][self.button_idx] != None and self.active_page_buttons[self.active_page_active_button][self.button_idx]["bg"] != 'chartreuse2': 
                self.active_page_buttons[self.active_page_active_button][self.button_idx].configure(bg=self.unactive_color)
                self.active_page_buttons[self.active_page_active_button][self.button_idx].configure(activebackground=self.unactive_color)
                
            self.active_page_active_button = self.active_page_buttons[self.active_page_active_button][direction_idx]
            #print(self.active_page_active_button, self.active_page_buttons[self.active_page_active_button][self.button_idx]["bg"])

            if self.active_page_buttons[self.active_page_active_button][self.button_idx]["bg"] != 'chartreuse2': 
                self.active_page_buttons[self.active_page_active_button][self.button_idx].configure(bg=self.active_color)
                self.active_page_buttons[self.active_page_active_button][self.button_idx].configure(activebackground=self.active_color)

    def select(self, a):
       #print("in select")
       #print(self.count_sele)
        self.count_sele=self.count_sele+1
        if self.active_page_active_button != None:
            #GPIO.remove_event_detect(self.CENTRE)
            if self.active_page_buttons[self.active_page_active_button][self.button_idx] == None:
                pass 
            elif len(self.active_page_buttons[self.active_page_active_button][self.params_idx]) == 0:
                self.active_page_buttons[self.active_page_active_button][self.centre_idx]()
                
            elif len(self.active_page_buttons[self.active_page_active_button][self.params_idx]) == 1:
                x = self.active_page_buttons[self.active_page_active_button][self.params_idx][0]
                self.active_page_buttons[self.active_page_active_button][self.centre_idx](x)
                
            elif len(self.active_page_buttons[self.active_page_active_button][self.params_idx]) == 2:
                x = self.active_page_buttons[self.active_page_active_button][self.params_idx][0]
                y = self.active_page_buttons[self.active_page_active_button][self.params_idx][1]
                self.active_page_buttons[self.active_page_active_button][self.centre_idx](x , y)
            #print("outttt the loop")
          #  time.sleep(1)
            #GPIO.add_event_detect(self.CENTRE, GPIO.FALLING, callback=lambda x: self.select(1)                 , bouncetime=500)
        
        
        
    def init_window(self, page_no):   
        self.active_page_buttons = None
        self.active_page_active_button = None  
        #print("\ninit_window");

        #making date time thread deactive

        self.stop_date_time()

        #print('[INFO] No. of active threads : ', threading.active_count())

        

        #Removing previous page widgets

        self.remove_widgets(page_no)

        time.sleep(0.5)



        # changing the title of our master widget

        self.master.title("GUI")

        

        #packing the frame

        self.pack(fill=BOTH, expand=1)

        
        if page_no == -1:

            self.uploading_message = Label(self, text="Processing. Please wait....", font=('Times New Roman', 22, "bold"),bg="white")
    
            self.uploading_message.place(x=10, y=10, width=460, height=300)
            
            if self.is_connected():
                
                if self.service == None:
                    self.connect_to_drive()
                
                file_names = [f for f in listdir("pictures/")]
                
                mime_types = ['image/jpeg' for names in file_names]
        
                try:
        
                    for file_name, mime_type in zip(file_names, mime_types):
            
                        file_metadata = {
            
                            'name' : file_name,
            
                            'parents': [self.folder_id]
            
                        }
            
                        media = MediaFileUpload('pictures/{0}'.format(file_name), mimetype=mime_type)
            
                        self.service.files().create(
            
                            body = file_metadata,
            
                            media_body=media,
            
                            fields='id'
            
                            ).execute()
            
                        os.remove("pictures/{}".format(file_name))
                except:
                    print("error while uploading")
                    
            time.sleep(5)
            
            self.uploading_message.place_forget()
            
    
        #current page number

        page_no = 0


        #adding date label on frame

        self.date_l = Label(self, text=datetime.datetime.now().strftime('%d/%m/%Y'), font=("Times New Roman", 17, "bold"), bg="white", anchor='w')

#        self.date_l.grid(row=0,column=0,sticky='w', padx=7, pady=7)

        self.date_l.place(x=10, y=5, width=150)



    

        #adding time label on frame

        self.time_l = Label(self, text=datetime.datetime.now().strftime('%H:%M:%S'), font=("Times New Roman", 17, "bold"), bg="white", anchor='e')

#        self.time_l.grid(row=0,column=2,sticky='e', padx=7, pady=7)

        self.time_l.place(x=320, y=5, width=150)



        

        #creating the date time thread

        self.dt_thread = threading.Thread(target=self.date_time)

        



        #Add Patient ID Label on the main window

        self.PID = Label(self, textvariable=self.PatientID_StrVar, font=('Times New Roman', 22, "bold"),bg="white")

#        self.PID.grid(row=1, columnspan=3, sticky='nsew',pady=(0,0))

        self.PID.place(x=10, y=50, width=460)





        

#        self.spacing = Label(self, image=self.spacing_img, bg="white")

#        self.spacing.image = self.spacing_img

#        self.spacing.grid(row=2, column=0,sticky='nsew', columnspan=3, pady=0)

        

        #adding a video button

        self.vid_btn = Button(self, text='Camera',bg='LightGray',activebackground='LightGray',font=("Times New Roman", 17, 'bold'),border='1',command=lambda: self.video_fun(page_no))

        self.vid_btn.config(image=self.vid_img,compound=LEFT)

#        self.vid_btn.grid(row=3,column=0,sticky='nsew', padx=(12, 10), pady=7, ipady = 7)

        self.vid_btn.place(x=11, y=220, width=146, height=90)



               

        #adding a Add Patient button

        self.add_p_btn = Button(self, text='Add \nPatient',image=self.add_p_img, compound=LEFT, bg='LightBlue3',activebackground='LightBlue3', border='1',font=("Times New Roman", 17, 'bold'),command=lambda: self.manual_entry(page_no))

#        self.add_p_btn.grid(row=3,column=1,sticky='nsew', pady=7, ipady = 7)

        self.add_p_btn.place(x=167, y=220, width=146, height=90)



        

        #adding a power button

        self.power_btn = Button(self, text='Power',bg='LightBlue3',activebackground='LightBlue3', border='1',font=("Times New Roman", 17, 'bold'),command=lambda:self.power_fun())

        self.power_btn.config(image=self.power_img,compound=LEFT)

#        self.power_btn.grid(row=3,column=2,sticky='nsew', padx=(10,12), pady=7, ipady = 7)

        self.power_btn.place(x=323, y=220, width=146, height=90)

            

        #making date time thread active

        self.date_time_thread = True

        if self.thread_number not in threading.enumerate():

            self.dt_thread.start()

            self.thread_number = threading.enumerate()[-1]

        self.active_page_buttons = [[lambda x: self.video_fun(x), self.vid_btn, -1, 1, -1, -1, [page_no]],
                                    [lambda x: self.manual_entry(x), self.add_p_btn, 0, 2, -1, -1, [page_no]],
                                    [lambda : self.power_fun(), self.power_btn, 1, -1, -1, -1, []]
                                   ]
        self.active_page_active_button = 0
        

        

        

    def stop_date_time(self):

        #print("\nstop date_time");

        #print('[INFO] No. of active threads : ', threading.active_count())

        #making date time thread deactive

        self.date_time_thread = False

    

    

    def date_time(self):

        #print("\ndate_time");

        #print('[INFO] No. of active threads : ', threading.active_count())

        while self.date_time_thread:

            self.date_l.configure(text=datetime.datetime.now().strftime('%d/%m/%Y'))

            self.time_l.configure(text=datetime.datetime.now().strftime('%H:%M:%S'))

    





    def video_fun(self,page_no):
        
        self.active_page_buttons = None
        self.active_page_active_button = None
        #print("\nvideo window function");

        #print('[INFO] No. of active threads : ', threading.active_count())
        
        

        #making date time thread deactive

        self.stop_date_time()

        

        #removing the init window from the screen

        self.remove_widgets(page_no)

        

        #current page number

        page_no = 1

        

        #Starting the Video thread i.e to start the live stream

        self.eye_video_thread = True

        



        #starting the video stream by using a delay of 0.5 seconds

        if self.vs == None:

            self.vs = WebcamVideoStream(src=0).start()

            time.sleep(0.5)

        

        

        self.thread_lock = threading.Lock()

               

        self.home_btn = Button(self,bg='LightBlue3',activebackground='LightBlue3',height=2, width=12,command=home_fun)

        self.home_btn.config(image=self.home_img,compound=LEFT)

        self.home_btn.place(x=5,y=5, height=152, width=55)

        

        self.start_btn = Button(self,command=None)

        self.start_btn.config(height=2, width=12,bg='LightBlue3',activebackground='LightBlue3', image=self.camera_img,compound=LEFT)

        self.start_btn.place(x=5,y=162, height=153, width=55)

        self.active_page_buttons=[
                    [lambda:self.home_fun(), self.home_btn, -1, -1, -1, 1,[]],
                    [lambda:self.capture(), self.start_btn, -1, -1, 0, -1,[]],
                    [None, None, 1,1,1,1,[]]
                   ]

        self.active_page_active_button = 2

        #creating the video thread

        self.v_thread = threading.Thread(target=self.videoLoop)



        #starting the thread

        self.v_thread.start()





    def home_fun(self):
        self.active_page_buttons = None
        self.active_page_active_button = None
        
        self.button_pressed = "Home"

        self.video_close()



    

    def next_page(self):
        self.active_page_buttons = None
        self.active_page_active_button = None
        self.vs = None
        time.sleep(0.5)
        if self.button_pressed == "Capture":

            self.diagnosis(1)

        

        elif self.button_pressed == "Home":

            self.init_window(1)

        

    

#    'nv': 'Melanocytic nevi',

#    'mel': 'melanoma',

#    'bkl': 'Benign keratosis-like lesions',

#    'bcc': 'Basal cell carcinoma',

#    'akiec': 'Bowen's Disease',

#    'vasc': 'Vascular lesions',

#    'df': 'Dermatofibroma'

    

    def diagnosis(self, page_no):
        self.active_page_buttons = None
        self.active_page_active_button = None
        #Remove previous page widgets

        self.remove_widgets(page_no)



#        current page number

        page_no = 2

        

        self.page_name = Label(self, text="Select Diagnosis", font=("Times New Roman", 20, "bold"), bg="white")

        self.page_name.place(x=10, y=5, width=470, height=40)

        

        self.diagnosis_buttons = {}

        

        self.diagnosis_buttons["nv"] = Button(self, text="Melanocytic\nNevi", bg=self.active_color, activebackground=self.active_color, font=("Times New Roman", 18), command=lambda: self.change_color("nv"))

        self.diagnosis_buttons["nv"].place(x=10,y=50, height=80, width=147)

        

        self.diagnosis_buttons["mel"] = Button(self, text=" Melanoma", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("mel"))

        self.diagnosis_buttons["mel"].place(x=167,y=50, height=80, width=146)

        

        self.diagnosis_buttons["bkl"] = Button(self, text="Benign\nKeratosis-like\nLesions", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("bkl"))

        self.diagnosis_buttons["bkl"].place(x=323,y=50, height=80, width=147)

        

        self.diagnosis_buttons["bcc"] = Button(self, text="Basal Cell\nCarcinoma", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("bcc"))

        self.diagnosis_buttons["bcc"].place(x=10,y=140, height=80, width=147)

        

        self.diagnosis_buttons["akiec"] = Button(self, text="Bowen's\nDisease", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("akiec"))

        self.diagnosis_buttons["akiec"].place(x=167,y=140, height=80, width=146)

        

        self.diagnosis_buttons["vasc"] = Button(self, text="Vascular\nLesions", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("vasc"))

        self.diagnosis_buttons["vasc"].place(x=323,y=140, height=80, width=147)

        

        self.diagnosis_buttons["df"] = Button(self, text="Dermato-\nfibroma", bg='LightBlue3', activebackground='LightBlue3', font=("Times New Roman", 18), command=lambda: self.change_color("df"))

        self.diagnosis_buttons["df"].place(x=10,y=230, height=80, width=147)

        

        self.custom_btn = Button(self, text="Custom\nDiagnosis", bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 18, 'bold'), command=lambda: self.custom_entry(page_no))

        self.custom_btn.place(x=167,y=230, height=80, width=146)

        

        self.back_btn = Button(self, text="Go Back/\nNo Diagnosis", bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 18, 'bold'), command=lambda: self.backFun(page_no))

        self.back_btn.place(x=323,y=230, height=80, width=147)


        self.active_page_buttons=[
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["nv"]   , -1, 1, -1, 3, ["nv"]], 
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["mel"]  , 0, 2, -1, 4, ["mel"]], 
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["bkl"]  , 1, -1, -1, 5, ["bkl"]], 
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["bcc"]  , -1, 4, 0, 6, ["bcc"]],
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["akiec"], 3, 5, 1, 7, ["akiec"]],
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["vasc"] , 4, -1, 2, 8, ["vasc"]], 
                                    [lambda x: self.change_color(x),self.diagnosis_buttons["df"]   , -1, 7, 3, -1, ["df"]], 
                                    [lambda x: self.custom_entry(x),self.custom_btn              , 6, 8, 4, -1,[page_no]], 
                                    [lambda x: self.backFun(x)     ,self.back_btn                , 7, -1, 5, -1,[page_no]]
                                     ]
        self.active_page_active_button = 0
        

        

    def change_color(self, disease):

        if self.diagnosis_buttons[disease]["bg"] == self.active_color:

            self.diagnosis_buttons[disease].config(bg = 'chartreuse2')

            self.diagnosis_buttons[disease].config(activebackground='chartreuse2')

            

        elif self.diagnosis_buttons[disease]["bg"] == 'chartreuse2':

            self.diagnosis_buttons[disease].config(bg = self.active_color)

            self.diagnosis_buttons[disease].config(activebackground=self.active_color)

            



        

    def custom_entry(self, page_no):

#        Remove previous page widgets

        self.remove_widgets(page_no)

        time.sleep(0.5)

#        current page number

        page_no = 3

        

        self.entryVar = StringVar(value='')

        

        self.entryText = Entry(self, textvariable=self.entryVar, font=('Times New Roman', 14), border='3')

        self.entryText.place(x=8,y=8, height=56, width=464)



        self.a_btn = Button(self, text='A', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), width=4, command=lambda:self.charFun('A'))

        self.a_btn.place(x=10,y=67, height=43, width=71)



        self.b_btn = Button(self, text='B', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), width=4, command=lambda:self.charFun('B'))

        self.b_btn.place(x=88,y=67, height=43, width=71)



        self.c_btn = Button(self, text='C', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), width=4, command=lambda:self.charFun('C'))

        self.c_btn.place(x=166,y=67, height=43, width=71)



        self.d_btn = Button(self, text='D', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), width=4, command=lambda:self.charFun('D'))

        self.d_btn.place(x=244,y=67, height=43, width=71)

        

        self.e_btn = Button(self, text='E', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), width=4, command=lambda:self.charFun('E'))

        self.e_btn.place(x=322,y=67, height=43, width=71)

        

        self.f_btn = Button(self, text='F', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('F'))

        self.f_btn.place(x=400,y=67, height=43, width=70)

        

        self.g_btn = Button(self, text='G', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('G'))

        self.g_btn.place(x=10,y=117, height=43, width=71)

        

        self.h_btn = Button(self, text='H', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('H'))

        self.h_btn.place(x=88,y=117, height=43, width=71)

        

        self.i_btn = Button(self, text='I', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('I'))

        self.i_btn.place(x=166,y=117, height=43, width=71)

        

        self.j_btn = Button(self, text='J', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('J'))

        self.j_btn.place(x=244,y=117, height=43, width=71)

        

        self.k_btn = Button(self, text='K', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('K'))

        self.k_btn.place(x=322,y=117, height=43, width=71)

        

        self.l_btn = Button(self, text='L', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('L'))

        self.l_btn.place(x=400,y=117, height=43, width=70)

        

        self.m_btn = Button(self, text='M', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('M'))

        self.m_btn.place(x=10,y=167, height=43, width=71)

        

        self.n_btn = Button(self, text='N', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('N'))

        self.n_btn.place(x=88,y=167, height=43, width=71)

        

        self.o_btn = Button(self, text='O', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('O'))

        self.o_btn.place(x=166,y=167, height=43, width=71)

        

        self.p_btn = Button(self, text='P', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('P'))

        self.p_btn.place(x=244,y=167, height=43, width=71)

        

        self.q_btn = Button(self, text='Q', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('Q'))

        self.q_btn.place(x=322,y=167, height=43, width=71)

        

        self.r_btn = Button(self, text='R', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('R'))

        self.r_btn.place(x=400,y=167, height=43, width=70)

        

        self.s_btn = Button(self, text='S', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('S'))

        self.s_btn.place(x=10,y=217, height=43, width=71)

        

        self.t_btn = Button(self, text='T', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('T'))

        self.t_btn.place(x=88,y=217, height=43, width=71)

        

        self.u_btn = Button(self, text='U', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('U'))

        self.u_btn.place(x=166,y=217, height=43, width=71)

        

        self.v_btn = Button(self, text='V', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('V'))

        self.v_btn.place(x=244,y=217, height=43, width=71)

        

        self.w_btn = Button(self, text='W', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('W'))

        self.w_btn.place(x=322,y=217, height=43, width=71)

        

        self.x_btn = Button(self, text='X', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('X'))

        self.x_btn.place(x=400,y=217, height=43, width=70)

        

        self.y_btn = Button(self, text='Y', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('Y'))

        self.y_btn.place(x=10,y=267, height=43, width=71)

        

        self.z_btn = Button(self, text='Z', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('Z'))

        self.z_btn.place(x=88,y=267, height=43, width=71)

        

        self.sp1_btn = Button(self, text=',', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 35), command=lambda:self.charFun('__'))

        self.sp1_btn.place(x=166,y=267, height=43, width=71)



        self.sp2_btn = Button(self, text='Space', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.charFun('_'))

        self.sp2_btn.place(x=244,y=267, height=43, width=71)

        

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.clearFun_diagnosis())

        self.clear_btn.place(x=322,y=267, height=43, width=71)

        

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 23), command=lambda:self.backFun(page_no))

        self.enter_btn.place(x=400,y=267, height=43, width=70)
        
        
        self.active_page_buttons=[
                                    [lambda x:self.charFun(x),self.a_btn, -1, 1, -1, 6,["a"]],
                                    [lambda x:self.charFun(x),self.b_btn,  0, 2, -1, 7,["b"]], 
                                    [lambda x:self.charFun(x),self.c_btn, 1, 3, -1, 8,["c"]],
                                    [lambda x:self.charFun(x),self.d_btn, 2, 4, -1, 9,["d"]], 
                                    [lambda x:self.charFun(x),self.e_btn, 3, 5, -1, 10,["e"]], 
                                    [lambda x:self.charFun(x),self.f_btn, 4, -1, -1, 11,["f"]], 
                                    [lambda x:self.charFun(x),self.g_btn, -1, 7, 0, 12,["g"]], 
                                    [lambda x:self.charFun(x),self.h_btn, 6, 8, 1, 13,["h"]], 
                                    [lambda x:self.charFun(x),self.i_btn, 7, 9, 2, 14,["i"]], 
                                    [lambda x:self.charFun(x),self.j_btn, 8, 10, 3, 15,["j"]],
                                    [lambda x:self.charFun(x),self.k_btn, 9, 11, 4, 16,["k"]],
                                    [lambda x:self.charFun(x),self.l_btn, 10, -1, 5, 17,["l"]],
                                    [lambda x:self.charFun(x),self.m_btn, -1, 13, 6, 18,["m"]], 
                                    [lambda x:self.charFun(x),self.n_btn,  12, 14, 7, 19,["n"]], 
                                    [lambda x:self.charFun(x),self.o_btn, 13, 15, 8, 20,["o"]], 
                                    [lambda x:self.charFun(x),self.p_btn, 14, 16, 9, 21,["p"]], 
                                    [lambda x:self.charFun(x),self.q_btn, 15, 17, 10, 22,["q"]],
                                    [lambda x:self.charFun(x),self.r_btn, 16, -1, 11, 23,["r"]],
                                    [lambda x:self.charFun(x),self.s_btn, -1, 19, 12, 24,["s"]], 
                                    [lambda x:self.charFun(x),self.t_btn, 18, 20, 13, 25,["t"]], 
                                    [lambda x:self.charFun(x),self.u_btn, 19, 21, 14, 26,["u"]],
                                    [lambda x:self.charFun(x),self.v_btn,  20, 22, 15, 27,["v"]],
                                    [lambda x:self.charFun(x),self.w_btn, 21, 23, 16, 28,["w"]],
                                    [lambda x:self.charFun(x),self.x_btn, 22, -1, 17, 29,["x"]],
                                    [lambda x:self.charFun(x),self.y_btn, -1, 25, 18, -1,["y"]],
                                    [lambda x:self.charFun(x),self.z_btn,  24, 26, 19, -1,["z"]], 
                                    [lambda x:self.charFun(x),self.sp1_btn, 25, 27, 20, -1,["__"]], 
                                    [lambda x:self.charFun(x),self.sp2_btn, 26, 28, 21, -1,["_"]], 
                                    [lambda:self.clearFun_diagnosis(), self.clear_btn, 27, 29, 22, -1,[]],
                                    [lambda x:self.backFun(x) ,self.enter_btn, 28, -1, 23, -1,[page_no]],
                                    [None, None, 0,0,0,0,[]]
                                  ]
        self.active_page_active_button = 30
                                  
    
        
        




    #Function to add number in Custom Diagnosis Field

    def charFun(self, val):

        #print("\nadd number in entry field");

        self.entryVar.set(self.entryVar.get()+str(val))

            

    #Function to clear charachter in Entry Field

    def clearFun_diagnosis(self):

        #print("\nclear entry field");

        txtLen = len(self.entryVar.get())

        if txtLen>0:

            self.entryVar.set(self.entryVar.get()[:txtLen-1])



    

    def is_connected(self, host="8.8.8.8", port=53, timeout=0.8):
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
            
        except socket.error as ex:
            #print(ex)
            return False

    def backFun(self, page_no):
        self.active_page_buttons = None
        self.active_page_active_button = None
        img = self.img

        self.diag_diseases = ''

        self.custom_diseases = ''

        for disease in self.diseases:

            if self.diagnosis_buttons[disease]["bg"] == 'chartreuse2':

                self.diag_diseases += "__" + disease

        

        self.custom_diseases = self.entryVar.get()

        

        date = datetime.datetime.now().strftime('%d-%m-%Y')

        cur_time = datetime.datetime.now().strftime('%H.%M.%S')

        id = self.remove_prefix(self.PatientID_StrVar.get(), 'Patient ID: ')

        

        if self.diag_diseases == '':

            if self.custom_diseases == '':

                imgname = id + "__" + date + "__" + cur_time

            else:

                imgname = id + "__" + date + "__" + cur_time + "__" + self.custom_diseases

                

        else:

            if self.custom_diseases == '':

                imgname = id + "__" + date + "__" + cur_time + self.diag_diseases



            else:

                imgname = id + "__" + date + "__" + cur_time + self.diag_diseases + "__" + self.custom_diseases



        cv2.imwrite("pictures/{}.jpg".format(imgname), img)
        
        if(self.is_connected()):
            if self.service == None:
                self.connect_to_drive()
                
            file_names = ["{}.jpg".format(imgname)]

            mime_types = ['image/jpeg']
            
    
            try:
                for file_name, mime_type in zip(file_names, mime_types):
        
                    file_metadata = {
        
                        'name' : file_name,
        
                        'parents': [self.folder_id]
        
                    }
        
                    media = MediaFileUpload('pictures/{0}'.format(file_name), mimetype=mime_type)
        
                    self.service.files().create(
        
                        body = file_metadata,
        
                        media_body=media,
        
                        fields='id'
        
                        ).execute()
        
                os.remove("pictures/{}.jpg".format(imgname))
            except:
                print("error while uploading")

        

        self.video_fun(page_no)



    def capture(self):

        self.button_pressed = "Capture"

        self.img = self.frame

        self.video_close()

        



    def videoLoop(self):

        #print("\nvideo loop");

        #print('[INFO] No. of active threads : ', threading.active_count())



        #loop until the video thread is on

        while self.eye_video_thread:

            # grab the frame from the video stream and resize it to have a maximum width of 300 pixels

            

            #capturing the frames

            self.frame = self.vs.read()

            #self.fps.update()

            #resizing the frames

            image = cv2.resize(self.frame, (410,310), interpolation=cv2.INTER_AREA)

            

            #converting the image into Tkinter readable image format

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            image = Image.fromarray(image)

            image = ImageTk.PhotoImage(image)

            

            if self.panel is None:

                self.thread_lock.acquire()

                self.panel = Label(image=image)

                self.panel.image = image

                self.panel.place(x=65, y=5, height=310,width=410)



                # otherwise, simply update the panel

            else:

                self.thread_lock.acquire()

                self.panel.configure(image=image)

                self.panel.image = image

            self.thread_lock.release()



            

#            self.set_panel(image)

            

            # if the panel is not None, we need to initialize it

        

        self.vs.stop()

      

        #time.sleep(0.5)

        self.next_page()

#        self.init_window(1)





    def set_panel(self, image):

        if self.panel is None:

            self.thread_lock.acquire()

            self.panel = Label(image=image)

            self.panel.image = image

            self.panel.place(x=65, y=5, height=310,width=410)



            # otherwise, simply update the panel

        else:

            self.thread_lock.acquire()

            self.panel.configure(image=image)

            self.panel.image = image

        self.thread_lock.release()



    

    def remove_prefix(self, text, prefix):

        if text.startswith(prefix):

            return text[len(prefix):]

        return text



    

    

    def video_close(self):

        #print("\nvideo close");

        self.eye_video_thread = False



    

    def power_fun(self):

       #print("\npower off window");

        #print('[INFO] No. of active threads : ', threading.active_count())

        

        #closing the video thread i.e stopping the live stream

        self.video_close()

        

        

        popup = Toplevel()

        popup.resizable(False, False)

        #popup.overrideredirect(1)

        popup.configure(bg='white')

        popup.title("Power Off?")

        popup.geometry('%dx%d+%d+%d' % (280, 120, 100, 120))

        

        label = Label(popup, text="Power Off?", font=("Times New Roman", 20, 'bold'), bg = "white")

        label.place(x=0,y=0, height=50, width=280)

        

        yes_btn = Button(popup, text="Yes",bg='LightBlue3',activebackground='LightGray',command=self.shutdown_fun, font=("Times New Roman", 20, 'bold'))

        yes_btn.config(image=self.cor_img,compound=LEFT)

        yes_btn.place(x=10,y=50, height=60, width=125)



        no_btn = Button(popup, text="No", bg='LightBlue3', activebackground='LightGray', command = popup.destroy, font=("Times New Roman", 20, 'bold'))

        no_btn.config(image=self.wrong_img,compound=LEFT)

        no_btn.place(x=145,y=50, height=60, width=125)

        popup.mainloop()
        
        
        self.active_page_buttons=[
                                   [lambda :self.shutdown_fun(), yes_btn, -1, 1, -1, -1,[]],
                                   [lambda :pop.destroy(), no_btn, 0, -1, -1, -1,[]],
                                   [None, None, 0, 0, 0, 0,[]]
                                 ]
        self.active_page_active_button = 2   
        
         




    def shutdown_fun(self):

        #print("\nshut down");

        os.system("sudo shutdown -h now")

        #exit()

        

    def remove_widgets(self, page_no):

        

        if page_no == -1:
            
            return

            

        elif page_no == 0:

            self.power_btn.place_forget()

            self.add_p_btn.place_forget()

            self.vid_btn.place_forget()

            self.PID.place_forget()

            self.time_l.place_forget()

            self.date_l.place_forget()

        

        elif page_no == 1:
            
            self.panel.place_forget()

            self.panel = None

            self.start_btn.place_forget()

            self.home_btn.place_forget()

            

        elif page_no == 2:

            self.back_btn.place_forget()

            self.custom_btn.place_forget()

            

            for disease in reversed(self.diseases):

                self.diagnosis_buttons[disease].place_forget()

            

            self.page_name.place_forget()

            

        elif page_no == 3:

            self.enter_btn.place_forget()

            self.clear_btn.place_forget()

            self.sp2_btn.place_forget()

            self.sp1_btn.place_forget()

            self.z_btn.place_forget()

            self.y_btn.place_forget()

            self.x_btn.place_forget()

            self.w_btn.place_forget()

            self.v_btn.place_forget()

            self.u_btn.place_forget()

            self.t_btn.place_forget()

            self.s_btn.place_forget()

            self.r_btn.place_forget()

            self.q_btn.place_forget()

            self.p_btn.place_forget()

            self.o_btn.place_forget()

            self.n_btn.place_forget()

            self.m_btn.place_forget()

            self.l_btn.place_forget()

            self.k_btn.place_forget()

            self.j_btn.place_forget()

            self.i_btn.place_forget()

            self.h_btn.place_forget()

            self.g_btn.place_forget()

            self.f_btn.place_forget()

            self.e_btn.place_forget()

            self.d_btn.place_forget()

            self.c_btn.place_forget()

            self.b_btn.place_forget()

            self.a_btn.place_forget()

            self.entryText.place_forget()

            

        elif page_no == 4:

            self.enter_btn.place_forget()

            self.zero_btn.place_forget()

            self.clear_btn.place_forget()

            self.nine_btn.place_forget()

            self.eight_btn.place_forget()

            self.seven_btn.place_forget()

            self.six_btn.place_forget()

            self.five_btn.place_forget()

            self.four_btn.place_forget()

            self.three_btn.place_forget()

            self.two_btn.place_forget()

            self.one_btn.place_forget()

            self.shift_btn.place_forget()

            self.entryText.place_forget()

            

        elif page_no == 5:

            self.enter_btn.place_forget()

            self.clear_btn.place_forget()

            self.z_btn.place_forget()

            self.y_btn.place_forget()

            self.x_btn.place_forget()

            self.w_btn.place_forget()

            self.v_btn.place_forget()

            self.u_btn.place_forget()

            self.t_btn.place_forget()

            self.s_btn.place_forget()

            self.r_btn.place_forget()

            self.q_btn.place_forget()

            self.p_btn.place_forget()

            self.o_btn.place_forget()

            self.n_btn.place_forget()

            self.m_btn.place_forget()

            self.l_btn.place_forget()

            self.k_btn.place_forget()

            self.j_btn.place_forget()

            self.i_btn.place_forget()

            self.h_btn.place_forget()

            self.g_btn.place_forget()

            self.f_btn.place_forget()

            self.e_btn.place_forget()

            self.d_btn.place_forget()

            self.c_btn.place_forget()

            self.b_btn.place_forget()

            self.a_btn.place_forget()

            self.shift_btn.place_forget()

            self.entryText.place_forget()

    

        

    def manual_entry(self, page_no):
    
        #Stop previous page processes

        if page_no == 0:

            self.stop_date_time()

                

        #Remove previous page widgets

        self.remove_widgets(page_no)

        time.sleep(0.5)

        

        self.PatientID_StrVar = StringVar(value='Patient ID: ')

        

        if page_no != 5:

            self.txtVar = StringVar(value='ID : ')

            

        #current page number

        page_no = 4

                

        self.entryText = Entry(self, textvariable=self.txtVar, font=('Times New Roman', 20), border='3', width=27)

        self.entryText.place(x=8,y=8, height=56, width=307)

        

        self.shift_btn = Button(self, text='ABC', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.shiftFun(page_no))

        self.shift_btn.place(x=323,y=10, height=52, width=147)

        

        self.one_btn = Button(self, text='1', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(1))

        self.one_btn.place(x=10,y=72, height=52, width=147)



        self.two_btn = Button(self, text='2', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(2))

        self.two_btn.place(x=167,y=72, height=52, width=146)



        self.three_btn = Button(self, text='3', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(3))

        self.three_btn.place(x=323,y=72, height=52, width=147)



        self.four_btn = Button(self, text='4', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(4))

        self.four_btn.place(x=10,y=134, height=52, width=147)



        self.five_btn = Button(self, text='5', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(5))

        self.five_btn.place(x=167,y=134, height=52, width=146)



        self.six_btn = Button(self, text='6', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(6))

        self.six_btn.place(x=323,y=134, height=52, width=147)



        self.seven_btn = Button(self, text='7', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(7))

        self.seven_btn.place(x=10,y=196, height=52, width=147)



        self.eight_btn = Button(self, text='8', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(8))

        self.eight_btn.place(x=167,y=196, height=52, width=146)



        self.nine_btn = Button(self, text='9', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(9))

        self.nine_btn.place(x=323,y=196, height=52, width=147)



        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.clearFun())

        self.clear_btn.place(x=10,y=258, height=52, width=147)



        self.zero_btn = Button(self, text='0', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun(0))

        self.zero_btn.place(x=167,y=258, height=52, width=146)



        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.enterFun(page_no))

        self.enter_btn.place(x=323,y=258, height=52, width=147)

        
        
        self.active_page_buttons=[
                                   [lambda x:self.numFun(x), self.one_btn, -1, 1, -1, 3,[1]],
                                   [lambda x:self.numFun(x), self.two_btn, 0, 2, -1, 4,[2]],
                                   [lambda x:self.numFun(x), self.three_btn, 1, -1, 12, 5,[3]], 
                                   [lambda x:self.numFun(x), self.four_btn, -1, 4, 0, 6,[4]],
                                   [lambda x:self.numFun(x), self.five_btn, 3, 5, 1, 7,[5]],
                                   [lambda x:self.numFun(x), self.six_btn, 4, -1, 2, 8,[6]],
                                   [lambda x:self.numFun(x), self.seven_btn, -1, 7, 3, 9,[7]],
                                   [lambda x:self.numFun(x), self.eight_btn, 6, 8, 4, 10,[8]],
                                   [lambda x:self.numFun(x), self.nine_btn, 7, -1, 5, 11,[9]],
                                   [lambda :self.clearFun(), self.clear_btn, -1, 10, 6, -1,[]],
                                   [lambda x:self.numFun(x), self.zero_btn, 9, 11, 7, -1,[0]], 
                                   [lambda x:self.enterFun(x), self.enter_btn, 10, -1, 8, -1,[page_no]], 
                                   [lambda x:self.shiftFun(x), self.shift_btn, -1, -1, -1, 2,[page_no]],
                                   [None, None, 0,0,0,0,[]]
                                  ]
        self.active_page_active_button = 13

            

    #Function to add number in Entry Field

    def numFun(self, val):

        #print("\nadd number in entry field");

        self.txtVar.set(self.txtVar.get()+str(val))

        

    #Function to clear charachter in Entry Field

    def clearFun(self):

        #print("\nclear entry field");

        txtLen = len(self.txtVar.get())

        if txtLen>5:

            self.txtVar.set(self.txtVar.get()[:txtLen-1])

    

    def shiftFun(self, page_no):

        #print("\nshiftfun");

        

        #Removing previous page widgets

        self.remove_widgets(page_no)

        time.sleep(0.5)



        #current page number

        page_no = 5



        self.entryText.place(x=8,y=8, height=56, width=307)



        self.shift_btn = Button(self, text='123', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.manual_entry(page_no))

        self.shift_btn.place(x=323,y=10, height=52, width=147)



        self.a_btn = Button(self, text='A', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), width=4, command=lambda:self.numFun('A'))

        self.a_btn.place(x=10,y=67, height=43, width=71)



        self.b_btn = Button(self, text='B', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), width=4, command=lambda:self.numFun('B'))

        self.b_btn.place(x=88,y=67, height=43, width=71)



        self.c_btn = Button(self, text='C', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), width=4, command=lambda:self.numFun('C'))

        self.c_btn.place(x=166,y=67, height=43, width=71)



        self.d_btn = Button(self, text='D', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), width=4, command=lambda:self.numFun('D'))

        self.d_btn.place(x=244,y=67, height=43, width=71)

        

        self.e_btn = Button(self, text='E', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), width=4, command=lambda:self.numFun('E'))

        self.e_btn.place(x=322,y=67, height=43, width=71)

        

        self.f_btn = Button(self, text='F', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('F'))

        self.f_btn.place(x=400,y=67, height=43, width=70)

        

        self.g_btn = Button(self, text='G', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('G'))

        self.g_btn.place(x=10,y=117, height=43, width=71)

        

        self.h_btn = Button(self, text='H', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('H'))

        self.h_btn.place(x=88,y=117, height=43, width=71)

        

        self.i_btn = Button(self, text='I', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('I'))

        self.i_btn.place(x=166,y=117, height=43, width=71)

        

        self.j_btn = Button(self, text='J', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('J'))

        self.j_btn.place(x=244,y=117, height=43, width=71)

        

        self.k_btn = Button(self, text='K', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('K'))

        self.k_btn.place(x=322,y=117, height=43, width=71)

        

        self.l_btn = Button(self, text='L', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('L'))

        self.l_btn.place(x=400,y=117, height=43, width=70)

        

        self.m_btn = Button(self, text='M', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('M'))

        self.m_btn.place(x=10,y=167, height=43, width=71)

        

        self.n_btn = Button(self, text='N', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('N'))

        self.n_btn.place(x=88,y=167, height=43, width=71)

        

        self.o_btn = Button(self, text='O', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('O'))

        self.o_btn.place(x=166,y=167, height=43, width=71)

        

        self.p_btn = Button(self, text='P', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('P'))

        self.p_btn.place(x=244,y=167, height=43, width=71)

        

        self.q_btn = Button(self, text='Q', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('Q'))

        self.q_btn.place(x=322,y=167, height=43, width=71)

        

        self.r_btn = Button(self, text='R', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('R'))

        self.r_btn.place(x=400,y=167, height=43, width=70)

        

        self.s_btn = Button(self, text='S', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('S'))

        self.s_btn.place(x=10,y=217, height=43, width=71)

        

        self.t_btn = Button(self, text='T', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('T'))

        self.t_btn.place(x=88,y=217, height=43, width=71)

        

        self.u_btn = Button(self, text='U', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('U'))

        self.u_btn.place(x=166,y=217, height=43, width=71)

        

        self.v_btn = Button(self, text='V', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('V'))

        self.v_btn.place(x=244,y=217, height=43, width=71)

        

        self.w_btn = Button(self, text='W', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('W'))

        self.w_btn.place(x=322,y=217, height=43, width=71)

        

        self.x_btn = Button(self, text='X', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('X'))

        self.x_btn.place(x=400,y=217, height=43, width=70)

        

        self.y_btn = Button(self, text='Y', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('Y'))

        self.y_btn.place(x=10,y=267, height=43, width=71)

        

        self.z_btn = Button(self, text='Z', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.numFun('Z'))

        self.z_btn.place(x=88,y=267, height=43, width=71)

        

        self.clear_btn = Button(self, text='Clear', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.clearFun())

        self.clear_btn.place(x=166,y=267, height=43, width=149)

        

        self.enter_btn = Button(self, text='Enter', bg='LightBlue3', activebackground='LightGray', font=("Times New Roman", 25), command=lambda:self.enterFun(page_no))

        self.enter_btn.place(x=322,y=267, height=43, width=148)

        self.active_page_buttons=[
                                    [lambda x:self.numFun(x),self.a_btn, -1, 1, -1, 6,["a"]],
                                    [lambda x:self.numFun(x),self.b_btn,  0, 2, -1, 7,["b"]], 
                                    [lambda x:self.numFun(x),self.c_btn, 1, 3, -1, 8,["c"]],
                                    [lambda x:self.numFun(x),self.d_btn, 2, 4, -1, 9,["d"]], 
                                    [lambda x:self.numFun(x),self.e_btn, 3, 5, 30, 10,["e"]], 
                                    [lambda x:self.numFun(x),self.f_btn, 4, -1, 30, 11,["f"]], 
                                    [lambda x:self.numFun(x),self.g_btn, -1, 7, 0, 12,["g"]], 
                                    [lambda x:self.numFun(x),self.h_btn,6, 8, 1, 13,["h"]], 
                                    [lambda x:self.numFun(x),self.i_btn,7, 9, 2, 14,["i"]], 
                                    [lambda x:self.numFun(x),self.j_btn,8, 10, 3, 15,["j"]],
                                    [lambda x:self.numFun(x),self.k_btn, 9, 11, 4, 16,["k"]],
                                    [lambda x:self.numFun(x),self.l_btn, 10, -1, 5, 17,["l"]],
                                    [lambda x:self.numFun(x),self.m_btn,-1, 13, 6, 18,["m"]], 
                                    [lambda x:self.numFun(x),self.n_btn,  12, 14, 7, 19,["n"]], 
                                    [lambda x:self.numFun(x),self.o_btn,13, 15, 8, 20,["o"]], 
                                    [lambda x:self.numFun(x),self.p_btn, 14, 16, 9, 21,["p"]], 
                                    [lambda x:self.numFun(x),self.q_btn,15, 17, 10, 22,["q"]],
                                    [lambda x:self.numFun(x),self.r_btn, 16, -1, 11, 23,["r"]],
                                    [lambda x:self.numFun(x),self.s_btn, -1, 19, 12, 24,["s"]], 
                                    [lambda x:self.numFun(x),self.t_btn,  18, 20, 13, 25,["t"]], 
                                    [lambda x:self.numFun(x),self.u_btn, 19, 21, 14, 26,["u"]],
                                    [lambda x:self.numFun(x),self.v_btn, 20, 22, 15, 27,["v"]],
                                    [lambda x:self.numFun(x),self.w_btn, 21, 23, 16, 28,["w"]],
                                    [lambda x:self.numFun(x),self.x_btn,22, -1, 17, 29,["x"]],
                                    [lambda x:self.numFun(x),self.y_btn, -1, 25, 18, -1,["y"]],
                                    [lambda x:self.numFun(x),self.z_btn, 24, 26, 19, -1,["z"]], 
                                    [lambda :self.clearFun(), self.clear_btn, 25, 28, 20, -1,[]],
                                    [lambda :self.clearFun(), self.clear_btn, 25, 28, 21, -1,[]],
                                    [lambda x:self.enterFun(x), self.enter_btn, 27, -1, 22, -1,[page_no]], 
                                    [lambda x:self.enterFun(x), self.enter_btn, 27, -1, 23, -1,[page_no]], 
                                    [lambda x:self.manual_entry(x), self.shift_btn, -1, -1, -1, 4,[page_no]],
                                    [None, None, 0, 0, 0, 0, []]
                                  ]
        self.active_page_active_button = 31



    #Function to Store the Patient ID:

    def enterFun(self, page_no):

        #print("\nenterfun");

        self.PatientID_StrVar.set(self.PatientID_StrVar.get()+self.txtVar.get()[5:])

        self.init_window(page_no)



# root window created. Here, that would be the only window, but

# you can later have windows within windows.



def main():

    #print("\nmain");

    root = Tk()

    root.geometry('%dx%d+%d+%d' % (480, 320, 0, -30))

    root.resizable(False, False)

    

#    root.grid_columnconfigure(3, minsize=100)

#    root.grid_rowconfigure(4, minsize=500)



    #creation of an instance

    app = Window(root)

    app.configure(background="white")

    #mainloop

    

    root.mainloop()



if __name__ == '__main__':

    main()

    

