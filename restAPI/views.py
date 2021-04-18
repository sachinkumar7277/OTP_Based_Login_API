from django.shortcuts import render,redirect
from restAPI.mixins import HttpResponseMixin
from django.http import HttpResponse,JsonResponse
import json
from restAPI.utils import is_json
from restAPI.models import Employee,Country,District,State,UserOTP,User
from django.views.generic import View
from twilio.rest import Client
import random
import requests
from decouple import config

from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
# Create your views here.


from django.core.serializers import serialize
from restAPI.mixins import SerializerMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



def index(request):


    return render(request,'index2.html')


def Validate_otp(otp,phone):
    """ Using API TO VALIDATE OTP AND AUTHENTICATE USER TO LOGIN """
    BASE_URL = "http://127.0.0.1:8000/"
    END_POINT = "login_otp_api/"
    #****************************************************************
    print("Mai call ho chuka hu ")
    data = {'otp':otp,'phone':phone }
    respon = requests.post(BASE_URL+END_POINT,data =json.dumps(data))
    print(respon.json())
    return int(respon.status_code)




def Validate(request,phone):
    if request.method == 'POST':
        otp = request.POST.get('otp_sent')
        print(otp)
        print(phone)
        status = Validate_otp(otp,phone)
        if status == 200:
            user = User.objects.get(phone=phone)
            print(user)
            login(request,user)

    return redirect('/')



def generate_otp(phone_number):
    """ Using API TO GENERATE OTP  """
    BASE_URL ="http://127.0.0.1:8000/"
    END_POINT = "login_otp_api/"

    data = {'phone': phone_number}
    respo = requests.get(BASE_URL+END_POINT,data =json.dumps(data))
    print(respo.status_code)
    otp = respo.json()
    return otp

def login_OTP_request(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        print(type(phone_number))
        OTP_Gen = generate_otp(phone_number)
        print("Ye otp hai : ",OTP_Gen)
        if OTP_Gen is not None :
            return render(request, 'Validate_otp.html',{'phone':phone_number})

    return render(request, 'login_using_otp.html')


def register(request):
   if request.method =='POST':

      username = request.POST['Username']
      email = request.POST['email']
      password1 = request.POST['Password']
      password2 = request.POST['Confirm Password']
      phone = request.POST['phone']
      if  password1 == password2 :
          print("Password matched")
          if   User.objects.filter(username=username).exists():
               print("USERNAME EXIXT")
               messages.info(request,'username already taken')
               return redirect('register')
          elif User.objects.filter(email=email).exists():
               print("Email alreadt taken ")
               messages.info(request,'Email id  already taken try with another email id')
               return redirect('register')
          else:
               print("creating user now ")
               user = User.objects.create_user(username=username,email=email,password=password1,phone = phone)
               user.save()
               return redirect('login')
   else:
      return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/')


# *************************************************  Defining LOGIN API CLASS BASED VIEWS                 ******************************************************8


@method_decorator(csrf_exempt,name='dispatch')
class Login_OTP(SerializerMixin,HttpResponseMixin,View):

    def send_otp(self, phone,*args,**kwargs):
        OTP = random.randint(999,9999)
        print(OTP)
        user = User.objects.get(phone = phone)
        print(user)
        """
        Acount_sid = config('YOUR_Acount_sid')
        auth_token = config('YOUR_auth_token')
        client = Client(Acount_sid, auth_token)

        message = client.messages \
            .create(
            body="Your One Time Password is {} Please do not share your OTP with Any one ".format(OTP),
            to='+91{}'.format(phone),
            from_=config('YOUR_TWILLIO_NUMBER'),
        )
        print(message)
        print(message.sid)
        
        """

        UserOTP.objects.create(user = user,otp = OTP).save()

        return OTP


    def get(self,request,*args,**kwargs):
        data = request.body

        valid_json_data = is_json(data)
        if not valid_json_data:
            json_data = json.dumps({'msg': "this is not valid json data "})
            return self.render_to_Http_response(json_data, status=400)
        dict_data = json.loads(data)


        get_otp = self.send_otp(dict_data['phone'])

        if get_otp is not None:
            return  self.render_to_Http_response(json.dumps(get_otp),status=200)
        else:
            json_data = json.dumps({'msg': "this is not valid json data "})
            return self.render_to_Http_response(json_data, status=400)

    @csrf_exempt
    def post(self,request,*args,**kwargs):
        data = request.body

        valid_json_data = is_json(data)
        if not valid_json_data:
            json_data = json.dumps({'msg': "this is not valid json data "})
            return self.render_to_Http_response(json_data, status=400)
        dict_data = json.loads(data)
        print("Yaha tak sb sahi hai ")
        user_ph = User.objects.get(phone = dict_data['phone'])

        userotp = UserOTP.objects.all().filter(user=user_ph).last()

        print("Ye userotp ka object hai : ",userotp.otp)
        print("Otp ka value jo request se aaya ha  ",dict_data['otp'])

        if userotp.otp == int(dict_data['otp']):
            json_data = json.dumps({'msg': "Mobile no. validated "})
            return self.render_to_Http_response(json_data, status=200)
        else:
            json_data = json.dumps({'msg': "this is Wrong otp "})
            return self.render_to_Http_response(json_data, status=400)




# *************************************************                   ******************************************************8
"""


def search(request):
    country = Country.objects.all()
    return render(request,'index.html',{'country':country})


def States(request):
    country_id = request.GET.get('country')
    print("selected country is ",country_id)
    state = State.objects.filter(country_id = country_id).order_by('name')
    return render(request,'load_country.html',{'states':state})

def Districts(request):
    state_id = request.GET.get('state')
    print("selected state is ",state_id)
    state = District.objects.filter(state_id = state_id).order_by('name')
    return render(request,'load_country.html',{'states':state})


def emp_data_view(request):
    emp_data =  {
        'emp_id':190494,
        'emp_name': 'sachin' ,
        'emp_salary': 30000
    }
    respo = '<h1> Employye id : {} <br>  Employee Name : {}  <br> Employee Salary : {} </h1>'.format(emp_data['emp_id'],emp_data['emp_name'],emp_data['emp_salary'])
    return HttpResponse(respo)


def emp_data_Json_view(request):
    emp_data =  {
        'emp_id':190494,
        'emp_name': 'sachin',
        'emp_salary': 30000
    }
    json_data = json.dumps(emp_data)
    return HttpResponse(json_data,content_type='application/json')

def emp_data_JsonRESPO_view(request):
    emp_data =  {
        'emp_id':190494,
        'emp_name': 'sachin' ,
        'emp_salary': 30000
    }
    # json_data = json.dumps(emp_data) not needed becaause JsonResponse() is doing the task of json.dumps here in the next line
    return JsonResponse(emp_data)

# Now FOCUS ON Class based view we go with class based view for production level

# class JsonCBV(View):
#
#     def get(self,request,*args,**kwargs):
#         emp_data = {
#             'emp_id': 190494,
#             'emp_name': 'sachin',
#             'emp_salary': 30000
#         }
#
#         return JsonResponse(emp_data)

class JsonCBV(HttpResponseMixin,View):

    def get(self,request,id,*args,**kwargs):           # Retrive
        dataval = Employee.objects.get(id = id)
        print(type(dataval))
        data = {
            'emp_name': dataval.emp_name,
            'emp_address': dataval.emp_address,
            'emp_salary':dataval.emp_salary
            }
        json_data = json.dumps(data)
        return self.render_to_Http_response(json_data)
    def post(self,request,id,*args,**kwargs):          # C   :- Create
        data = request.body

        valid_json_data = is_json(data)
        if not valid_json_data:
            json_data = json.dumps({'msg': "this is not valid json data "})
            return self.render_to_Http_response(json_data,status=400)
        Employee_data = json.loads(data)
        print("Ye Employee kadata hai through Api aaya hai : ",Employee_data)
        forms = EmployeeForms(Employee_data)
        print(forms)
        if forms.is_valid():
            forms.save(commit=True)
            json_data = json.dumps({'msg':"Resource dreated successfully"})
            return self.render_to_Http_response(json_data,status=200)
        if forms.errors:
            json_data = json.dumps({'msg': "Resource created successfully"})
            return self.render_to_Http_response(json_data, status=400)

        data = {
            'emp_name': dataval.emp_name,
            'emp_address': dataval.emp_address,
            'emp_salary': dataval.emp_salary
        }
        json_data = json.dumps(data)
        return self.render_to_Http_response(json_data)
    def put(self,request,id,*args,**kwargs):
        dataval = Employee.objects.get(id=id)
        print(type(dataval))
        data = {'emp_name': dataval.emp_name,
                'emp_address': dataval.emp_address,
                'emp_salary': dataval.emp_salary}
        json_data = json.dumps(data)
        return self.render_to_Http_response(json_data)
    def delete(self,request,id,*args,**kwargs):
        dataval = Employee.objects.filter(id = id).delete()
        print(type(dataval))
        data = {'emp_name': dataval.emp_name,
                'emp_address': dataval.emp_address,
                'emp_salary': dataval.emp_salary}
        json_data = json.dumps({'msg': 'deleted '})
        return self.render_to_Http_response(json_data)


from django.core.serializers import serialize
from restAPI.mixins import SerializerMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt,name='dispatch')
class serializerapi(SerializerMixin,HttpResponseMixin,View):

    def get(self,request,id,*args,**kwargs):
        try:
            dataval = Employee.objects.get(id =id)
        except Employee.DoesNotExist:
            json_data = json.dumps({'msg':' Requested id:{} doesnot exist try with some other id '.format(id)})
            return self.render_to_Http_response(json_data,status = 404)
        else:
            json_data = self.serializermix(dataval)
            return self.render_to_Http_response(json_data,status = 200)
    @csrf_exempt
    def post(self, request, *args, **kwargs):  # C   :- Create
        data = request.body
        print(data)
        valid_json_data = is_json(data)
        if not valid_json_data:
            json_data = json.dumps({'msg': "this is not valid json data "})
            return self.render_to_Http_response(json_data, status=400)
        Employee_data = json.loads(data)
        print("Ye Employee kadata hai through Api aaya hai : ", Employee_data)
        forms = EmployeeForms(Employee_data)
        print(forms)
        if forms.is_valid():
            forms.save(commit=True)
            json_data = json.dumps({'msg': "Resource created successfully"})
            return self.render_to_Http_response(json_data, status=200)
        if forms.errors:
            json_data = json.dumps({'msg': "Resource not created try with valid json data "})
            return self.render_to_Http_response(json_data, status=400)

"""

