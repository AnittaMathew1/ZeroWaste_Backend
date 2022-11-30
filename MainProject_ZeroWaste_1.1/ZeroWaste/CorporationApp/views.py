from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.db import connection

from .serializers import wasteSerializer
from .models import wastes
import HouseOwnerApp.models as ho_models
import HouseOwnerApp.serializers as ho_serializers


@api_view(['GET'])
def getWastes(request):
    wasteList = wastes.objects.all()
    serializer = wasteSerializer(wasteList, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def postCorporationlogin(request):
    data_username = request.data['username']
    data_password = request.data['password']

    if data_username!="admin":
        raise AuthenticationFailed('User not found')
    if data_password!="admin":
        raise AuthenticationFailed('Incorrect password')
    # payload = {
    #     'id':"admin",
    #     'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
    #     'iat':datetime.datetime.utcnow()
    # }

    # token = jwt.encode(payload, 'secret',algorithm='HS256')
    response =  Response()
    # response.set_cookie(key = 'jwt',value=token, httponly=True)
    response.data = {'status':1}
    return response

@api_view(['POST'])
def postLogoutView(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {'message': 'Successfully logged out','status':1}
    return response

@api_view(['GET'])
def getBookingReport(request):
    # token = request.COOKIES.get('jwt')
    # if not token:
    #     raise AuthenticationFailed('Unauthenticated!')
    # try:
    #     payload = jwt.decode(token,'secret',algorithms=['HS256'])
    # except jwt.ExpiredSignatureError :
    #     raise AuthenticationFailed('Unauthenticated!')
    cursor = connection.cursor()
    cursor.execute("SELECT houseownerapp_houseowner.firstname,houseownerapp_houseowner.lastname,houseownerapp_houseowner.address,houseownerapp_houseowner.phoneno,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.wastecollector_id,houseownerapp_bookingstatus.status from houseownerapp_houseowner inner join houseownerapp_slotbooking on houseownerapp_houseowner.id = houseownerapp_slotbooking.houseowner_id_id inner join corporationapp_wastes on houseownerapp_slotbooking.waste_id_id = corporationapp_wastes.id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id")
    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}
        singleitem["firstname"]=item[0]
        singleitem["lastname"]=item[1]
        singleitem["address"]=item[2]
        singleitem["phoneno"]=item[3]
        singleitem["wastetype"]=item[4]
        singleitem["collectorid"]=item[5]
        singleitem["status"]=item[6]

        final_list.append(singleitem)

    return Response(final_list)

# @api_view(['POST'])
# def postBookingReport(request):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token,'secret',algorithms=['HS256'])
#     except jwt.ExpiredSignatureError :
#         raise AuthenticationFailed('Unauthenticated!')
    
#     ward_no = request.data['ward_no']
#     collection_date = request.data['collection_date']

#     cursor = connection.cursor()
#     cursor.execute("SELECT houseownerapp_houseowner.firstname,houseownerapp_houseowner.lastname,houseownerapp_houseowner.address,houseownerapp_houseowner.phoneno,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.wastecollector_id,houseownerapp_bookingstatus.status from houseownerapp_houseowner inner join houseownerapp_slotbooking on houseownerapp_houseowner.id = houseownerapp_slotbooking.houseowner_id_id inner join corporationapp_wastes on houseownerapp_slotbooking.waste_id_id = corporationapp_wastes.id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id where houseownerapp_houseowner.wardno_id = %s and houseownerapp_slotbooking.collection_date = %s",[ward_no,collection_date])
#     result = cursor.fetchall()

#     final_list=[]

#     for item in result:

#         singleitem={}
#         singleitem["First Name"]=item[0]
#         singleitem["Last Name"]=item[1]
#         singleitem["Address"]=item[2]
#         singleitem["Phone no"]=item[3]
#         singleitem["Waste type"]=item[4]
#         singleitem["Collector Id"]=item[5]
#         singleitem["Booking status"]=item[6]

#         final_list.append(singleitem)

#     return Response(final_list)