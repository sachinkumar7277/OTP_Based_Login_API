import requests
import json
"""
BASE_URL ="http://127.0.0.1:8000/"
END_POINT = "serialapi/"

def get_all_resource():
    respo = requests.get(BASE_URL + END_POINT)
    print(respo.status_code)
    print(respo.json())

def get_resources(id):
    respo = requests.get(BASE_URL + END_POINT+id+'/')
    print(respo.status_code)
    print(respo.json())

def create_resource():
    new_data ={

        'emp_name':input('Employee name : '),
        'emp_address':input("emp_address : "),
        'branch': input("branch_ame : "),
        'emp_salary':input("emp_salary : ")
    }
    respo = requests.post(BASE_URL + END_POINT,data=json.dumps(new_data))
    print(respo.status_code)
    print(respo.json())

#create_resource()



print("Here We are fetching data from Django app to python program")
# print('*'*30)
# print(Data)
# print(respo.text)
id = input('Enter Id of Employee:  ')
get_resources(id)

"""
def generate_otp():

    BASE_URL ="http://127.0.0.1:8000/"
    END_POINT = "otpapi/"

    phone_number = input("Enter phone number : ")
    data = {'phone': phone_number}
    respo = requests.get(BASE_URL+END_POINT,data =json.dumps(data))
    otp = respo.json()
    print(otp)

def Validate_otp():

    BASE_URL = "http://127.0.0.1:8000/"
    END_POINT = "otpapi/"

    phone_number = input("Enter phone number : ")
    otp = int(input('Enter OTP'))
    data = {'otp':otp,'phone':phone_number }
    respon = requests.post(BASE_URL+END_POINT,data =json.dumps(data))
    print(respon.json())

generate_otp()

Validate_otp()