from django.shortcuts import render,redirect
from resources.models import Resource
from resources.mongoDB import collection
from user.decorators import(
role_required
)
@role_required(allowed_roles=['Student','Admin','Faculty'])
def download(request,id):
    resource =  Resource.objects.get(id=id)
    resource.download_count+=1
    resource.save()
    mongo_doc = collection.find_one({"resource_id": id})or {}
    file_url = mongo_doc.get('file_url')
    return redirect(file_url)
