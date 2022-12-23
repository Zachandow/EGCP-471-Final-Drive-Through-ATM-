#!/usr/bin/python3
from distanceReader import *
import tkinter as tk
import time
import atexit
import RPi.GPIO as GPIO
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from time import sleep

current_balance = 1000

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
    mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)


atexit.register(turnOffMotors)
myMotor1 = mh.getMotor(3)
myMotor2 = mh.getMotor(1)
myMotor1.setSpeed(0)
myMotor2.setSpeed(0)


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {'Balance': tk.IntVar()}

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (AdjustmentPage, StartPage, MenuPage, WithdrawPage, DepositPage, BalancePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("AdjustmentPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class AdjustmentPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='DRIVE THROUGH ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        adjustment_label = tk.Label(self,
                                    text='Please configure to your liking',
                                    font=('Orbitron', 30),
                                    fg='white',
                                    bg='#3d3d5c')
        adjustment_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def GPIO_up_button():
            myMotor1.run(Raspi_MotorHAT.FORWARD)
            myMotor1.setSpeed(255)
            time.sleep(2)
            turnOffMotors()

        up_button = tk.Button(button_frame,
                              text='Move up',
                              font=('Pacifico', 30),
                              command=GPIO_up_button,
                              relief='raised',
                              borderwidth=3,
                              width=17,
                              height=2)
        up_button.place(x=725, y=200)

        def GPIO_down_button():
            myMotor1.run(Raspi_MotorHAT.BACKWARD)
            myMotor1.setSpeed(255)
            time.sleep(2)
            turnOffMotors()

        down_button = tk.Button(button_frame,
                                text='Move down',
                                font=('Orbitron', 30),
                                command=GPIO_down_button,
                                relief='raised',
                                borderwidth=3,
                                width=17,
                                height=2)
        down_button.place(x=725, y=400)

        def GPIO_out_button():
            myMotor2.run(Raspi_MotorHAT.BACKWARD)
            myMotor2.setSpeed(255)
            time.sleep(4)
            turnOffMotors()

        out_button = tk.Button(button_frame,
                               text='Move Out',
                               font=('Orbitron', 30),
                               command=GPIO_out_button,
                               relief='raised',
                               borderwidth=3,
                               width=17,
                               height=2)

        out_button.place(x=275, y=300)

        def GPIO_in_button():
            myMotor2.run(Raspi_MotorHAT.FORWARD)
            myMotor2.setSpeed(255)
            time.sleep(4)
            turnOffMotors()

        in_button = tk.Button(button_frame,
                              text='Move in',
                              font=('Orbitron', 30),
                              command=GPIO_in_button,
                              relief='raised',
                              borderwidth=3,
                              width=17,
                              height=2)
        in_button.place(x=1175, y=300)

        def done():
            controller.show_frame('StartPage')

        done_button = tk.Button(button_frame,
                                text='Done',
                                font=('Orbitron', 30),
                                command=done,
                                relief='raised',
                                borderwidth=3,
                                width=17,
                                height=2)
        done_button.place(x=725, y=300)
        #        done_button.grid(row=1, column=2, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

#        def exit():
#            myMotor1

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        self.controller.title('Securitex')
        self.controller.attributes('-zoomed', True)
        # self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self,
                                 text='DRIVE THROUGH ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        password_label = tk.Label(self,
                                  text='Enter your password',
                                  font=('orbitron', 13),
                                  bg='#3d3d5c',
                                  fg='white')
        password_label.pack(pady=10)

        my_password = tk.StringVar()
        password_entry_box = tk.Entry(self,
                                      textvariable=my_password,
                                      font=('orbitron', 12),
                                      width=22)
        password_entry_box.focus_set()
        password_entry_box.pack(ipady=7)

        def handle_focus_in(_):
            password_entry_box.configure(fg='black', show='*')

        password_entry_box.bind('<FocusIn>', handle_focus_in)

        def check_password():
            if my_password.get() == 'egcp471':
                my_password.set('')
                incorrect_password_label['text'] = ''
                controller.show_frame('MenuPage')
            else:
                incorrect_password_label['text'] = 'Incorrect Password'

        enter_button = tk.Button(self,
                                 text='Enter',
                                 command=check_password,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        incorrect_password_label = tk.Label(self,
                                            text='',
                                            font=('orbitron', 13),
                                            fg='white',
                                            bg='#33334d',
                                            anchor='n')
        incorrect_password_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.gif')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.gif')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.gif')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class MenuPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='DRIVE THROUGH ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        main_menu_label = tk.Label(self,
                                   text='Main Menu',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#3d3d5c')
        main_menu_label.pack()

        selection_label = tk.Label(self,
                                   text='Please make a selection',
                                   font=('orbitron', 13),
                                   fg='white',
                                   bg='#3d3d5c',
                                   anchor='w')
        selection_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def withdraw():
            controller.show_frame('WithdrawPage')

        withdraw_button = tk.Button(button_frame,
                                    text='Withdraw',
                                    command=withdraw,
                                    relief='raised',
                                    borderwidth=3,
                                    width=50,
                                    height=5)
        withdraw_button.grid(row=0, column=0, pady=5)

        def deposit():
            controller.show_frame('DepositPage')

        deposit_button = tk.Button(button_frame,
                                   text='Deposit',
                                   command=deposit,
                                   relief='raised',
                                   borderwidth=3,
                                   width=50,
                                   height=5)
        deposit_button.grid(row=1, column=0, pady=5)

        def balance():
            controller.show_frame('BalancePage')

        balance_button = tk.Button(button_frame,
                                   text='Balance',
                                   command=balance,
                                   relief='raised',
                                   borderwidth=3,
                                   width=50,
                                   height=5)
        balance_button.grid(row=2, column=0, pady=5)

        def exit():
            controller.show_frame('AdjustmentPage')
            tmpD = distance_V()

            while (tmpD > 22):
                myMotor1.run(Raspi_MotorHAT.FORWARD)
                myMotor1.setSpeed(255)
                tmpD = distance_V()
                time.sleep(0.1)

            while (tmpD < 20):
                myMotor1.run(Raspi_MotorHAT.BACKWARD)
                myMotor1.setSpeed(255)
                tmpD = distance_V()
                time.sleep(0.1)

            myMotor1.setSpeed(0)
            myMotor2.run(Raspi_MotorHAT.FORWARD)
            myMotor2.setSpeed(255)
            time.sleep(40)
            turnOffMotors()


        exit_button = tk.Button(button_frame,
                                text='Exit',
                                command=exit,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=3, column=0, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.gif')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.gif')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.gif')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class WithdrawPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='GROUP 3 DRIVE-THRU ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        choose_amount_label = tk.Label(self,
                                       text='Choose the amount you want to withdraw',
                                       font=('orbitron', 13),
                                       fg='white',
                                       bg='#3d3d5c')
        choose_amount_label.pack()

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def withdraw(amount):
            global current_balance
            current_balance -= amount
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')

        twenty_button = tk.Button(button_frame,
                                  text='20',
                                  command=lambda: withdraw(20),
                                  relief='raised',
                                  borderwidth=3,
                                  width=50,
                                  height=5)
        twenty_button.grid(row=0, column=0, pady=5)

        forty_button = tk.Button(button_frame,
                                 text='40',
                                 command=lambda: withdraw(40),
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=5)
        forty_button.grid(row=1, column=0, pady=5)

        sixty_button = tk.Button(button_frame,
                                 text='60',
                                 command=lambda: withdraw(60),
                                 relief='raised',
                                 borderwidth=3,
                                 width=50,
                                 height=5)
        sixty_button.grid(row=2, column=0, pady=5)

        eighty_button = tk.Button(button_frame,
                                  text='80',
                                  command=lambda: withdraw(80),
                                  relief='raised',
                                  borderwidth=3,
                                  width=50,
                                  height=5)
        eighty_button.grid(row=3, column=0, pady=5)

        one_hundred_button = tk.Button(button_frame,
                                       text='100',
                                       command=lambda: withdraw(100),
                                       relief='raised',
                                       borderwidth=3,
                                       width=50,
                                       height=5)
        one_hundred_button.grid(row=0, column=1, pady=5, padx=555)

        two_hundred_button = tk.Button(button_frame,
                                       text='200',
                                       command=lambda: withdraw(200),
                                       relief='raised',
                                       borderwidth=3,
                                       width=50,
                                       height=5)
        two_hundred_button.grid(row=1, column=1, pady=5)

        three_hundred_button = tk.Button(button_frame,
                                         text='300',
                                         command=lambda: withdraw(300),
                                         relief='raised',
                                         borderwidth=3,
                                         width=50,
                                         height=5)
        three_hundred_button.grid(row=2, column=1, pady=5)

        cash = tk.StringVar()
        other_amount_entry = tk.Entry(button_frame,
                                      textvariable=cash,
                                      width=59,
                                      justify='right')
        other_amount_entry.grid(row=3, column=1, pady=5, ipady=30)

        def other_amount(_):
            global current_balance
            current_balance -= int(cash.get())
            controller.shared_data['Balance'].set(current_balance)
            cash.set('')
            controller.show_frame('MenuPage')

        other_amount_entry.bind('<Return>', other_amount)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.gif')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.gif')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.gif')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class DepositPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='DRIVE THROUGH ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        space_label = tk.Label(self, height=4, bg='#3d3d5c')
        space_label.pack()

        enter_amount_label = tk.Label(self,
                                      text='Enter amount',
                                      font=('orbitron', 13),
                                      bg='#3d3d5c',
                                      fg='white')
        enter_amount_label.pack(pady=10)

        cash = tk.StringVar()
        deposit_entry = tk.Entry(self,
                                 textvariable=cash,
                                 font=('orbitron', 12),
                                 width=22)
        deposit_entry.pack(ipady=7)

        def deposit_cash():
            global current_balance
            current_balance += int(cash.get())
            controller.shared_data['Balance'].set(current_balance)
            controller.show_frame('MenuPage')
            cash.set('')

        enter_button = tk.Button(self,
                                 text='Enter',
                                 command=deposit_cash,
                                 relief='raised',
                                 borderwidth=3,
                                 width=40,
                                 height=3)
        enter_button.pack(pady=10)

        two_tone_label = tk.Label(self, bg='#33334d')
        two_tone_label.pack(fill='both', expand=True)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.gif')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.gif')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.gif')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


class BalancePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#3d3d5c')
        self.controller = controller

        heading_label = tk.Label(self,
                                 text='DRIVE THROUGH ATM',
                                 font=('orbitron', 45, 'bold'),
                                 foreground='#ffffff',
                                 background='#3d3d5c')
        heading_label.pack(pady=25)

        global current_balance
        controller.shared_data['Balance'].set(current_balance)
        balance_label = tk.Label(self,
                                 textvariable=controller.shared_data['Balance'],
                                 font=('orbitron', 13),
                                 fg='white',
                                 bg='#3d3d5c',
                                 anchor='w')
        balance_label.pack(fill='x')

        button_frame = tk.Frame(self, bg='#33334d')
        button_frame.pack(fill='both', expand=True)

        def menu():
            controller.show_frame('MenuPage')

        menu_button = tk.Button(button_frame,
                                command=menu,
                                text='Menu',
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        menu_button.grid(row=0, column=0, pady=5)

        def exit():
            controller.show_frame('AdjustmentPage')
            tmpD = distance_V()

            while (tmpD > 22):
                myMotor1.run(Raspi_MotorHAT.FORWARD)
                myMotor1.setSpeed(255)
                tmpD = distance_V()
                time.sleep(0.1)

            while (tmpD < 20):
                myMotor1.run(Raspi_MotorHAT.BACKWARD)
                myMotor1.setSpeed(255)
                tmpD = distance_V()
                time.sleep(0.1)

            myMotor1.setSpeed(0)
            myMotor2.run(Raspi_MotorHAT.FORWARD)
            myMotor2.setSpeed(255)
            time.sleep(40)
            turnOffMotors()

        exit_button = tk.Button(button_frame,
                                text='Exit',
                                command=exit,
                                relief='raised',
                                borderwidth=3,
                                width=50,
                                height=5)
        exit_button.grid(row=1, column=0, pady=5)

        bottom_frame = tk.Frame(self, relief='raised', borderwidth=3)
        bottom_frame.pack(fill='x', side='bottom')

        visa_photo = tk.PhotoImage(file='visa.gif')
        visa_label = tk.Label(bottom_frame, image=visa_photo)
        visa_label.pack(side='left')
        visa_label.image = visa_photo

        mastercard_photo = tk.PhotoImage(file='mastercard.gif')
        mastercard_label = tk.Label(bottom_frame, image=mastercard_photo)
        mastercard_label.pack(side='left')
        mastercard_label.image = mastercard_photo

        american_express_photo = tk.PhotoImage(file='american-express.gif')
        american_express_label = tk.Label(bottom_frame, image=american_express_photo)
        american_express_label.pack(side='left')
        american_express_label.image = american_express_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')
            time_label.config(text=current_time)
            time_label.after(200, tick)

        time_label = tk.Label(bottom_frame, font=('orbitron', 12))
        time_label.pack(side='right')

        tick()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
