from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .serializers import houseOwnerSerializer
from .serializers import wardsSerializer
from .serializers import slotBookingSerializer
from .serializers import bookingStatusSerializer
from .models import houseowner
from .models import wards
from .models import slotbooking

import jwt, datetime
from django.db import connection


@api_view(['POST'])
def postHouseOwner(request):
    serializer = houseOwnerSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['GET'])
def getWards(request):
    wardsList = wards.objects.all()
    serializer = wardsSerializer(wardsList, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def postHouseOwnerlogin(request):
    data_email = request.data['email']
    data_password = request.data['password']

    user = houseowner.objects.filter(email = data_email).first()

    if user is None:
        raise AuthenticationFailed('User not found')
    if not user.check_password(data_password):
        raise AuthenticationFailed('Incorrect password')
    payload = {
        'id':user.id,
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
        'iat':datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret',algorithm='HS256')
    response =  Response()
    response.set_cookie(key = 'jwt',value=token, httponly=True)
    response.data = {'jwt': token,'status':1}
    # response.headers = {'jwt': token}
    return response

@api_view(['POST'])
def postLogoutView(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {'message': 'Successfully logged out','status':1}
    return response

# @api_view(['GET'])
# def getUserView(request):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token,'secret',algorithms=['HS256'])
#     except jwt.ExpiredSignatureError :
#         raise AuthenticationFailed('Unauthenticated!')

#     user = houseowner.objects.filter(id = payload['id'])
#     serializer = houseOwnerSerializer(user,many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def postSlotBooking(request):
    token = request.data.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    
    ho_id = payload['id']
    print(ho_id)

    waste_id = request.data['waste_id']
    print(waste_id)
    collection_date = request.data['collection_date']
    print(collection_date)
    booking_date = request.data['booking_date']
    print(booking_date)

    data ={'houseowner_id':ho_id,'waste_id':waste_id,'collection_date':collection_date,'booking_date':booking_date}
   
    serializer = slotBookingSerializer(data = data)

    if(serializer.is_valid()):
        serializer.save()
        data_1 = {'collected_date':collection_date,'slot_id':serializer.data['id']}
        serializer_1 = bookingStatusSerializer(data = data_1)
        if(serializer_1.is_valid()):
            serializer_1.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['GET'])
def getBookingHistory(request):
    token = request.data.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    ho_id = payload['id']

    cursor = connection.cursor()
    cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_slotbooking.collection_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.wastecollector_id from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id where houseownerapp_slotbooking.houseowner_id_id = %s",[ho_id])

    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}

        singleitem["Booked Date"]=item[0]
        singleitem["Collected Date"]=item[1]
        singleitem["Waste Type"]=item[2]
        singleitem["Collector ID"]=item[3]

        final_list.append(singleitem)

    return Response(final_list)

@api_view(['GET'])
def getBookingStatus(request):
    token = request.data.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    ho_id = payload['id']

    cursor = connection.cursor()
    cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_slotbooking.collection_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.status from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status != %s",[ho_id,"collected"])

    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}

        singleitem["Booked Date"]=item[0]
        singleitem["Collected Date"]=item[1]
        singleitem["Waste Type"]=item[2]
        singleitem["Status"]=item[3]

        final_list.append(singleitem)

    return Response(final_list)
