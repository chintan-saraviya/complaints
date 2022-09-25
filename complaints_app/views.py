from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from complaints_app.models import Complaint
from complaints_app.serializers import ComplaintSerializer
from xlutils.copy import copy  # http://pypi.python.org/pypi/xlutils
from xlrd import open_workbook  # http://pypi.python.org/pypi/xlrd
import xlwt
from django.http import HttpResponse
import os

# Create your views here.


class Register(APIView):
    # API view to register a user simply by asking username and password
    def post(self, request):
        try:
            data = self.request.data['data']
            user, created = User.objects.get_or_create(username=data['username'])
            user.set_password(data['password'])
            user.save()
            token, _ = Token.objects.get_or_create(user)
            return Response({"success": True, "token": token.key}, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({"success": False, "message": error.__str__()}, status=status.HTTP_400_BAD_REQUEST)


class ComplaintsView(ListCreateAPIView):
    # API View to make a new complaint and list all complaints
    permission_classes = [IsAuthenticated, ]
    serializer_class = ComplaintSerializer
    renderer_classes = [JSONRenderer, ]
    queryset = Complaint.objects.all()


class ComplaintView(RetrieveUpdateAPIView):
    # API View to track status of and to update individual complaints
    permission_classes = [IsAuthenticated, ]
    serializer_class = ComplaintSerializer
    renderer_classes = [JSONRenderer, ]
    queryset = Complaint.objects.all()


# excel_app/views.py
def export_write_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    # EG: path = excel_app/sample.xls
    path = os.path.dirname(__file__)
    file = os.path.join(path, 'sample.xls')

    rb = open_workbook(file, formatting_info=True)
    r_sheet = rb.sheet_by_index(0)

    wb = copy(rb)
    ws = wb.get_sheet(0)

    row_num = 2  # index start from 0
    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])

    # wb.save(file) # will replace original file
    # wb.save(file + '.out' + os.path.splitext(file)[-1]) # will save file where the excel file is
    wb.save(response)
    return response