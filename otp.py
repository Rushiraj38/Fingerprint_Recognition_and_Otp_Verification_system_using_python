from twilio.rest import Client
from tkinter import *
from tkinter.ttk import *
from ttkthemes import themed_tk as tk
from tkinter import messagebox
import smtplib
import random
import time


class otp:

    def __init__(self, window):

        """takes window to display all the attributes and Methods for this class"""

        self.window = window
        self.window.geometry("1366x720+0+0")
        self.window.title("Account Verification Page")
        self.window.resizable(False, False)
        self.start()

    def start(self):

        """it starts verification process"""

        self.login_frame = PhotoImage(file='otp_verification_frame.png')
        self.image_panel = Label(self.window, image=self.login_frame)
        self.image_panel.pack(fill='both', expand='yes')

        self.txt = "Account Verification"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.window, text=self.txt, font=('yu gothic ui', 30, "bold"), relief=FLAT)
        self.heading.place(x=470, y=70, width=450)

        # ============================Email========================================

        self.email_label = Label(self.window, text="Email or mobile number ", font=("yu gothic ui", 13, "bold"))
        self.email_label.place(x=495, y=180)
        self.email_entry = Entry(self.window, font=("yu gothic ui semibold", 12))
        self.email_entry.place(x=530, y=210, width=380)

        # ============================OTP=========================================

        self.otp_label = Label(self.window, text="Recent OTP ", font=("yu gothic ui", 13, "bold"))
        self.otp_label.place(x=495, y=295)
        self.otp_entry = Entry(self.window, font=("yu gothic ui semibold", 12))
        self.otp_entry.place(x=530, y=325, width=380)

        # ============================Verify Button================================

        self.verify = PhotoImage(file='verify.png')
        self.verify_button = Button(self.window, image=self.verify, cursor="hand2", command=self.click_verification)
        self.verify_button.place(x=640, y=403)

        # ============================Submit button================================

        self.send_otp = PhotoImage(file='send_otp.png')
        self.send_otp_button = Button(self.window, image=self.send_otp, cursor="hand2", command=self.validation)
        self.send_otp_button.place(x=500, y=503)

        # ============================Exit button================================

        self.exit_img = PhotoImage(file='exit.png')
        self.exit_button = Button(self.window, image=self.exit_img, cursor="hand2", command=self.click_exit)
        self.exit_button.place(x=783, y=503)

        # =============================timer button================================

        self.timer_label = Label(self.window, text='Countdown', font=("yu gothic ui", 13, "bold"))
        self.timer_label.place(x=670, y=590)
        self.sec = StringVar()
        self.sec_entry = Entry(self.window, textvariable=self.sec, width=2, font=("yu gothic ui semibold", 12))
        self.sec_entry.place(x=725, y=550)
        self.sec.set('00')
        self.mins = StringVar()
        self.mins_entry = Entry(self.window, textvariable=self.mins, width=2, font=("yu gothic ui semibold", 12))
        self.mins_entry.place(x=700, y=550)
        self.mins.set('02')
        self.hrs = StringVar()
        self.hrs_entry = Entry(self.window, textvariable=self.hrs, width=2, font=("yu gothic ui semibold", 12))
        self.hrs_entry.place(x=675, y=550)
        self.hrs.set('00')

    def validation(self):

        """validates if email entry field is left empty, if True
        returns info message displaying to enter the email address"""

        if self.email_entry.get() == '':
            messagebox.showinfo("Empty", "Please Enter Email Address or mobile")
        else:
            self.click_send_otp()

    def countdown(self):
        times = int(self.hrs.get()) * 3600 + int(self.mins.get()) * 60 + int(self.sec.get())
        while times > -1:
            minute, second = (times // 60, times % 60)
            hour = 0
            if minute > 60:
                hour, minute = (minute // 60, minute % 60)
            self.sec.set(second)
            self.mins.set(minute)
            self.hrs.set(hour)

            self.window.update()
            time.sleep(1)
            if (times == 0):
                messagebox.showinfo("time's up", "you must resend the otp")
                self.sec.set('00')
                self.mins.set('02')
                self.hrs.set('00')
            times -= 1

    def click_send_otp(self):

        """Sends and OTP to the email that a user uses to create admin account, BaseException is handled to avoid
        internet issue or wrong email address that may often happen due to use"""

        if self.email_entry.get() != "":

            try:
                try:
                    self.value = random.randint(100000, 999999)
                    # print(value)
                    if "@" in self.email_entry.get():
                        server = smtplib.SMTP("smtp.gmail.com", 587)
                        server.starttls()

                        server.login("otpv234@gmail.com", "Otpveri#234")
                        self.e = str(self.email_entry.get())
                        server.sendmail("otpv234@gmail.com", f"{self.e}", f"{self.value}")

                        messagebox.showinfo("Success", "OTP have been sent")

                    elif len(self.email_entry.get()) == 10:
                        age1 = "+91" + self.email_entry.get()
                        client = Client("Enter SID", "Enter your credential here")
                        client.messages.create(to=(age1), from_="+13863563540", body=self.value)


                except BaseException as msg:
                    messagebox.showerror("Failed",
                                         "There is an error sending OTP\n Make sure you are connected to internet")

            except BaseException as msg:
                print(msg)
            self.countdown()
        else:
            messagebox.showerror("Empty", "Please Enter Email Address or mobile \nand Click Send OTP")

    def click_verification(self):

        """if OTP entry field is not empty, it will verify the actual OTP with user OTP that they
        entered in OTP field"""

        if self.otp_entry.get() != "":
            print(self.otp_entry.get())
            try:
                if int(self.otp_entry.get()) == self.value:
                    messagebox.showinfo("Success", "You Have Been Successfully Verified")
                else:
                    messagebox.showerror("Bad Requests", "Sorry we were not able to identify you")
            except ValueError:
                messagebox.showerror("Bad Requests", "Sorry we were not able to identify you")

        else:
            messagebox.showerror("Empty", "Please Enter recent OTP from your email")

    def click_exit(self):

        """Terminates the program when if returned True"""

        ask = messagebox.askyesnocancel("Confirm Exit", "Are you sure you want to Exit\nSystem?")
        if ask is True:
            self.window.withdraw()


def win():
    window = tk.ThemedTk()
    window.get_themes()
    window.set_theme("arc")
    otp(window)
    window.mainloop()


if __name__ == '__main__':
    win()
