from django.urls import path, include
from complaints_app.views import *

urlpatterns = [
    path('api/complaints/', ComplaintsView.as_view(), name='complaints'),
    path('api/complaint/', ComplaintView.as_view(), name='complaint'),
]