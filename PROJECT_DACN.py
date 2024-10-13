from tkinter import *
from check_password import check_pass, cap_lai, check_pass_cu, doi_mat_khau_moi, check_cccd, password, check_rfid
import time
import random
from tkinter import messagebox
import pandas as pd
import tkinter as tk
import numpy as np
import RPi.GPIO as GPIO
from SimpleMFRC522 import SimpleMFRC522
import telepot
from telepot.loop import MessageLoop    
import MFRC522
from Cam_bien_van_tay import save_van_tay, find_van_tay, remove_van_tay

khoa_pin = 15 #13
led_state = 38
buzzer_state = 40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_state, GPIO.OUT)
GPIO.setup(buzzer_state, GPIO.OUT)
GPIO.setup(khoa_pin, GPIO.OUT)
GPIO.setwarnings(False)



data_mk = pd.read_csv('Mat_khau.csv')
txt_pass = ""  
hidden_pass = ""
pass_word = password(str(list(data_mk['Mật khẩu'])[-1]))
print('Pass_word: ', pass_word)
txt_ccd_corect = "1234567891011"
txt_cccd = ""
dem_sai_mk = 0
len_pass = len(pass_word)

def buzzer_on(time_sleep, n_on):
    for i in range (n_on):
        GPIO.output(buzzer_state, GPIO.HIGH)
        time.sleep(time_sleep)
        GPIO.output(buzzer_state, GPIO.LOW)
        time.sleep(time_sleep)
    
def led_buzzer_on(time_sleep, n_on):
    for i in range (n_on):
        GPIO.output([led_state, buzzer_state], GPIO.HIGH)
        time.sleep(time_sleep)
        GPIO.output([led_state, buzzer_state], GPIO.LOW)
        time.sleep(time_sleep)
        
def led_on(time_sleep, n_on):
    for i in range (n_on):
        GPIO.output(led_state, GPIO.HIGH)
        time.sleep(time_sleep)
        GPIO.output(led_state, GPIO.LOW)
        time.sleep(time_sleep)
        
def clear_all():
    global txt_pass, hidden_pass
    txt_pass = ""
    hidden_pass = ""
    label_result.config(text=hidden_pass)
    GPIO.output(buzzer_state, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzer_state, GPIO.LOW)
    
def clear():
    global txt_pass, hidden_pass
    try:
        
        txt_pass = txt_pass[:-1]
        hidden_pass = hidden_pass[:-1]
        label_result.config(text=hidden_pass)
        GPIO.output(buzzer_state, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(buzzer_state, GPIO.LOW)
    except:
        label_result.config(text='error')


def show(value): # Nhan cac nut thi hien ky tu len man hinh
    global txt_pass
    global hidden_pass
    
    txt_pass += value
    hidden_pass += '*'
    label_result.config(text= hidden_pass)
    GPIO.output(buzzer_state, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(buzzer_state, GPIO.LOW)


        
def tat_phim():
    b0 = Button(top, text="0", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=120) 
    b1 = Button(top, text="1", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=120) 
    b2 = Button(top, text="2", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=120) 

    b3 = Button(top, text="3", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=170) 
    b4=Button(top, text="4", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=170) 
    b5= Button(top, text="5", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=170) 

    b6 = Button(top, text="6", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=220) 
    b7 = Button(top, text="7", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=220) 
    b8 = Button(top, text="8", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=220) 

    b9 = Button(top, text="9", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=270) 
    bca = Button(top, text="CA", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=270) 
    bc = Button(top, text="C", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=270) 
    bxn = Button(top, text="Xác nhận", width=8, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#ff9001").place(x=240, y=330) 
    bq = Button(top, text="Quên mật khẩu", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239").place(x=205, y=400) 
    bd = Button(top, text="Đổi mật khẩu", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239").place(x=205, y=450) 
    b_van_tay = Button(top, text="Vân tay", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239").place(x=205, y=500) 
    b_rfid = Button(top, text = 'Thẻ từ', width=15, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#DA4239")
    b_rfid.place(x=205, y = 550)
    b_add_rfid = Button(top, text = 'Thêm thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239").place(x=390, y=120) 
    b_remove_rfid = Button(top, text = 'Xóa thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239").place(x=390, y=170) 
    b_add_van_tay = Button(top, text = 'Thêm vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239").place(x=390, y=220) 
    b_remove_van_tay = Button(top, text = 'Xóa vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239").place(x=390, y=270) 
        
def xac_nhan():
    global txt_pass, pass_word, hidden_pass, dem_sai_mk
    
    label_matkhau.config(text = 'Mật khẩu')
    print('Pass_word: ', pass_word)
    state_pass = check_pass(txt_pass, pass_word)
    if state_pass == True:
        tat_phim()
        
        b_dong_cua = Button(top, text="Đóng cửa", width=10, height=1,
            font=('arial', 10, 'bold'), bd= 1,
            fg = "#fff",bg="#3697f5",
            command=lambda: dong_cua())
        b_dong_cua.place(x=20, y=100)
        dem_sai_mk = 0
        GPIO.output(led_state, GPIO.HIGH)
        GPIO.output(buzzer_state, GPIO.HIGH)
        GPIO.output(khoa_pin, GPIO.HIGH)
        label_result.config(text='Mở cửa thành công')
        label_result.update()
        time.sleep(2)
        GPIO.output(buzzer_state, GPIO.LOW)
        hidden_pass = ""
        txt_pass = ""
        label_result.config(text='Mời bạn đóng cửa')
        
    else:
        
        b_dong_cua = Label(top, text="", width=20, height=2,
            font=('arial', 10, 'bold'), bd= 1,
            bg="#CCCCCC")
        b_dong_cua.place(x=20, y=100)
        dem_sai_mk += 1
        label_result.config(text=state_pass)
        label_result.update()
        led_buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_result.config(text=hidden_pass)  
        label_result.update()
        
        if dem_sai_mk == 3:
            label_result.config(text='Sai mật khẩu 3 lần')  
            label_result.update()
            led_buzzer_on(0.5,10)
            dem_sai_mk = 0
        trang_chu()
        time.sleep(1)
        
        
        
    
def trang_chu():
        global txt_pass, hidden_pass, pass_word
        hidden_pass = ""
        txt_pass = ''
        label_result.config(text="")
        label_matkhau.config(text='Mật khẩu')
        b_dong_cua = Label(top, text="", width=20, height=2,
            font=('arial', 10, 'bold'), bd= 1,
            bg="#CCCCCC")
        b_dong_cua.place(x=20, y=100)
        GPIO.output([led_state, buzzer_state, khoa_pin], [GPIO.LOW, GPIO.LOW, GPIO.LOW])
        
        back = Label(top, text='',width=13, height = 2 , bg="#CCCCCC").place(x=20, y=20)
        b0 = Button(top, text="0", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('0')).place(x=210, y=120) 
        b1 = Button(top, text="1", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('1')).place(x=260, y=120) 
        b2 = Button(top, text="2", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('2')).place(x=310, y=120) 

        b3 = Button(top, text="3", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('3')).place(x=210, y=170) 
        b4=Button(top, text="4", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('4')).place(x=260, y=170) 
        b5= Button(top, text="5", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('5')).place(x=310, y=170) 

        b6 = Button(top, text="6", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('6')).place(x=210, y=220) 
        b7 = Button(top, text="7", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('7')).place(x=260, y=220) 
        b8 = Button(top, text="8", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('8')).place(x=310, y=220) 

        b9 = Button(top, text="9", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: show('9')).place(x=210, y=270) 
        bca = Button(top, text="CA", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: clear_all()).place(x=260, y=270) 
        bc = Button(top, text="C", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5", command=lambda: clear()).place(x=310, y=270) 

        bxn = Button(top, text="Xác nhận", width=8, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#ff9001", command= lambda: xac_nhan()).place(x=240, y=330) 
        bq = Button(top, text="Quên mật khẩu", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239", command= lambda: quen_mat_khau()).place(x=205, y=400) 
        bd = Button(top, text="Đổi mật khẩu", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239", command= lambda: doi_mat_khau()).place(x=205, y=450) 
        b_van_tay = Button(top, text="Vân tay", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239", command= lambda: gui_van_tay()).place(x=205, y=500) 
        b_rfid = Button(top, text = 'Thẻ từ', width=15, height=2,
                font=('arial', 13, 'bold'),
                bd= 1, fg = "#fff",bg="#DA4239", command= lambda: gui_rfid())
        b_rfid.place(x=205, y = 550)
        
        b_add_rfid = Button(top, text = 'Thêm thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_add_rfid()).place(x=390, y=120) 
        b_remove_rfid = Button(top, text = 'Xóa thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_remove_rfid()).place(x=390, y=170)
        b_add_van_tay = Button(top, text = 'Thêm vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_add_van_tay()).place(x=390, y=220) 
        b_remove_van_tay = Button(top, text = 'Xóa vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_remove_van_tay()).place(x=390, y=270) 
    
def xac_nhan_mat_khau_moi():
    global txt_pass, txt_ccd_corect, pass_word, len_pass
    state_mk_moi = doi_mat_khau_moi(txt_pass, pass_word)
    label_matkhau.config(text='Mật khẩu mới')
    if state_mk_moi == True:
        data_mk = pd.read_csv('Mat_khau.csv')
        data_mk.loc[len(data_mk)] = txt_pass
        data_mk.to_csv('Mat_khau.csv', index=False)
        data_mk = pd.read_csv('Mat_khau.csv')
        pass_word = password(str(list(data_mk['Mật khẩu'])[-1]))
        len_pass = len(pass_word)
        label_result.config(text=pass_word)
        label_result.update()
        time.sleep(1)
        label_result.config(text='Thay đổi mật khẩu thành công')
        label_result.update()
        for i in range (0,3):
            GPIO.output(buzzer_state, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(buzzer_state, GPIO.LOW)
            time.sleep(0.2)
        time.sleep(1)
        trang_chu()
        
    else:
        label_result.config(text=state_mk_moi)
        label_result.update()
        time.sleep(1)
        hidden_pass = ""
        txt_pass = ""
        label_result.config(text=hidden_pass)
        label_result.update()

        
def cap_lai_mat_khau():
		global txt_pass, txt_ccd_corect, pass_word, len_pass
		state_cap_lai = cap_lai(txt_pass, txt_ccd_corect)
		if state_cap_lai == 'Sai CCCD' or state_cap_lai == 'Chỉ 13 ký tự':
			label_result.config(text='{}'.format(state_cap_lai))
		else:
			b0 = Button(top, text="0", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=120) 
			b1 = Button(top, text="1", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=120) 
			b2 = Button(top, text="2", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=120) 

			b3 = Button(top, text="3", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=170) 
			b4=Button(top, text="4", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=170) 
			b5= Button(top, text="5", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=170) 

			b6 = Button(top, text="6", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=220) 
			b7 = Button(top, text="7", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=220) 
			b8 = Button(top, text="8", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=220) 

			b9 = Button(top, text="9", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=210, y=270) 
			bca = Button(top, text="CA", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=260, y=270) 
			bc = Button(top, text="C", width=4, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#3697f5").place(x=310, y=270) 
			bq = Button(top, text="Xác nhận", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239").place(x=205, y=400) 
			label_matkhau.config(text = 'Mật khẩu')
			data_mk = pd.read_csv('Mat_khau.csv')
			data_mk.loc[len(data_mk)] = cap_lai(txt_pass, txt_ccd_corect)
			data_mk.to_csv('Mat_khau.csv', index=False)
			data_mk = pd.read_csv('Mat_khau.csv')
			pass_word = password(str(list(data_mk['Mật khẩu'])[-1]))
			len_pass = len(pass_word)
			label_result.config(text='{}'.format(pass_word))
			
        
def change_mat_khau_moi():
    global txt_pass, pass_word, hidden_pass
    label_matkhau.config(text = 'Nhập số CCCD')
    if check_cccd(txt_pass, txt_ccd_corect) == True:
        label_matkhau.config(text = 'Nhập mật khẩu mới')
        txt_pass = ""
        hidden_pass = ""
        label_result.config(text=txt_pass)
        Button(top, text="Xác nhận", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239",
               command= lambda: xac_nhan_mat_khau_moi()).place(x=205, y=400) 

    else:
        label_result.config(text=check_cccd(txt_pass, txt_ccd_corect))
        
def xac_nhan_mat_khau_cu ():
    global txt_pass, pass_word, hidden_pass, txt_ccd_corect
    state_mk_cu = check_pass_cu(txt_pass, pass_word)
    if state_mk_cu == True:
        label_result.config(text=state_mk_cu)
        txt_pass = ""
        hidden_pass = ""
        label_matkhau.config(text = 'Nhập số CCCD')
        label_result.config(text=hidden_pass)
        bq = Button(top, text="Xác nhận", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239", 
                    command= lambda: change_mat_khau_moi()).place(x=205, y=400) 
        back = Button(top, text='Trang chủ',  command= lambda: trang_chu()).place(x=20, y=20)
        bxn = Label(top, text="",  width=30, height=3, font=('arial', 13, 'bold'), bg='#CCCCCC').place(x=240, y=330) 
        
    else:
        label_result.config(text=state_mk_cu)
        label_result.update()
        time.sleep(1)
        txt_pass = ""
        hidden_pass = ""
        label_result.config(text=hidden_pass)
        label_result.update()
    
def quen_mat_khau():
    global txt_pass, pass_word, hidden_pass
    global bxn, b_van_tay, bd
    txt_pass = ""
    hidden_pass = ""
    label_matkhau.config(text = 'Nhập số CCCD')
    label_result.config(text=hidden_pass)
    bq = Button(top, text="Xác nhận", width=15, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#DA4239",
                command= lambda: cap_lai_mat_khau()).place(x=205, y=400) 
    back = Button(top, text='Trang chủ',  command= lambda: trang_chu()).place(x=20, y=20)
    bxn = Label(top, text="",  width=30, height=3, font=('arial', 13, 'bold'), bg='#CCCCCC').place(x=240, y=330) 

    b_van_tay = Label(top, text="", width=30, height=3, font=('arial', 13, 'bold'), bd= 1,bg="#CCCCCC").place(x=205, y=500)
    bd = Label(top, text="", width=30, height=3, font=('arial', 13, 'bold'), bd= 1, bg="#CCCCCC").place(x=205, y=450) 
    b_rfid = Label(top, text = '', width=30, height=3,font=('arial', 13, 'bold'), bd= 1, fg = "#CCCCCC", bg="#CCCCCC").place(x=205, y = 550)
    b_dong_cua = Label(top, text="", width=20, height=2,
            font=('arial', 10, 'bold'), bd= 1,
            bg="#CCCCCC")
    b_dong_cua.place(x=20, y=100)
    b_add_rfid = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=120) 
    b_remove_rfid = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=170) 
    b_add_van_tay = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=220) 
    b_remove_van_tay = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=270)

def doi_mat_khau():
    global txt_pass, pass_word, hidden_pass
    txt_pass = ""
    hidden_pass = ""
    label_matkhau.config(text = 'Mật khẩu cũ')
    label_result.config(text=hidden_pass)
    bq = Label(top, text = "", width=30, height=3, font=('arial', 10, 'bold'),bg="#CCCCCC").place(x=205, y=400) 
   
    back = Button(top, text='Trang chủ',  command= lambda: trang_chu()).place(x=20, y=20)
    bxn = Button(top, text="Xác nhận", width=8, height=2, font=('arial', 13, 'bold'), bd= 1, fg = "#fff",bg="#ff9001",
                 command= lambda: xac_nhan_mat_khau_cu()).place(x=240, y=330) 
    
    b_van_tay = Label(top, text="", width=30, height=3, font=('arial', 13, 'bold'), bd= 1,bg="#CCCCCC").place(x=205, y=500)
    bd = Label(top, text="", width=30, height=3, font=('arial', 13, 'bold'), bd= 1, bg="#CCCCCC").place(x=205, y=450) 
    b_rfid = Label(top, text = '', width=30, height=3,font=('arial', 13, 'bold'), bd= 1, fg = "#CCCCCC",bg="#CCCCCC").place(x=205, y = 550)
    b_add_rfid = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=120) 
    b_remove_rfid = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=170) 
    b_add_van_tay = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=220) 
    b_remove_van_tay = Label(top, text = '', width=30, height=2, font=('arial', 13, 'bold'), bd=1, fg = "#CCCCCC",bg="#CCCCCC").place(x=390, y=270)

def read_rfid_card():
	reader = MFRC522.MFRC522()
	start_time = time.time()

	while True:
		current_time = time.time()
		if current_time - start_time > 5:
			return('Đã hết thời gian chờ 5s')
			
		(status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)
		
		if status == reader.MI_OK:
			print('The da duoc phat hien')
			(status, TagType) = reader.MFRC522_Anticoll()
			# Doc ID
			
			# Kiem tra doc id thanh cong k
			if status == reader.MI_OK:
				read_id_test = SimpleMFRC522()
				id = read_id_test.read_id()
				print('ID: ', id)
				return id
        
		


def gui_rfid():
    global txt_pass, hidden_pass, dem_sai_mk
    txt_pass = ""
    hidden_pass = ""
    label_matkhau.config(text = 'Quét thẻ từ')
    
    label_result.config(text=hidden_pass)
    data_rfid = pd.read_csv('Data_RFID.csv')
    id = read_rfid_card() # doc id
    if id != 'Đã hết thời gian chờ 5s':
        state_check_rfid = check_rfid(id, data_rfid)
        if state_check_rfid == True:
            b_dong_cua = Button(top, text="Đóng cửa", width=10, height=1,
                font=('arial', 10, 'bold'), bd= 1,
                fg = "#fff",bg="#3697f5",
                command=lambda: dong_cua())
            b_dong_cua.place(x=20, y=100)
            dem_sai_mk = 0
            GPIO.output(led_state, GPIO.HIGH)
            GPIO.output(buzzer_state, GPIO.HIGH)
            GPIO.output(khoa_pin, GPIO.HIGH)
            label_result.config(text='Mở cửa thành công')
            label_result.update()
            time.sleep(2)
            hidden_pass = ""
            txt_pass = ""
            label_result.config(text='Mời bạn đóng cửa')
            GPIO.output(buzzer_state, GPIO.LOW)
            tat_phim()
        else:
            b_dong_cua = Label(top, text="", width=20, height=2,
                font=('arial', 10, 'bold'), bd= 1,
                bg="#CCCCCC")
            b_dong_cua.place(x=20, y=100)
            dem_sai_mk += 1
            label_result.config(text=state_check_rfid) # Sai the
            label_result.update()
            led_buzzer_on(0.5,3)
            hidden_pass = ""
            txt_pass = ""
            label_result.config(text=hidden_pass)  
            label_result.update()
            label_matkhau.config(text='Mật khẩu')
            label_matkhau.update()
            
            if dem_sai_mk == 3:
                 # Led nhay 3 lan
                label_result.config(text='Sai mật khẩu 3 lần')  
                label_result.update()
                led_buzzer_on(0.5,10)
                dem_sai_mk = 0
                trang_chu()
    else:
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
        label_result.config(text=id) # Đã hết thời gian choừ 5s
        label_result.update()
        led_buzzer_on(0.5,3)

        
							

    
def dong_cua():
    global hidden_pass, txt_pass
    b_dong_cua = Label(top, text="", width=20, height=2,
            font=('arial', 10, 'bold'), bd= 1,
            bg="#CCCCCC")
    b_dong_cua.place(x=20, y=100)
    back = Label(top, text='',width=15, height=2,
            font=('arial', 10, 'bold'), bd= 1,
            bg="#CCCCCC").place(x=20, y=20)
    
    txt_pass = ""
    hidden_pass = ""
    GPIO.output(khoa_pin, GPIO.LOW) #dong cua
    label_result.config(text='Đóng cửa thành công')
    label_result.update()
    GPIO.output(led_state, GPIO.LOW)
    buzzer_on(0.5,3)
    
    trang_chu()
   

def gui_add_rfid(): #
        global hidden_pass, txt_pass
        
        data_rfid = pd.read_csv('Data_RFID.csv')
        id_card = read_rfid_card()
        if id_card != 'Đã hết thời gian chờ 5s':
            
            if id_card not in list(data_rfid['ID']):
                list_id = list(data_rfid['ID'])
                list_id.append(id_card)
                data_rfid = pd.DataFrame({'ID':list_id})
                data_rfid.to_csv('Data_RFID.csv', index=False)
                label_result.config(text='Thêm thẻ thành công')
                label_result.update()
                led_buzzer_on(0.5, 1)
                hidden_pass = ""
                txt_pass = ""
                label_matkhau.config(text = 'Mật khẩu')
            
        
            else:
                label_result.config(text='Thêm thẻ không thành công')
                label_result.update()
                led_buzzer_on(0.5, 3)
                hidden_pass = ""
                txt_pass = ""
                label_matkhau.config(text = 'Mật khẩu')

        else:
            hidden_pass = ""
            txt_pass = ""
            label_matkhau.config(text = 'Mật khẩu')
            label_result.config(text=id_card) # Đã hết thời gian choừ 5s
            label_result.update()
            led_buzzer_on(0.5, 3)
            
            
        
            
def gui_remove_rfid(): #
        id_card = read_rfid_card()
        data_rfid = pd.read_csv('Data_RFID.csv')
        if id_card != 'Đã hết thời gian chờ 5s':
            
            if id_card in list(data_rfid['ID']):
                list_id = list(data_rfid['ID'])
                list_id.remove(id_card)
                data_rfid = pd.DataFrame({'ID':list_id})
                data_rfid.to_csv('Data_RFID.csv', index=False)
                label_result.config(text='Xóa thẻ thành công')
                label_result.update()
                led_buzzer_on(0.5, 1)
                txt_pass = ""
                hidden_pass = ""
                label_matkhau.config(text = 'Mật khẩu')
                
            else:
                label_result.config(text='Xóa thẻ không thành công')
                label_result.update()
                led_buzzer_on(0.5, 3)
                hidden_pass = ""
                txt_pass = ""
                label_matkhau.config(text = 'Mật khẩu')
        else:
            hidden_pass = ""
            txt_pass = ""
            label_matkhau.config(text = 'Mật khẩu')
            label_result.config(text=id_card) # Đã hết thời gian choừ 5s
            label_result.update()
            led_buzzer_on(0.5, 3)
            
def gui_van_tay():
    global hidden_pass, txt_pass, dem_sai_mk
    hidden_pass = ''
    txt_pass = ''
    label_matkhau.config(text = 'Vân tay')
    state_find_van_tay = find_van_tay()
    if state_find_van_tay == True:
        b_dong_cua = Button(top, text="Đóng cửa", width=10, height=1,
                font=('arial', 10, 'bold'), bd= 1,
                fg = "#fff",bg="#3697f5",
                command=lambda: dong_cua())
        b_dong_cua.place(x=20, y=100)
        dem_sai_mk = 0
        GPIO.output(led_state, GPIO.HIGH)
        GPIO.output(buzzer_state, GPIO.HIGH)
        GPIO.output(khoa_pin, GPIO.HIGH)
        label_result.config(text='Mở cửa thành công')
        label_result.update()
        time.sleep(2)
        hidden_pass = ""
        txt_pass = ""
        label_result.config(text='Mời bạn đóng cửa')
        GPIO.output(buzzer_state, GPIO.LOW)
        tat_phim()
    elif state_find_van_tay == 'Quá thời gian chờ 5s':
        label_result.config(text='Quá thời gian chờ 5s')
        label_result.update()
        led_buzzer_on(0.5,3)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
        
    else:
        b_dong_cua = Label(top, text="", width=20, height=2,
                font=('arial', 10, 'bold'), bd= 1,
                bg="#CCCCCC")
        b_dong_cua.place(x=20, y=100)
        dem_sai_mk += 1
        label_result.config(text='Sai vân tay') # Sai the
        label_result.update()
        led_buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_result.config(text=hidden_pass)  
        label_result.update()
        label_matkhau.config(text='Mật khẩu')
        label_matkhau.update()
        
        if dem_sai_mk == 3:
             # Led nhay 3 lan
            label_result.config(text='Sai mật khẩu 3 lần')  
            label_result.update()
            led_buzzer_on(0.5, 10)
            dem_sai_mk = 0
            trang_chu()
            
def gui_add_van_tay():
    global hidden_pass, txt_pass, dem_sai_mk
    state_save_van_tay = save_van_tay()
    if state_save_van_tay == True:
        label_result.config(text='Thêm thành công')
        label_result.update()
        led_buzzer_on(0.5, 1)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
    elif state_save_van_tay == 'Quá thời gian chờ 5s':
        label_result.config(text='Quá thời gian chờ 5s')
        label_result.update()
        led_buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
    else:
        label_result.config(text='Thêm không thành công')
        label_result.update()
        led_buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')

def gui_remove_van_tay():
    state_remove_van_tay = remove_van_tay()
    if state_remove_van_tay == True:
        label_result.config(text='Xóa thành công')
        label_result.update()
        led_buzzer_on(0.5, 1)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
    elif state_remove_van_tay == 'Quá thời gian chờ 5s':
        label_result.config(text='Quá thời gian chờ 5s')
        label_result.update()
        led_buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
    else:
        label_result.config(text='Xóa không thành công')
        label_result.update()
        buzzer_on(0.5, 3)
        hidden_pass = ""
        txt_pass = ""
        label_matkhau.config(text = 'Mật khẩu')
        
        
# bot telegram
def handle(msg):
    global txt_pass, label_result, pass_word, len_pass
    chat_id = msg['chat']['id'] # Receiving the message from telegram
    command = msg['text']   # Getting text from the message
    
    print ('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage (chat_id, str("Hi! MakerPro"))
        
    if command == '/menu':
        bot.sendMessage (chat_id, '/The_tu')
        bot.sendMessage(chat_id, '/Mk_ (_: Mật khẩu)')
        bot.sendMessage(chat_id, '/Dong_cua')
        bot.sendMessage(chat_id, '/Doi_mk_ (_: CCCD_Mật khẩu cũ_Mật khẩu mới)') #Doi_mk_1234567891011_12345678_123456789
        bot.sendMessage(chat_id, '/Quen_mk_ (_: CCCD)')
        bot.sendMessage(chat_id, '/Them_the')
        bot.sendMessage(chat_id, '/Xoa_the')
        bot.sendMessage(chat_id, '/Van_tay')
        bot.sendMessage(chat_id, '/Xoa_van_tay')
        bot.sendMessage(chat_id, '/Them_van_tay')


    if command == '/The_tu':
        state_activity = label_result.cget('text')
        if state_activity != 'Mời bạn đóng cửa':
            bot.sendMessage (chat_id, str("Quẹt thẻ"))
            gui_rfid()
            state_result = label_result.cget('text')
            if state_result == 'Mời bạn đóng cửa':
                bot.sendMessage (chat_id, str("Mở cửa thành công - Mời bạn đóng cửa"))
            elif state_result == 'Đã hết thời gian chờ 5s':
                bot.sendMessage (chat_id, 'Đã hết thời gian chờ 5s')
                time.sleep(1)
                trang_chu()
            else:
                bot.sendMessage (chat_id, 'Sai thẻ')
                time.sleep(1)
                trang_chu()
        else:
            bot.sendMessage (chat_id, str("Không thể quẹt thẻ"))

            
    if command[0:4] == '/Mk_' and len(command) >= 12:
        txt_pass = command[4:]
        state_activity = label_result.cget('text')
      
        if state_activity == '':
            xac_nhan()
            state_result = label_result.cget('text')
            if state_result == 'Mời bạn đóng cửa':
                bot.sendMessage (chat_id, str("Mở cửa thành công - Mời bạn đóng cửa"))
            else:
                bot.sendMessage (chat_id, str("Sai mật khẩu"))
        else:
            bot.sendMessage (chat_id, str("Không thể nhập mật khẩu"))
   
            
            
        
    if command == '/Dong_cua':
        state_activity = label_result.cget('text')
        if state_activity == 'Mời bạn đóng cửa':
            bot.sendMessage (chat_id, str("Đóng cửa thành công"))
            dong_cua()
        else:
            bot.sendMessage (chat_id, str("Không thể đóng cửa"))
            
           
    
    len_pass = len(pass_word)
    if command[0:8] == '/Doi_mk_' and len(command) >= 39 and command[7] == '_' and command[22: len_pass+22].isnumeric() == True and command[len_pass+22] == '_' and command[len_pass+22+1: ].isnumeric() == True and command[8:21] == '1234567891011': # /Doi_mk_1234567891011_12345678_123456789
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            if state_activity == '':
                if command[8:21] == '1234567891011': # CCCD
                    if command[22: len_pass+22] == pass_word: # pass cu
                        if command[22+len_pass+1:] != pass_word: # pass mới 
                            txt_pass = command[22+len_pass+1:]
                            data_mk = pd.read_csv('Mat_khau.csv')
                            data_mk.loc[len(data_mk)] = txt_pass
                            pass_word = password(str(list(data_mk['Mật khẩu'])[-1]))
                            len_pass = len(pass_word)
                            data_mk.to_csv('Mat_khau.csv', index=False)
                            label_result.config(text=pass_word)
                            label_result.update()
                            time.sleep(1)
                            label_result.config(text='Thay đổi mật khẩu thành công')
                            label_result.update()
                            time.sleep(1)
                            trang_chu()
                            bot.sendMessage (chat_id, str("Đổi mật khẩu thành công"))

                        elif command[22+len_pass+1:] == pass_word:
                            bot.sendMessage (chat_id, str("Trùng mật khẩu cũ"))
                            
                            
                        else:
                            bot.sendMessage (chat_id, str("Sai mật khẩu mới (>= 8 ký tự)"))
                            
                    else:
                        bot.sendMessage (chat_id, str("Sai mật khẩu cũ"))
                        
                else:
                    
                    bot.sendMessage (chat_id, str("Sai CCCD"))
            else:
                bot.sendMessage (chat_id, str("Không thể thực hiện"))
        else:
            bot.sendMessage (chat_id, str("Chỉ có chủ nhà thực hiện lệnh"))

            
           
    # /Quen_mk_1234567891011
    if command[0:9] == '/Quen_mk_' and command[9:].isnumeric() == True and len(command) == 22 :
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            txt_pass = command[9:]
            if state_activity == '':
                state_cap_lai = cap_lai(txt_pass, txt_ccd_corect)
                if state_cap_lai == 'Sai CCCD' or state_cap_lai == 'Chỉ 13 ký tự':
                    bot.sendMessage (chat_id, state_cap_lai)
                else:
                    data_mk = pd.read_csv('Mat_khau.csv')
                    data_mk.loc[len(data_mk)] = cap_lai(txt_pass, txt_ccd_corect)
                    data_mk.to_csv('Mat_khau.csv', index=False)
                    data_mk = pd.read_csv('Mat_khau.csv')
                    pass_word = password(str(list(data_mk['Mật khẩu'])[-1]))
                    len_pass = len(pass_word)
                    bot.sendMessage(chat_id, 'Cấp lại mật khẩu thành công')
                    bot.sendMessage(chat_id, 'Mật khẩu mới: {}'.format(pass_word))
                    time.sleep(1)

            else:

                bot.sendMessage (chat_id, str("Không thể thực hiện"))
                time.sleep(3)
        else:
            bot.sendMessage(chat_id, 'Chỉ có chủ nhà thực hiện lệnh')

        
    if command == '/Them_the':
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            if state_activity != 'Mời bạn đóng cửa': # Cửa đóng
                        bot.sendMessage(chat_id, str('Mời bạn cho thẻ'))
                        gui_add_rfid()
                        state_result = label_result.cget('text')
                        if state_result == 'Thêm thẻ thành công':
                            bot.sendMessage(chat_id, str('Thêm thẻ thành công'))
                            time.sleep(1)
                            trang_chu()
                        elif state_result == 'Thêm thẻ không thành công':
                            bot.sendMessage(chat_id, str('Thêm thẻ không thành công'))
                            time.sleep(1)
                            trang_chu()
                        else:
                            bot.sendMessage(chat_id, str('Quá thời gian chờ 5s'))
                        
            else:
                bot.sendMessage(chat_id, str('Không thể thực hiện'))
        else:
            bot.sendMessage(chat_id, 'Chỉ có chủ nhà thực hiện lệnh')

    
    if command == '/Xoa_the':
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            if state_activity != 'Mời bạn đóng cửa':
                        bot.sendMessage(chat_id, str('Mời bạn cho thẻ'))
                        gui_remove_rfid()
                        state_result = label_result.cget('text')
                        if state_result == 'Xóa thẻ thành công':
                            bot.sendMessage(chat_id, str('Xóa thẻ thành công'))
                            time.sleep(1)
                            trang_chu()
                        elif state_result == 'Xóa thẻ không thành công':
                            bot.sendMessage(chat_id, str('Xóa thẻ không thành công'))
                            time.sleep(1)
                            trang_chu()
                        else:
                            bot.sendMessage(chat_id, str('Quá thời gian chờ 5s'))
                        
            else:
                bot.sendMessage(chat_id, str('Không thể thực hiện'))
        else:
            bot.sendMessage(chat_id, 'Chỉ có chủ nhà thực hiện lệnh')
            
    if command == '/Van_tay':
        state_activity = label_result.cget('text')
        if state_activity != 'Mời bạn đóng cửa':
            bot.sendMessage (chat_id, str("Đặt vân tay"))
            gui_van_tay()
            state_result = label_result.cget('text')
            if state_result == 'Mời bạn đóng cửa':
                bot.sendMessage (chat_id, str("Mở cửa thành công - Mời bạn đóng cửa"))
            elif state_result == 'Quá thời gian chờ 5s':
                bot.sendMessage (chat_id, 'Quá thời gian chờ 5s')
                time.sleep(1)
                trang_chu()
            else:
                bot.sendMessage (chat_id, 'Sai vân tay')
                time.sleep(1)
                trang_chu()
        else:
            bot.sendMessage (chat_id, str("Không thể dùng vân tay"))
            
    if command == '/Xoa_van_tay':
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            if state_activity != 'Mời bạn đóng cửa':
                        bot.sendMessage(chat_id, str('Đặt vân tay'))
                        gui_remove_van_tay()
                        state_result = label_result.cget('text')
                        if state_result == 'Xóa thành công':
                            bot.sendMessage(chat_id, str('Xóa vân tay thành công'))
                            time.sleep(1)
                            trang_chu()
                        elif state_result == 'Xóa không thành công':
                            bot.sendMessage(chat_id, str('Xóa vân tay không thành công'))
                            time.sleep(1)
                            trang_chu()
                        else:
                            bot.sendMessage(chat_id, str('Quá thời gian chờ 5s'))
                        
            else:
                bot.sendMessage(chat_id, str('Không thể thực hiện'))
        else:
            bot.sendMessage(chat_id, 'Chỉ có chủ nhà thực hiện lệnh')
            
    if command == '/Them_van_tay':
        if chat_id == 6039829308:
            state_activity = label_result.cget('text')
            if state_activity != 'Mời bạn đóng cửa':
                        bot.sendMessage(chat_id, str('Đặt vân tay'))
                        gui_add_van_tay()
                        state_result = label_result.cget('text')
                        if state_result == 'Thêm thành công':
                            bot.sendMessage(chat_id, str('Thêm vân tay thành công'))
                            time.sleep(1)
                            trang_chu()
                        elif state_result == 'Thêm không thành công':
                            bot.sendMessage(chat_id, str('Thêm vân tay không thành công'))
                            time.sleep(1)
                            trang_chu()
                        else:
                            bot.sendMessage(chat_id, str('Quá thời gian chờ 5s'))
                        
            else:
                bot.sendMessage(chat_id, str('Không thể thực hiện'))
        else:
            bot.sendMessage(chat_id, 'Chỉ có chủ nhà thực hiện lệnh')
     
try:
    bot = telepot.Bot('7046872194:AAHuC8WJFF8x7QQcs_KJJn1Wt3kkMOZJ0sg')
    print (bot.getMe())

    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    MessageLoop(bot, handle).run_as_thread()
    print ('Listening....')
except:
    pass
    
# Main
top = Tk()

top.title('Window 1')
top.geometry('570x700+100+200')
top.resizable(False, False)
label_matkhau = Label(top, text='Mật khẩu', font=('Times New Roman', 16))
label_matkhau.pack(side='top', pady= 10)
top.config(bg='#CCCCCC')


label_result = Label(top, width=25, height=2, text="", font= ('arial', 15))
label_result.pack()

GPIO.output([led_state, buzzer_state, khoa_pin], [GPIO.LOW, GPIO.LOW, GPIO.LOW])

b0 = Button(top, text="0", width=4, height=2,
            font=('arial', 13, 'bold'), bd= 1,
            fg = "#fff",bg="#3697f5",
            command=lambda: show('0'))
b0.place(x=210, y=120) 

b1 = Button(top, text="1", width=4, height=2,
            font=('arial', 13, 'bold'), bd= 1,
            fg = "#fff",bg="#3697f5",
            command=lambda: show('1'))
b1.place(x=260, y=120) 

b2 = Button(top, text="2", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('2'))
b2.place(x=310, y=120) 

b3 = Button(top, text="3", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('3'))
b3.place(x=210, y=170)
 
b4=Button(top, text="4", width=4, height=2,
          font=('arial', 13, 'bold'),
          bd= 1, fg = "#fff",bg="#3697f5",
          command=lambda: show('4'))
b4.place(x=260, y=170) 

b5= Button(top, text="5", width=4, height=2,
           font=('arial', 13, 'bold'),
           bd= 1, fg = "#fff",bg="#3697f5",
           command=lambda: show('5'))
b5.place(x=310, y=170) 

b6 = Button(top, text="6", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('6'))
b6.place(x=210, y=220) 

b7 = Button(top, text="7", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('7'))
b7.place(x=260, y=220) 

b8 = Button(top, text="8", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('8'))
b8.place(x=310, y=220) 

b9 = Button(top, text="9", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: show('9'))
b9.place(x=210, y=270) 

bca = Button(top, text="CA", width=4, height=2,
             font=('arial', 13, 'bold'),
             bd= 1, fg = "#fff",bg="#3697f5",
             command=lambda: clear_all())

bca.place(x=260, y=270)
 
bc = Button(top, text="C", width=4, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#3697f5",
            command=lambda: clear())
bc.place(x=310, y=270) 

bxn = Button(top, text="Xác nhận", width=8, height=2,
             font=('arial', 13, 'bold'),
             bd= 1, fg = "#fff",bg="#ff9001",
             command= lambda: xac_nhan())
bxn.place(x=240, y=330) 

bq = Button(top, text="Quên mật khẩu", width=15, height=2,
            font=('arial', 13, 'bold'),
            bd= 1, fg = "#fff",bg="#DA4239",
            command= lambda: quen_mat_khau())
bq.place(x=205, y=400) 

bd = Button(top, text="Đổi mật khẩu", width=15, height=2,
            font=('arial', 13, 'bold'), bd= 1,
            fg = "#fff",bg="#DA4239",
            command= lambda: doi_mat_khau())
bd.place(x=205, y=450) 

b_van_tay = Button(top, text="Vân tay", width=15, height=2,
                   font=('arial', 13, 'bold'),
                   bd= 1, fg = "#fff",bg="#DA4239", command = lambda: gui_van_tay())

b_van_tay.place(x=205, y=500) 


b_rfid = Button(top, text = 'Thẻ từ', width=15, height=2,
                font=('arial', 13, 'bold'),
                bd= 1, fg = "#fff",bg="#DA4239", command= lambda: gui_rfid())
b_rfid.place(x=205, y = 550)

b_add_rfid = Button(top, text = 'Thêm thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_add_rfid()).place(x=390, y=120) 
b_remove_rfid = Button(top, text = 'Xóa thẻ từ', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_remove_rfid()).place(x=390, y=170) 
b_add_van_tay = Button(top, text = 'Thêm vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_add_van_tay()).place(x=390, y=220) 
b_remove_van_tay = Button(top, text = 'Xóa vân tay', width=10, height=1, font=('arial', 13, 'bold'), bd=1, fg = "#fff",bg="#DA4239", command=lambda: gui_remove_van_tay()).place(x=390, y=270) 

top.mainloop()
