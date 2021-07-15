import tkinter
from tkinter.constants import ANCHOR
import cv2  #pip install opencv-python
import PIL.Image, PIL.ImageTk  #pip install pillow
from functools import partial
import time
import threading # allow program to excuate without thread
import imutils # module for resize the image

#Globally Define Items
SET_WIDTH=650
SET_HEIGHT=368

stream=cv2.VideoCapture("veidoclips/virat_kholi.mp4")
flag=True

def play(speed):
    global flag
    print(f"You are click on Play.Speed is {speed}")
    # play video in reverse
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)
    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame,ancho=tkinter.NW)
    if flag:
        canvas.create_text(120,25,fill='black',font=" Times 25 bold",text="Decision Pending")
    flag = not flag



def pending(decision):
    # display decision pending
    frame = cv2.cvtColor(cv2.imread("decisionpending.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0, image= frame,ancho=tkinter.NW)
    
    # wait 2 second
    time.sleep(2)

    # display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponsor.png"),cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image= frame,ancho=tkinter.NW)
    
    # wait 2.5 second
    time.sleep(2.5)
    # display decision not out or out
    if decision=='out':
        decisionImage="out.png"
    else:
        decisionImage="not_out.png"

    frame = cv2.cvtColor(cv2.imread(decisionImage), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,image= frame,ancho=tkinter.NW)
    exit()
    
    

def out():
    thread=threading.Thread(target=pending,args=("out",))
    thread.daemon=1
    thread.start()
    print("Player is out")
  


def not_out():
    thread=threading.Thread(target=pending,args=("not out",))
    thread.daemon=1
    thread.start()
    print("Player is not out")
     


#Tkinter gui start here
window=tkinter.Tk()
cv_image=cv2.cvtColor(cv2.imread("welcome.png"),cv2.COLOR_BGR2RGB)
window.title("Third Umpire Decison Review Program")
canvas=tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_image))
image_on_canvas = canvas.create_image(0,0,ancho=tkinter.NW, image= photo)
canvas.pack()

#buttons of tkinter gui
btn=tkinter.Button(window,text="<< Previous (Fast)",width=50,command = partial(play,-25))
btn.pack()

btn=tkinter.Button(window,text="<< Previous (Slow)",width=50,command = partial(play,-2))
btn.pack()

btn=tkinter.Button(window,text="Next (Slow) >>",width=50,command = partial(play,2))
btn.pack()

btn=tkinter.Button(window,text="Next (Fast) >>", width=50 , command = partial(play,25))
btn.pack()

btn=tkinter.Button(window,text="Out",width=50,command=out)
btn.pack()

btn=tkinter.Button(window,text="Not-Out",width=50,command=not_out)
btn.pack()


window.mainloop()