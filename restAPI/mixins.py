from django.http import HttpResponse
from django.core.serializers import serialize
import json
from django.shortcuts import render
class HttpResponseMixin(object):
    def render_to_Http_response(self,json_data,status=200):
        return HttpResponse(json_data,content_type='application/json',status=status)

class SerializerMixin(object):
    def serializermix(self,dataval):
        json_data = serialize('json', [dataval,], fields={'emp_name',"emp_address" ,'emp_salary'})
        print("Ye json_data hai serializemixin se :",type(json_data))

        p_dict = json.loads(json_data)
        print(p_dict)
        print("Ye p_dict ka type :",type(p_dict))
        final_view = []
        for obj in p_dict:
            emp_dataview = obj['fields']
            print("Ye bahinchod hai :",emp_dataview)
            final_view.append(emp_dataview)
        json_data = json.dumps(final_view)
        return json_data