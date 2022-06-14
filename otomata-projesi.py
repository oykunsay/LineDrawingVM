import tkinter as tk
from tkinter import BOTH, BOTTOM, HORIZONTAL,CENTER, LEFT, RIGHT, TOP, VERTICAL, PanedWindow, ttk
from tkinter import filedialog as fd
from turtle import ScrolledCanvas, RawTurtle, TurtleScreen
import lex
import yacc

###################################### LEXING #########################################
tokens = (
    'NUMBER',
    'RED',
    'GREEN',
    'BLUE',
    'BLACK',
    'FORW',
    'RIGHT',
    'COLOR',
    'PEN',
) 

t_FORW    = r'F'
t_RIGHT   = r'R'
t_COLOR  = r'COLOR'
t_PEN  = r'PEN'
t_RED  = r'K'
t_GREEN  = r'Y'
t_BLUE  = r'M'
t_BLACK  = r'S'
 
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t 

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value) 
    
t_ignore  = ' \t' 

##################### PARSING ########################

#FUNCTIONS

def forw(num1):
    turtle.forward(num1)
def right(num2):
    turtle.right(num2)
    
def pensize(num4):
    if num4 == 1:
        turtle.pensize(1)
    elif num4 == 2:
        turtle.pensize(3)
    elif num4 == 3:
       turtle.pensize(5)

precedence = (
     ('left', 'FORW', 'RIGHT'),
     ('left', 'COLOR', 'PEN'),
 )
 
########################################### PARSER ##############################################

def p_start(p):
    '''start : function 
             | function option 
             | errormessage'''
    if len(p)==2:
        p[0]=p[1]
    elif len(p)==3:
        p[0]= (p[1],p[2])

def p_function(p):
    '''
    function : forward
             | right
             | color
             | pen
    '''
    p[0]=p[1] 

def p_empty(p):
    'empty :'
    pass
 
def p_option(p):
    '''option : start
              | empty '''
    p[0]=p[1]
    

def p_forward(p):
    'forward : FORW NUMBER' 
    p[0]= forw(p[2])
    
 
def p_right(p):
    'right : RIGHT NUMBER'
    p[0]= right(p[2])
    

def p_color(p):
    'color : COLOR colors'
    
def p_colors(p):
    '''colors : BLACK 
              | BLUE
              | GREEN
              | RED '''
    if p[1] == 'S':
        p[0]=turtle.color("black")
    elif p[1] == 'M':
        p[0]=turtle.color("blue")
    elif p[1] == 'Y':
        p[0]=turtle.color("green")
    elif p[1] == 'K':
        p[0]=turtle.color("red")
   

def p_pen(p):
    'pen : PEN NUMBER'
    p[0]=pensize(p[2])
    

######################################### GUI ########################################
root = tk.Tk()
root.title("Automata Theory")
root.geometry("800x600")

def read_file(a): 
    file = open(a,'r')

    read_file = file.read()
    T = tk.Label(right_panel, 
              text=read_file, bg="light blue", fg="white", width=50, font=("Arial", 30)).pack(fill=BOTH)

    file.close()

    lexer.input(read_file)
    result=parser.parse(read_file)
    print(result)


def choose_file():
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=(("text files",".txt"),
        ("all files",".*")))
    read_file(filename)


##################### TURTLE'I GUI'YE EKLEME ##################

canvas = ScrolledCanvas(root) 
canvas.pack(side=LEFT, fill=BOTH) 
screen = TurtleScreen(canvas) 
turtle = RawTurtle(canvas) 


open_button = ttk.Button(
    root,
    text='Dosya Seç',
    command=choose_file
)

panel_2 = PanedWindow(bd=4, relief="raised")
panel_2.pack(fill=BOTH, expand= 1)
open_button.pack(pady= "10")

#KONTROL PANELI
right_panel = PanedWindow(panel_2, orient=HORIZONTAL, bd=2, relief="raised", bg="light blue")
panel_2.add(right_panel)


#ERROR PANEL
bottom_panel = PanedWindow(panel_2, orient=VERTICAL, bd=2, relief="raised", height= "250", bg= "light green")
panel_2.add(bottom_panel)
bottom_panel.pack(fill= BOTH, side= BOTTOM)

    
def t_error(t):
    E1= tk.Label(bottom_panel, 
              text="error: invalid syntax", bg="light green", fg="dark green", width=50, font=("Arial", 11)).pack(fill=BOTH)
    t.lexer.skip(1)
    
def p_error(p):
    E2= tk.Label(bottom_panel, 
              text="error: invalid syntax", bg="light green", fg="dark green", width=50, font=("Arial", 11)).pack(fill=BOTH)


def p_WrongCommandError(p):
    '''errormessage : FORW RED option
                    | FORW BLUE option
                    | FORW BLACK option
                    | FORW GREEN option
                    | RIGHT RED option
                    | RIGHT BLUE option
                    | RIGHT BLACK option
                    | RIGHT GREEN option
                    | PEN RED option
                    | PEN BLUE option
                    | PEN BLACK option
                    | PEN GREEN option
                    | COLOR NUMBER option'''
    if p[1]=='F':
        EF= tk.Label(bottom_panel, 
              text="error: incorrect value after F command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1]=='R':
        ER= tk.Label(bottom_panel, 
              text="error: incorrect value after R command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1]=='PEN':
        EP= tk.Label(bottom_panel, 
              text="error: incorrect value after PEN command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1]=='COLOR':
        EC= tk.Label(bottom_panel, 
              text="error: incorrect value after COLOR command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)

def p_MissingValueError(p):
    '''errormessage : FORW empty option
                    | RIGHT empty option
                    | COLOR empty option
                    | PEN empty option '''
 
    if p[1] == 'F':
        EF1= tk.Label(bottom_panel, 
              text="error : missing value after F command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1] == 'R':
        EF2= tk.Label(bottom_panel, 
              text="error : missing value after R command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1] == 'COLOR':
        EF3= tk.Label(bottom_panel, 
              text="error : missing value after COLOR command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[1] == 'PEN':
        EF4= tk.Label(bottom_panel, 
              text="error : missing value after PEN command", bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
        
def p_MissingCommandError(p):
    '''errormessage : option empty NUMBER option
                    | option empty RED option 
                    | option empty BLUE option 
                    | option empty GREEN option 
                    | option empty BLACK option '''

    if p[3] == 'K':
        EK= tk.Label(bottom_panel, 
              text=("error : missing command before '%s'" % (p[3])), bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[3] == 'M':
        EM= tk.Label(bottom_panel, 
              text=("error : missing command before '%s'" % (p[3])), bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[3] == 'Y':
        EY= tk.Label(bottom_panel, 
              text=("error : missing command before '%s'" % (p[3])), bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    elif p[3] == 'S':
        ES= tk.Label(bottom_panel, 
              text=("error : missing command before '%s'" % (p[3])), bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)
    else:
        ELS= tk.Label(bottom_panel, 
              text=("error : missing command before '%s'" % (p[3])), bg="light green", fg="dark green", width=50, font=("Arial", 12)).pack(fill=BOTH)

parser=yacc.yacc()
lexer = lex.lex()


root.mainloop()