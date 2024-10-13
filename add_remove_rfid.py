import pandas as pd
from read_rfid import read_rfid_card


	data_rfid = pd.read_csv('/home/lappc/Do_an_chuyen_nganh/Data_RFID.csv')
	id,text = read_rfid_card()
if id not in list(data_rfid['ID']):
	list_id = list(data_rfid['ID'])
	list_id.append(id)
	data_rfid = pd.DataFrame({'ID':list_id})
	data_rfid.to_csv('Data_RFID.csv', index=False)
	return True
else:
	return False

def remove_rfid():
	data_rfid = pd.read_csv('/home/lappc/Do_an_chuyen_nganh/Data_RFID.csv')
    id,text = read_rfid_card()
    if id in data_rfid['ID']:
		list_id = list(data_rfid['ID'])
		list_id.remove(id)
		data_rfid = pd.DataFrame({'ID':list_id})
        data_rfid.to_csv('Data_RFID.csv', index=False)
        return True
    else:
        return False

