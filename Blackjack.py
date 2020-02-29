import time
import random
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("BlackJack")

canvas = tk.Canvas(root,height = 700,width = 800)
canvas.pack()

balance = 0 

values = {'2': 2 , '3' : 3 , '4' : 4 , '5' : 5 , '6' : 6 , '7' : 7 , '8' : 8 , '9' : 9 , '10' : 10 , 'J' : 10 , 'Q' : 10 , 'K' : 10 , 'A' : 11}


class Cards():  
    cs = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    def __init__(self,suit):
        self.suit = suit 






            
            
class Deck():
    l=[]
    def __init__(self):
        suits = [Cards('Hearts'),Cards('Diamond'),Cards('Spades'),Cards('Clubs')]
        for k in range(0,4):
            for j in range(0,13):
                self.l.append((suits[k].suit,suits[k].cs[j]))
        self.ShuffleDeck()

    def Deal(self):
        return self.l.pop()
    
    def ShuffleDeck(self):
        random.shuffle(self.l)
        

def thankyou(gameframe):
    tyframe = tk.Frame(gameframe, bg = 'black')
    tyframe.place(relwidth = 1, relheight = 1)
    tylabel = tk.Label(tyframe,fg = 'gray',text="THANK YOU\nFOR PLAYING",height = 300,width = 1500,bg = 'black',anchor = 'center')
    tylabel.config(font = ('courier',45,'bold'))
    tylabel.place(relx = 0.1,rely = 0.1,relwidth = 0.8,relheight = 0.4)
    tybutton = tk.Button(tyframe, text="EXIT" , activeforeground = 'red' , fg = 'red' , bg = 'gray',height = 3,width = 20, command = root.destroy)
    tybutton.config(font = ('times',15,'bold'))
    tybutton.place(relx = 0.4,rely = 0.7,relwidth = 0.2 , relheight = 0.1)

def game(p1,d1,deck,root):
    gameframe = tk.Frame(root, bg = 'green' )
    gameframe.place(relwidth = 1 ,relheight = 1)
    dlabel = tk.Label(gameframe , text = "Dealer's Hand:" , bg = 'green' , fg = 'white' )
    dlabel.config(font = ('courier', 15,'bold'))
    dlabel.place(relwidth = 0.3 , relheight = 0.1)
    cardfont = ('courier' , 15 , 'bold')
    dclabel = tk.Label(gameframe , text = str(d1.cards[0]) + " , <UNKNOWN>" , bg = 'green' , fg = 'white')
    dclabel.config(font = cardfont)
    dclabel.place(relx = 0.1, rely = 0.25)
    plabel = tk.Label(gameframe , text = "Player's Hand:" , bg = 'green' , fg = 'white')
    plabel.config(font = ('courier', 15, 'bold'))
    plabel.place(rely = 0.4, relwidth = 0.3 , relheight = 0.1)
    p1.printHands(gameframe,d1,deck,root)

    
    
def checkBet(p1,d1,deck,bet,root,betframe):
    global balance
    if bet > balance:
        if not tk.messagebox.askretrycancel("Error!",'Cannot place your bet , as the bet exceeds the balance!'):
            thankyou(root)
    elif bet < 50:
        if not tk.messagebox.askretrycancel('Error!','Minimum Bet is 50'):
            thankyou(betframe)
    else:
        p1.bet = bet
        balance -= p1.bet
        game(p1,d1,deck,root)
    
def placeBet(root,p1,d1,deck):
    betframe = tk.Frame(root, bg = 'gray', bd = 5 , relief = 'groove')
    betframe.place(relwidth = 1.0 , relheight = 1.0)
    bfont = ('times',30, 'bold')
    blabel1 = tk.Label(betframe, text = 'Place your Bet:',bg = 'gray' , fg = 'black')
    blabel1.config(font = bfont)
    blabel1.pack(side = 'top')
    bentry = tk.Entry(betframe , font = bfont ,justify = 'center', bg = 'black' , fg = 'white'  , relief = 'sunken')
    bentry.place(relx = 0.35,rely = 0.2 , relwidth = 0.3 , relheight = 0.1)
    bsubmit = tk.Button(betframe , text = 'SUBMIT' , fg = 'red' ,font = 30, height = 3 , width = 300 , bg ='black' , relief = 'raised' , activeforeground = 'red', command = lambda : checkBet(p1,d1,deck,int(bentry.get()),root,betframe))
    bsubmit.pack(side = 'bottom')

class Player():
    import tkinter
    def __init__(self,deck,d1,root,tk):
        self.cards = []
        self.deck = deck
        self.aces = 0
        for i in range (0,2):
            self.cards.append(deck.Deal())
            
        for card in self.cards:
            if card[1] == 'A':
                self.aces += 1
        self.score = self.handValue()
        self.tk = tk
        self.bet = placeBet(root,self,d1,deck)
    
    def handValue(self):
        val = 0
        for card in self.cards:
            val += int(values[card[1]])
        self.aceCase(val)
        return val

    def Hit(self,gameframe,x,deck,root):
        self.cards.append(deck.Deal())
        if self.cards[-1][1] == 'A':
            self.aces += 1
        self.score = self.handValue()
        self.printHands(gameframe,x,deck,root)
    
    def aceCase(self,val):
        if val > 21 and self.aces > 0:
            val -= 10
            self.aces -= 1
        return val    
    
    def pWins(self,gameframe,d1,root):
        global balance
        balance += 2 * self.bet
        if tk.messagebox.askyesno("Hand Result","Player Wins this hand.\nPlayer Balance : {}\nDo you want to play again?".format(balance)):
            create_player(root,tk)
        else:
            thankyou(gameframe)
            
    def pBusts(self,gameframe,d1,root):
        global balance
        if tk.messagebox.askyesno("Hand Result","Player Busts.\nDealer wins this hand.\nPlayer Balance : {}\nDo you want to play again?".format(balance)):
            create_player(root,tk)
        else:
            thankyou(gameframe)
            
    def dWins(self,gameframe,d1,root):
        global balance
        if tk.messagebox.askyesno("Hand Result","Dealer wins this hand.\nPlayer Balance : {}\nDo you want to play again?".format(balance)):
            create_player(root,tk)
        else:
            thankyou(gameframe)
            
    def dBusts(self,gameframe,d1,root):
        global balance
        balance += 2 * self.bet
        if tk.messagebox.askyesno("Hand Result","Dealer Busts.\nPlayer wins this hand.\nPlayer Balance : {}\nDo you want to play again?".format(balance)):
            create_player(root,tk)
        else:
            thankyou(gameframe)
            
    def push(self,gameframe,d1,root):
        global balance
        balance += self.bet
        if tk.messagebox.askyesno("Hand Result","This hand was tied\nPlayer Balance : {}\nDo you want to play again?".format(balance)):
            create_player(root,tk)
        else:
            thankyou(gameframe)
            
    def printHands(self,gameframe,d1,deck,root):
        cardfont = ('courier' , 15 , 'bold')
        pclabel = self.tk.Label(gameframe, text = str(self.cards) , bg = 'green' , fg = 'white')
        pclabel.config(font = cardfont) 
        pclabel.place(relx  = 0.1 ,rely = 0.55)
        if self.score == 21 and d1.score != 21:
            self.pWins(gameframe,d1,root)
        elif self.score == 21 and d1.score == 21:
            d1.printHands(gameframe,self,deck,root)
        elif self.score > 21:
            self.pBusts(gameframe,d1,root)
        pbutton1 = self.tk.Button(gameframe, text = 'HIT' , bg = 'white' , fg = 'green' , font = 30 , relief = 'raised' , command = lambda : self.Hit(gameframe,d1,deck,root))
        pbutton1.place(relx = 0.1 , rely = 0.8,relwidth = 0.2 , relheight=0.1)
        pbutton2 = self.tk.Button(gameframe, text = 'STAY' , bg = 'white' , fg = 'green' , font = 30 , relief = 'raised' , command = lambda : d1.printHands(gameframe,self,deck,root))
        pbutton2.place(relx = 0.4 , rely = 0.8,relwidth = 0.2 , relheight=0.1)





class Dealer():
    def __init__(self,deck,root,tk):
        self.cards = []
        self.aces = 0
        for i in range (0,2):
            self.cards.append(deck.Deal())
            self.score = self.handValue()
            
        for card in self.cards:
            if card[1] == 'A':
                self.aces += 1
        self.score = self.handValue()
        self.tk = tk
        
    def handValue(self):
        val = 0
        for card in self.cards:
            val += int(values[card[1]])
        self.aceCase(val)
        return val

    def Hit(self,gameframe,x,deck,root):
        self.cards.append(deck.Deal())
        if self.cards[-1][1] == 'A':
            self.aces += 1
        self.score = self.handValue()
        self.printHands(gameframe,x,deck,root)
    
    def aceCase(self,val):
        if val > 21 and self.aces > 0:
            val -= 10
            self.aces -= 1
        return val    
    
    
    def printHands(self,gameframe,p1,deck,root):
        cardfont = ('courier' , 15 , 'bold')
        dclabel = self.tk.Label(gameframe, text = str(self.cards) , bg = 'green' , fg = 'white')
        dclabel.config(font = cardfont) 
        dclabel.place(relx = 0.1 , rely=0.25)
        if self.score == 21 and p1.score == 21:
            p1.push(gameframe,self,root)
        elif self.score < 21 and self.score < p1.score :
            self.Hit(gameframe,p1,deck,root)
        elif self.score > p1.score and self.score <= 21:
            p1.dWins(gameframe,self,root)
        elif self.score == 21:
            p1.dWins(gameframe,self,root)
        else:
            p1.dBusts(gameframe,self,root)

    
def create_player(root,tk):
    deck  = Deck()
    d1 = Dealer(deck,root,tk)
    p1 = Player(deck,d1,root,tk)
    
    
def get_balance(root,bal,tk,frame):
    global balance 
    if bal < 500:
        if not tk.messagebox.askretrycancel("Error!",'Cannot accept value less than 500 $'):
            thankyou(frame)
    else:
        balance = bal
        create_player(root,tk)

def play(root,tk):
    frame =  tk.Frame(root, bg = 'gray', bd = 4 , relief = 'groove')
    frame.place(relwidth = 1 , relheight = 1)
    font = ('times' , 30 , 'bold')
    blabel1 = tk.Label(frame, text = 'Please Enter your Bank Balance:',bg = 'gray' , fg = 'black')
    blabel1.config(font = font)
    blabel1.pack(side = 'top')
    blabel2 = tk.Label(frame, text = '(minimum should 500$)' , bg = 'gray' , fg = 'black')
    blabel2.config(font = ('times',20,'bold'))
    blabel2.pack(side = 'top')
    bentry = tk.Entry(frame, font =font ,bg = 'black' , justify = 'center' , fg = 'white'  , relief = 'sunken')
    bentry.place(relx = 0.35,rely = 0.2 , relwidth = 0.3 , relheight = 0.1)
    bsubmit = tk.Button(frame , text = 'SUBMIT' , fg = 'red' ,font = 30, height = 3 , width = 300 , bg ='black' , relief = 'raised' , activeforeground = 'red' , command = lambda : get_balance(root,int(bentry.get()),tk,frame))
    bsubmit.pack(side = 'bottom')


def welcome(root,tk):
    frame = tk.Frame(root,bg = 'gray',bd = 5,relief = 'groove')
    frame.place(relwidth = 1.0 , relheight = 1.0)

    welcomefont = ('courier',45,'bold')
    welcome1 = tk.Label(frame,fg = 'white',text="WELCOME TO",height = 300,width = 1500,bg = 'gray',anchor = 'center')
    welcome1.config(font = welcomefont)
    welcome1.place(relx = 0.1,rely = 0.1,relwidth = 0.8,relheight = 0.4)
    welcome2 = tk.Label(frame,fg = 'black',text="BLACKJACK!!!",height = 300,width = 1500,bg = 'gray',anchor = 'center')
    welcome2.config(font = welcomefont)
    welcome2.place(relx = 0.1,rely = 0.4,relwidth = 0.8,relheight = 0.2)
    
    playfont = ('times',15,'bold')
    button = tk.Button(frame, text="PLAY",activeforeground = 'red' , fg = 'red' , bg = 'black',height = 3,width = 20, command = lambda : play(root,tk) )
    button.config(font = playfont)
    button.place(relx = 0.4,rely = 0.7,relwidth = 0.2 , relheight = 0.1)
    return

welcome(root,tk)

root.mainloop()