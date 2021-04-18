from django.contrib import admin
from restAPI.models import Employee,Country,State,District
from .models import User,UserOTP
# Register your models here.


admin.site.register(User)
class UserOTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'otp', 'time')
admin.site.register(UserOTP,UserOTPAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id','emp_name','emp_address','emp_salary')
admin.site.register(Employee,EmployeeAdmin)



admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)




