from django.shortcuts import render,redirect
from user.decorators import role_required
from .models import Resource
from .form import ResourceForm
from django.contrib import messages
from .mongoDB import collection
from datetime import datetime
import uuid
from .cloudinary import upload_file_to_cloudinary,delete_file_from_cloudinary
@role_required(allowed_roles=['Admin','Faculty'])
def resourceAdd(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST,request.FILES)
        if form.is_valid():
            file_obj = request.FILES.get('file_upload')
            resource_instance = form.save(commit=False)
            resource_instance.uploaded_by = request.user
            resource_instance.save()
            print(resource_instance.description)
            unique_name = f"{datetime.now().timestamp()}_{file_obj.name}"
            file_url = upload_file_to_cloudinary(file_obj, unique_name)
            resource_type = request.POST.get('category')
            public_id = unique_name
            add_fields = {
                "resource_id": resource_instance.id,
                "uploaded_by":f"{request.user.username} ({request.user.role})",
                "uploaded_at":datetime.now(),
                "subject":request.POST.get('subject'),
                "resource_type":resource_type,
                "cloud_public_id":public_id,
                "file_url":file_url,

            }
            if resource_type == "Notes":
                add_fields["details"] = {
                    "professor": request.POST.get('professor'),
                    "format": request.POST.get('format'),
                    "topic_coverage": request.POST.get('topic_coverage'),
                }
            elif resource_type == 'Assignment':
                add_fields['details'] = {
                    "deadline": request.POST.get('deadline'),
                    "total_marks": request.POST.get('total_marks'),
                    "lab_work": request.POST.get('lab_work'),
                }
            elif resource_type == 'Syllabus':
                add_fields['details'] = {
                    "academic_year": request.POST.get('academic_year'),
                    "semester": request.POST.get('semester'),
                    "department": request.POST.get('department')
                }
            elif resource_type == 'Previous_paper':
                add_fields['details'] = {
                    "exam_year": request.POST.get('exam_year'),
                    "exam_type": request.POST.get('exam_type'),
                    "difficulty_rating": request.POST.get('difficulty_rating'),
                }
            elif resource_type == 'Reference':
                add_fields['details'] = {
                    "author": request.POST.get('author'),
                    "isbn": request.POST.get('isbn'),
                    "external_link": request.POST.get('external_link'),
                }
            elif resource_type == 'Other':
                add_fields['details'] = {
                    "details": request.POST.get('details'),
                }
            if file_url:
                resource = collection.insert_one(add_fields)
                messages.success(
                request,
                f"Resource -- {resource_instance.title} -- has been Added."
                )
                return redirect('resourceList')
    else:
        form = ResourceForm(request.POST)
    return render(request,'resourceAdd.html',{'form':form})

@role_required(allowed_roles=['Admin', 'Faculty'])
def resourceUpdate(request, id):
    sql_instance = Resource.objects.get(id=id)
    mongo_instance = collection.find_one({"resource_id": id} )or {}
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=sql_instance)
        if form.is_valid():
            updated_sql = form.save()
            file_url = mongo_instance.get('file_url')
            public_id = mongo_instance.get('cloud_public_id')
            if request.FILES.get('file_upload'):
                delete_file_from_cloudinary(public_id)
                file_obj = request.FILES.get('file_upload')
                unique_name = f"{datetime.now().timestamp()}_{file_obj.name}"
                file_url = upload_file_to_cloudinary(file_obj, unique_name)
                public_id = unique_name
            resource_type = request.POST.get('category')
            update_fields = {
                "subject": request.POST.get('subject'),
                "resource_type": resource_type,
                "file_url": file_url,
                "cloud_public_id": public_id,
            }
            details = {}
            if resource_type == "Notes":
                details = {
                    "professor": request.POST.get('professor'),
                    "format": request.POST.get('format'),
                    "topic_coverage": request.POST.get('topic_coverage'),
                }
            elif resource_type == 'Assignment':
                details = {
                    "deadline": request.POST.get('deadline'),
                    "total_marks": request.POST.get('total_marks'),
                    "lab_work": request.POST.get('lab_work'),
                }
            elif resource_type == 'Syllabus':
                details = {
                    "academic_year": request.POST.get('academic_year'),
                    "semester": request.POST.get('semester'),
                    "department": request.POST.get('department')
                }
            elif resource_type == 'Previous_paper':
                details = {
                    "exam_year": request.POST.get('exam_year'),
                    "exam_type": request.POST.get('exam_type'),
                    "difficulty_rating": request.POST.get('difficulty_rating'),
                }
            elif resource_type == 'Reference':
                details = {
                    "author": request.POST.get('author'),
                    "isbn": request.POST.get('isbn'),
                    "external_link": request.POST.get('external_link'),
                }
            elif resource_type == 'Other':
                details = {"details": request.POST.get('details')}
            update_fields["details"] = details

            collection.update_one(
                {"resource_id": id},
                {"$set": update_fields}

            )
            messages.success(request, f"Resource -- {updated_sql.title} -- updated successfully.")
            return redirect('resourceList')
    else:
        form = ResourceForm(instance=sql_instance)
        mongo_details = mongo_instance.get('details', {})
    return render(request, 'resourceUpdate.html', {
        'form': form,
        'resource_instance': mongo_instance,
        'details': mongo_details
    })
@role_required(allowed_roles=['Admin','Faculty'])
def resourceDelete(request,id):
    resource = collection.find_one({"resource_id": id} )or {}
    resources = Resource.objects.get(id=id)
    if request.method == "POST":
        public_id = resource.get('cloud_public_id')
        collection.delete_one({"resource_id":id })
        delete_file_from_cloudinary(public_id)
        resources.delete()
        messages.warning(
            request,
            f" Resource -- {resources.title} -- is successfully Deleted"
        )
        return redirect('resourceList')
    return render(request, 'resourceDelete.html', {'resource': resources})
@role_required(allowed_roles=['Admin','Faculty','Student'])
def resourceList(request):
    resources = Resource.objects.all()
    resource_ids = list(resources.values_list('id', flat=True))

    # Search for the IDs in the 'resource_id' field (checking both int and str)
    search_ids = [int(rid) for rid in resource_ids] + [str(rid) for rid in resource_ids]
    mongo_data = list(collection.find({'resource_id': {'$in': search_ids}}, {'_id': 0}))

    # Map using 'resource_id' as the key
    mongo_map = {}
    for item in mongo_data:
        m_id = item.get('resource_id')
        if m_id is not None:
            try:
                mongo_map[int(m_id)] = item
            except (ValueError, TypeError):
                continue

    for res in resources:
        # Attach the mongo document to the resource instance
        res.mongo_info = mongo_map.get(res.id, {})

    return render(request, 'resourceList.html', {'resources': resources})

