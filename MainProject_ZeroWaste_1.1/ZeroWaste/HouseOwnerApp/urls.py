from .import views
from django.urls import path

urlpatterns = [

    path('houseowner/signup/',views.postHouseOwner,name = 'signup'),
    path('wards/',views.getWards,name = 'wards'),
    path('houseowner/login/',views.postHouseOwnerlogin,name = 'login'),
    path('houseowner/logout/',views.postLogoutView,name = 'logout'),
    # path('user/',views.getUserView),
    path('houseowner/slotbooking/',views.postSlotBooking, name='slotbooking'),
    path('houseowner/bookinghistory/',views.getBookingHistory, name='bookinghistory'),
    path('houseowner/bookingstatus/',views.getBookingStatus, name='bookingstatus'),

]