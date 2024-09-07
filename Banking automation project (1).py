#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from tkinter.ttk import Combobox
import time
from tkinter import messagebox
import sqlite3
import re

try:
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("create table acn(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_opendate text,acn_gender text)")
    conobj.close()
    print("table created")
except:
    print("something went wrong,might be table already exists")
    
win=Tk()
win.configure(bg="pink")
win.state("zoomed")
win.resizable(width=False,height=False)
title=Label(win,text="Banking Automation",font=("arial",20,"bold",'underline'),bg="pink")
title.pack()

dt=time.strftime("%d %b %Y")
date=Label(win,text=f"{dt}",font=("arial",20,"bold"),bg="pink",fg="blue")
date.place(relx=0.86,rely=0.1)

def main_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.95)

    def forgotpass():
        frm.destroy()
        forgotpass_screen()

    def new():
        frm.destroy()
        newuser_screen()

    def login_db():
        global gacn
        gacn=e_acn.get()
        pwd=e_pass.get()
        if len(gacn)==0 or len(pwd)==0:
            messagebox.showwarning("Validation","Empty fields are not allowed")
            return

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_no,acn_pass from acn where acn_no=? and acn_pass=?",(gacn,pwd))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showwarning("Login","Invalid details")
        else:
            frm.destroy()
            welcome_screen()

        conobj.commit()
        conobj.close()
        
    def clear():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()

    lbl_acn=Label(frm,text=("ACN"),font=("arial",20,"bold"),bg="powder blue")
    lbl_acn.place(relx=0.3,rely=0.1)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=0.4,rely=0.1)
    e_acn.focus()

    lbl_pass=Label(frm,text=("Pass"),font=("arial",20,"bold"),bg="powder blue")
    lbl_pass.place(relx=0.3,rely=0.2)

    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,show='*')
    e_pass.place(relx=0.4,rely=0.2)

    btn_login=Button(frm,text=("login"),font=("arial",20,"bold"),command=login_db)
    btn_login.place(relx=0.42,rely=0.3)

    btn_clear=Button(frm,text=("clear"),font=("arial",20,"bold"),command=clear)
    btn_clear.place(relx=0.5,rely=0.3)

    btn_forgotpass=Button(frm,command=forgotpass,text=("forgot password"),font=("arial",20,"bold"))
    btn_forgotpass.place(relx=0.4,rely=0.4)

    btn_new=Button(frm,command=new,text=("open new account"),font=("arial",20,"bold"))
    btn_new.place(relx=0.39,rely=0.5)

def forgotpass_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.95)

    def back():
        frm.destroy()
        main_screen()

    def forgotpass_db():
        acn=e_acn.get()
        mob=e_mob.get()
        email=e_email.get()
        
        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_pass from acn where acn_no=? and acn_mob=? and acn_email=?",(acn,mob,email))
        tup=curobj.fetchone()
        if tup==None:
            messagebox.showwarning("Forgot password","Invalid details")
        else:    
            messagebox.showinfo("Forgot password",f"Your password is: {tup[0]}")
        conobj.commit()
        conobj.close()

        e_acn.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")

    btn_back=Button(frm,command=back,text=("back"),font=("arial",20,"bold"),bd=5)
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text=("ACN"),font=("arial",20,"bold"),bg="powder blue")
    lbl_acn.place(relx=0.3,rely=0.1)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_acn.place(relx=0.4,rely=0.1)
    e_acn.focus()

    lbl_email=Label(frm,text=("Email"),font=("arial",20,"bold"),bg="powder blue")
    lbl_email.place(relx=0.3,rely=0.2)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=0.4,rely=0.2)

    lbl_mob=Label(frm,text=("Mob"),font=("arial",20,"bold"),bg="powder blue")
    lbl_mob.place(relx=0.3,rely=0.3)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=0.4,rely=0.3)
    
    btn_submit=Button(frm,text=("Submit"),font=("arial",20,"bold"),bd=5,command=forgotpass_db)
    btn_submit.place(relx=0.45,rely=0.4)

def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="powder blue")
    frm.place(relx=0,rely=0.15,relwidth=1,relheight=.95)

    def back():
        frm.destroy()
        main_screen()
    def newuser_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        gen=cb_gender.get()
        bal=0
        opendate=time.strftime("%d %B %Y,%A")

        match=re.fullmatch("[6-9][0-9]{9}",mob)
        if match==None:
            messagebox.showwarning("validation","Invalid format of mob")
            return

        match=re.fullmatch("[a-zA-Z0-9_]+[@][a-z]+\.[a-zA-Z]+",email)
        if match==None:
            messagebox.showwarning("validation","Invalid format of email")
            return

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into acn(acn_name,acn_pass,acn_email,acn_mob,acn_gender,acn_opendate,acn_bal) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,gen,opendate,bal))
        curobj.execute("select max(acn_no) from acn")
        tup=curobj.fetchone()
        messagebox.showinfo("New User",f"Your account no. is {tup[0]}")
        conobj.commit()
        conobj.close()
        e_name.delete(0,"end")
        e_pass.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        cb_gender.delete(0,"end")
        
    btn_back=Button(frm,command=back,text=("back"),font=("arial",20,"bold"),bd=5)
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text=("Name"),font=("arial",20,"bold"),bg="powder blue")
    lbl_name.place(relx=0.3,rely=0.1)

    e_name=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_name.place(relx=0.4,rely=0.1)
    e_name.focus()
    
    lbl_pass=Label(frm,text=("Pass"),font=("arial",20,"bold"),bg="powder blue")
    lbl_pass.place(relx=0.3,rely=0.2)

    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_pass.place(relx=0.4,rely=0.2)

    lbl_email=Label(frm,text=("Email"),font=("arial",20,"bold"),bg="powder blue")
    lbl_email.place(relx=0.3,rely=0.3)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_email.place(relx=0.4,rely=0.3)

    lbl_mob=Label(frm,text=("Mob"),font=("arial",20,"bold"),bg="powder blue")
    lbl_mob.place(relx=0.3,rely=0.4)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5)
    e_mob.place(relx=0.4,rely=0.4)

    lbl_gender=Label(frm,text=("Gender"),font=("arial",20,"bold"),bg="powder blue")
    lbl_gender.place(relx=0.3,rely=0.5)

    cb_gender=Combobox(frm,values=['---select---','Male','Female'],font=('arial',20,'bold'))
    cb_gender.place(relx=0.4,rely=0.5)

    btn_submit=Button(frm,text=("submit"),font=("arial",20,"bold"),bd=5,command=newuser_db)
    btn_submit.place(relx=0.45,rely=0.6)
    
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='powder blue')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def logout():
        frm.destroy()
        main_screen()

    def details():
        ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_opendate,acn_bal,acn_gender,acn_email,acn_mob from acn where acn_no=?",(gacn))
        tup=curobj.fetchone()
        conobj.close()

        lbl_wel=Label(ifrm,text="This is Details Screen",font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()
        
        lbl_open=Label(ifrm,text=f"Open Date:{tup[0]}",font=("arial",15,"bold"),bg="white")
        lbl_open.place(relx=0.2,rely=0.2)

        lbl_bal=Label(ifrm,text=f"Balance:{tup[1]}",font=("arial",15,"bold"),bg="white")
        lbl_bal.place(relx=0.2,rely=0.3)

        lbl_gender=Label(ifrm,text=f"Gender:{tup[2]}",font=("arial",15,"bold"),bg="white")
        lbl_gender.place(relx=0.2,rely=0.4)

        lbl_email=Label(ifrm,text=f"Email:{tup[3]}",font=("arial",15,"bold"),bg="white")
        lbl_email.place(relx=0.2,rely=0.5)

        lbl_mob=Label(ifrm,text=f"Mobile:{tup[4]}",font=("arial",15,"bold"),bg="white")
        lbl_mob.place(relx=0.2,rely=0.6)
        
    def update():
        ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        conobj=sqlite3.connect(database="bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select acn_name,acn_pass,acn_email,acn_mob from acn where acn_no=?",(gacn))
        tup=curobj.fetchone()
        conobj.close()

        lbl_wel=Label(ifrm,text="This is Update Screen",font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_name=Label(ifrm,text="Name",font=("arial",20,"bold"),bg="white")
        lbl_name.place(relx=0.2,rely=0.2)

        e_name=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_name.place(relx=0.2,rely=0.3)
        e_name.insert(0,tup[0])
        e_name.focus()

        lbl_pwd=Label(ifrm,text="Pass",font=("arial",20,"bold"),bg="white")
        lbl_pwd.place(relx=0.2,rely=0.5)

        e_pwd=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_pwd.place(relx=0.2,rely=0.6)
        e_pwd.insert(0,tup[1])

        lbl_email=Label(ifrm,text="Email",font=("arial",20,"bold"),bg="white")
        lbl_email.place(relx=0.6,rely=0.2)

        e_email=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_email.place(relx=0.6,rely=0.3)
        e_email.insert(0,tup[2])

        lbl_mob=Label(ifrm,text="Mob",font=("arial",20,"bold"),bg="white")
        lbl_mob.place(relx=0.6,rely=0.5)

        e_mob=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_mob.place(relx=0.6,rely=0.6)
        e_mob.insert(0,tup[3])

        def update_db():
            name=e_name.get()
            pwd=e_pwd.get()
            email=e_email.get()
            mob=e_mob.get()

            match=re.fullmatch("[6-9][0-9]{9}",mob)
            if match==None:
                messagebox.showwarning("validation","Invalid format of mob")
                return

            match=re.fullmatch("[a-zA-Z0-9_]+[@][a-z]+\.[a-zA-Z]+",email)
            if match==None:
                messagebox.showwarning("validation","Invalid format of email")
                return

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update acn set acn_name=?,acn_pass=?,acn_email=?,acn_mob=?",(name,pwd,email,mob))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Update","Record updated")

        btn_update=Button(ifrm,text="Update",font=("arial",20,"bold"),bd=5,command=update_db)
        btn_update.place(relx=0.65,rely=0.77)

    def deposit():
        ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text="This is Deposit Screen",font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_amount=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amount.place(relx=0.2,rely=0.2)

        e_amount=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amount.place(relx=0.4,rely=0.2)
        e_amount.focus()

        def deposit_db():
            amount=float(e_amount.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            if amount>0:
                curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amount,gacn))
                messagebox.showinfo("Deposit",f"{amount} amount deposited")
            else:
                messagebox.showerror("Deposit","Invalid amount")
            conobj.commit()
            conobj.close()
            e_amount.delete(0,"end")
              
        btn_submit=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,command=deposit_db)
        btn_submit.place(relx=0.4,rely=0.4)

    def withdraw():
        ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text="This is withdraw Screen",font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_amount=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amount.place(relx=0.2,rely=0.2)

        e_amount=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amount.place(relx=0.4,rely=0.2)
        e_amount.focus()

        def withdraw_db():
            amount=float(e_amount.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn))
            tup=curobj.fetchone()
            if tup[0]>amount:
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amount,gacn))
                messagebox.showinfo("Withdraw",f"{amount} amount withdrawn successfully")
            else:
                messagebox.showwarning("Withdraw","Invalid amount")
            conobj.commit()
            conobj.close()
            e_amount.delete(0,"end")
            
        btn_submit=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,command=withdraw_db)
        btn_submit.place(relx=0.4,rely=0.4)

    def transfer():
        ifrm=Frame(frm,highlightbackground='black', highlightthickness=2)
        ifrm.configure(bg='white')
        ifrm.place(relx=.2,rely=.1,relwidth=.7,relheight=.5)

        lbl_wel=Label(ifrm,text="This is Transfer Screen",font=('arial',20,'bold'),bg='white',fg='blue')
        lbl_wel.pack()

        lbl_amount=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="white")
        lbl_amount.place(relx=0.2,rely=0.2)

        e_amount=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amount.place(relx=0.4,rely=0.2)
        e_amount.focus()

        lbl_to=Label(ifrm,text="To",font=("arial",20,"bold"),bg="white")
        lbl_to.place(relx=0.2,rely=0.4)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=0.4,rely=0.4)

        def transfer_db():
            amount=float(e_amount.get())
            to=e_to.get()
            if to==gacn:
                messagebox.showwarning("Transfer","To and From can't be same")
                return
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_bal from acn where acn_no=?",(gacn))
            tup1=curobj.fetchone()
            
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select acn_no from acn where acn_no=?",(to))
            tup2=curobj.fetchone()

            if tup2==None:
                messagebox.showwarning("Transfer","Invalid ACN")
                return
            if tup1[0]>amount:
                curobj.execute("update acn set acn_bal=acn_bal-? where acn_no=?",(amount,gacn))
                curobj.execute("update acn set acn_bal=acn_bal+? where acn_no=?",(amount,to))
                messagebox.showinfo("Transfer",f"{amount} amount transfered successfully to acn_no {to}")
            else:
                messagebox.showwarning("Transfer","Not sufficient balance")
            conobj.commit()
            conobj.close()
            e_amount.delete(0,"end")
            e_to.delete(0,"end")
            
        btn_submit=Button(ifrm,text="Submit",font=("arial",20,"bold"),bd=5,command=transfer_db)
        btn_submit.place(relx=0.4,rely=0.6)
        
    conobj=sqlite3.connect(database="bank.sqlite")
    curobj=conobj.cursor()
    curobj.execute("select acn_name from acn where acn_no=?",(gacn))
    tup=curobj.fetchone()
    conobj.commit()
    conobj.close()
    
    lbl_wel=Label(frm,text=f"Welcome,{tup[0]}",font=('arial',20,'bold'),bg='powder blue')
    lbl_wel.place(relx=0,rely=0)

    btn_logout=Button(frm,text="logout",font=('arial',20,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.9,rely=0)

    btn_details=Button(frm,command=details,width=10,text="Details",font=('arial',20,'bold'),bd=5)
    btn_details.place(relx=0,rely=.1)

    btn_update=Button(frm,command=update,width=10,text="Update",font=('arial',20,'bold'),bd=5)
    btn_update.place(relx=0,rely=.2)

    btn_deposit=Button(frm,command=deposit,width=10,text="Deposit",font=('arial',20,'bold'),bd=5)
    btn_deposit.place(relx=0,rely=.3)

    btn_withdraw=Button(frm,command=withdraw,width=10,text="Withdraw",font=('arial',20,'bold'),bd=5)
    btn_withdraw.place(relx=0,rely=.4)

    btn_transfer=Button(frm,command=transfer,width=10,text="Transfer",font=('arial',20,'bold'),bd=5)
    btn_transfer.place(relx=0,rely=.5)
    
    
main_screen()
win.mainloop()


# # 
