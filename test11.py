from tkinter import *
from tkinter.filedialog import*
import io
import tokenize as tn
import pygame
import requests
from mutagen.mp3 import MP3


time = list()
words = list()
Z1 = list()




def main():
    root = Tk()
    root.title("My reading book")
    root.maxsize(width=600,height=600)
    S = Scrollbar(root)
    S.pack(side=RIGHT,fill=Y)
    text1 = Text(root, width = 400, height = 400)
    text1.pack(side=LEFT,fill=Y)
    S.config(command=text1.yview)
    text1.config(yscrollcommand=S.set)
       

    def ttsIt(tokenL,savefile='_gtts.mp3',lang='en'):#upload the txt file to google and get the byte's of the each words in the txt file from google
        GOOGLE_TTS_URL='http://translate.google.com/translate_tts'
        textL = [t.string for t in tokenL if t.type==tn.NAME]
        textlangL = []
        for text in textL:
            lang = 'en'
            textlangL+=[(text,lang)]
        f = open(savefile,'wb')
        for idx,textlang in enumerate(textlangL):

            text,lang=textlang

            payload = { 'ie':'utf8',
                        'tl':lang,
                        'q':text,
                        'total':len(textlangL),
                        'idx':idx,
                        'textlen':len(text)}
            try:
                r=requests.get(GOOGLE_TTS_URL,params=payload)
                byteNum = len(r.content)
                f.write(r.content)
                time.append(byteNum)
        
            except Exception as e:
                raise
        f.close()
        return time
           
    def textshowdata():#use time and words to create the showtext data
        accT = 0
        for i in range(0,len(time)):
            z = (words[i],time[i],accT,accT+time[i],'1.0','1.0')
            accT+=time[i]
            Z1.append(z)
        
    def Init():
        pygame.mixer.pre_init(frequency= 16000, channels=1, size=-16)
        pygame.mixer.init()
        pygame.mixer.music.load('_gtts.mp3')
        
    def open_File(): #open the txt file and get the each words in the txt file
        f = askopenfile(mode='r')
        global article
        article = f.read()
        text1.delete(1.0,END)
        text1.insert(1.0,article)
        word = article.split()
        for i in word:
            words.append(i)
      
        fp = io.StringIO(article)
        tokenL=[x for x in tn.generate_tokens(fp.readline)]
        ttsIt(tokenL)
        textshowdata()
        Init()
        f.close()
    def sync():
        text1.delete(1.0,END)
        text1.tag_configure('highlight',background='yellow')
        text1.insert('insert',article)
        Z2 = list()            
        idx2 = '1.0'
        for n,z in enumerate(Z1):
            text = z[0]
            idx1 = text1.search(text,idx2)
            idx2 = idx1 + ' + %d chars'%len(text)
            idx3 = text1.index(idx2)
            z1 = (z[0],z[1],z[2],z[3],idx1,idx3)
            Z2.append(z1)
            print(idx1,idx2,idx3)
        pygame.mixer.music.play()
        n = 0
        tmpBool = True
        pos = pygame.mixer.music.get_pos()
        while pos!=-1:
            pos = pygame.mixer.music.get_pos()
            audio = MP3("_gtts.mp3")
            Length = audio.info.length*1000
            sumT = sum(time)
            iPos = int(pos/Length*sumT)

            if n<len(Z2):
                if iPos>=Z2[n][2]-500 and iPos<=Z2[n][3]-500 and tmpBool==True:
                    
                    if n>=1:
                        text1.tag_remove('highlight',Z2[n-1][4],Z2[n-1][5])
                    text1.tag_add('highlight',Z2[n][4],Z2[n][5])   
                    text1.see(Z2[n][5])
                    text1.update()

                    tmpBool = False
                elif iPos >= Z2[n][3]:
                    n+=1
                    tmpBool= True
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        
       
       
        
 
    menubar = Menu(root)
    filemenu = Menu(menubar)
    filemenu.add_command(label="Open",command = open_File)
    filemenu.add_command(label="Read load",command = sync)
    filemenu.add_command(label="Quit",command = root.quit)
    menubar.add_cascade(label="File",menu=filemenu)
    root.config(menu=menubar)
   
main()
