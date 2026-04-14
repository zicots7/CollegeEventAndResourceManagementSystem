from django.urls import path
from user.views import(
AddFaculty,
AddStudent,
userLogin,
userLogout,
faculty_list,
student_list,
EditStudent,
EditFaculty,
DeleteStudent,
DeleteFaculty
)
urlpatterns = [
    path('', userLogin, name='userLogin'),
    path('EditStudent/<int:id>/',EditStudent,name='EditStudent'),
    path('DeleteStudent/<int:id>/',DeleteStudent,name='DeleteStudent'),
    path('AddStudent/',AddStudent,name='AddStudent'),
    path('AddFaculty/',AddFaculty,name='AddFaculty'),
    path('EditFaculty/<int:id>/',EditFaculty,name='EditFaculty'),
    path('DeleteFaculty/<int:id>/',DeleteFaculty,name='DeleteFaculty'),
    path('userLogout/',userLogout,name='userLogout'),
    path('faculty_list/',faculty_list,name='faculty_list'),
    path('student_list/', student_list, name='student_list'),

]