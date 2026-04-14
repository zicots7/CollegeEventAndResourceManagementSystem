from django.urls import path
from. views import (
resourceAdd,
resourceUpdate,
resourceList,
resourceDelete,
)
urlpatterns = [
    path('resourceAdd/',resourceAdd,name='resourceAdd'),
    path('resourceUpdate/<int:id>',resourceUpdate,name='resourceUpdate'),
    path('resourceDelete/<int:id>/',resourceDelete,name='resourceDelete'),
    path('resourceList/',resourceList,name='resourceList'),
]