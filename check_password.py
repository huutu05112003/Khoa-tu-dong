import random 
import pandas as pd

def password(last_pass_csv):
    return last_pass_csv
    


def check_pass(input_pass, pass_word):
    
    if len(input_pass) < 8:
        return 'Không đủ 8 ký tự'
    else:
        if input_pass == pass_word:
            return True
        else:
            return 'Sai mật khẩu'

def cap_lai(txt_cccd, txt_ccd_corect):
    if len(txt_cccd) == 13:
        if txt_cccd == txt_ccd_corect:
            pass_word = random.randint(10000000, 99999999)
            
            return str(pass_word)
        else:
            return 'Sai CCCD'
    else:
        return 'Chỉ 13 ký tự'

def check_pass_cu(txt_pass, pass_word):
    if len(txt_pass) < 8:
        return 'Không đủ 8 ký tự'
    else:
        if txt_pass == pass_word:
            return True
        else:
            return 'Sai mật khẩu cũ'

def doi_mat_khau_moi(txt_pass, pass_word):
    if len(txt_pass) < 8:
        return 'Không đủ 8 ký tự'
    elif txt_pass[0] == '0':
        return 'Không được bắt đầu "0"'
    else:
        if txt_pass == pass_word:
            return 'Trùng mật khẩu cũ'
        else:
            return True

def check_cccd(txt_cccd, txt_cccd_correct):
    if len(txt_cccd) == 13:
        if txt_cccd == txt_cccd_correct:
            return True
        else:
            return 'Sai CCCD'
    else:
        return 'Chỉ 13 ký tự'
        
def check_rfid(txt_rfid, data_rfid):
    if txt_rfid in list(data_rfid['ID']):
        return True
    else:
        return 'Sai the'
        
