'''Popup Keyboard is a module to be used with Python's Tkinter library
It subclasses the Entry widget as KeyboardEntry to make a pop-up
keyboard appear when the widget gains focus. Still early in development.
'''

from Tkinter import *


class _PopupKeyboard(Toplevel):
    '''A Toplevel instance that displays a keyboard that is attached to
    another widget. Only the Entry widget has a subclass in this version.
    '''
    
    def __init__(self, parent, attach, x, y, keycolor, keysize=5):
        Toplevel.__init__(self, takefocus=0)
        
        self.overrideredirect(True)
        self.attributes('-alpha',0.85)

        self.parent = parent
        self.attach = attach
        self.keysize = keysize
        self.keycolor = keycolor
        self.x = x
        self.y = y

        self.row1 = Frame(self)
        self.row2 = Frame(self)
        self.row3 = Frame(self)
        self.row4 = Frame(self)

        self.row1.grid(row=1)
        self.row2.grid(row=2)
        self.row3.grid(row=3)
        self.row4.grid(row=4)
        
        self._init_keys()

        # destroy _PopupKeyboard on keyboard interrupt
        self.bind('<Key>', lambda e: self._destroy_popup())

        # resize to fit keys
        self.update_idletasks()
        self.geometry('{}x{}+{}+{}'.format(self.winfo_width(),
                                           self.winfo_height(),
                                           self.x,self.y))
        
    def _init_keys(self):
        self.alpha = {
            'row1' : ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','/'],
            'row2' : ['<<<','a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l',',','>>>'],
            'row3' : ['shift','z', 'x', 'c', 'v', 'b', 'n', 'm','.','?','[1,2,3]'],
            'row4' : ['@','#','%','*','[ space ]','+','-','=']
            }
        
        for row in self.alpha.iterkeys(): # iterate over dictionary of rows
            if row == 'row1':             # TO-DO: re-write this method
                i = 1                     # for readability and functionality
                for k in self.alpha[row]:
                    Button(self.row1,
                           text=k,
                           width=self.keysize,
                           bg=self.keycolor,
                           command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)
                    i += 1
            elif row == 'row2':
                i = 2
                for k in self.alpha[row]:
                    Button(self.row2,
                           text=k,
                           width=self.keysize,
                           bg=self.keycolor,
                           command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)
                    i += 1
            elif row == 'row3':
                i = 2
                for k in self.alpha[row]:
                    Button(self.row3,
                           text=k,
                           width=self.keysize,
                           bg=self.keycolor,
                           command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)
                    i += 1
            else:
                i = 3
                for k in self.alpha[row]:
                    if k == '[ space ]':
                        Button(self.row4,
                               text=k,
                               width=self.keysize * 3,
                               bg=self.keycolor,
                               command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)
                    else:
                        Button(self.row4,
                               text=k,
                               width=self.keysize,
                               bg=self.keycolor,
                               command=lambda k=k: self._attach_key_press(k)).grid(row=0,column=i)
                    i += 1

    def _destroy_popup(self):
        self.destroy()

    def _attach_key_press(self, k):
        if k == '>>>':
            self.attach.tk_focusNext().focus_set()
            self.destroy()
        elif k == '<<<':
            self.attach.tk_focusPrev().focus_set()
            self.destroy()
        elif k == '[1,2,3]':
            pass
        elif k == '[ space ]':
            self.attach.insert(END, ' ')
        else:
            self.attach.insert(END, k)

'''
TO-DO: Implement Number Pad
class _PopupNumpad(Toplevel):
    def __init__(self, x, y, keycolor='gray', keysize=5):
        Toplevel.__init__(self, takefocus=0)
        
        self.overrideredirect(True)
        self.attributes('-alpha',0.85)

        self.numframe = Frame(self)
        self.numframe.grid(row=1, column=1)

        self.__init_nums()

        self.update_idletasks()
        self.geometry('{}x{}+{}+{}'.format(self.winfo_width(),
                                           self.winfo_height(),
                                           self.x,self.y))

    def __init_nums(self):
        i=0
        for num in ['7','4','1','8','5','2','9','6','3']:
            print num
            Button(self.numframe,
                   text=num,
                   width=int(self.keysize/2),
                   bg=self.keycolor,
                   command=lambda num=num: self.__attach_key_press(num)).grid(row=i%3, column=i/3)
            i+=1
'''

class KeyboardEntry(Frame):
    '''An extension/subclass of the Tkinter Entry widget, capable
    of accepting all existing args, plus a keysize and keycolor option.
    Will pop up an instance of _PopupKeyboard when focus moves into
    the widget

    Usage:
    KeyboardEntry(parent, keysize=6, keycolor='white').pack()
    '''
    
    def __init__(self, parent, keysize=5, keycolor='gray', *args, **kwargs):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.entry = Entry(self, *args, **kwargs)
        self.entry.pack()

        self.keysize = keysize
        self.keycolor = keycolor
        
        self.state = 'idle'
        
        self.entry.bind('<FocusIn>', lambda e: self._check_state('focusin'))
        self.entry.bind('<FocusOut>', lambda e: self._check_state('focusout'))
        self.entry.bind('<Key>', lambda e: self._check_state('keypress'))

    def _check_state(self, event):
        '''finite state machine'''
        if self.state == 'idle':
            if event == 'focusin':
                self._call_popup()
                self.state = 'virtualkeyboard'
        elif self.state == 'virtualkeyboard':
            if event == 'focusin':
                self._destroy_popup()
                self.state = 'typing'
            elif event == 'keypress':
                self._destroy_popup()
                self.state = 'typing'
        elif self.state == 'typing':
            if event == 'focusout':
                self.state = 'idle'
        
    def _call_popup(self):
        self.kb = _PopupKeyboard(attach=self.entry,
                                 parent=self.parent,
                                 x=self.entry.winfo_rootx(),
                                 y=self.entry.winfo_rooty() + self.entry.winfo_reqheight(),
                                 keysize=self.keysize,
                                 keycolor=self.keycolor)

    def _destroy_popup(self):
        self.kb._destroy_popup()

def test():  
    root = Tk()
    KeyboardEntry(root, keysize=6, keycolor='white').pack()
    KeyboardEntry(root).pack()
    root.mainloop()
