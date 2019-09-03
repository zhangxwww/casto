from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Operation
import uuid
import pytz
import datetime
import time
import os

# Create your views here.


UPLOAD_PATH = '../images'

if not os.path.exists(UPLOAD_PATH):
    os.mkdir(UPLOAD_PATH)


@login_required
def upload(request):
    file_local = request.FILES.get('image', None)
    file_web = request.POST.get('url', None)
    if file_local is None and file_web is None:
        return HttpResponse(status=400)
    image_name = str(uuid.uuid1())
    path = os.path.join(UPLOAD_PATH, image_name)
    if file_local is not None:
        raw_name = file_local.name
        _, suffix = os.path.split(raw_name)
        if not suffix in ['jpg', 'JPEG', 'jpeg']:
            return JsonResponse({'error': 'wrong jpeg format'})
        path += '.' + suffix
        with open(path, 'wb') as file:
            for chuck in file_local.chunks():
                file.write(chuck)
    else:
        # TODO
        raw_name = 'image.jpg'
        pass
    operation = Operation.objects.create(
        raw_image=path,
        raw_image_name=raw_name,
        user_id=request.user.id
    )
    operation.save()
    return JsonResponse({'id': operation.id})


@login_required
def net(request, net_id):
    user_id = request.user.id
    operation_id = request.POST.get('id', None)
    if operation_id is None:
        return JsonResponse({'error': 'not exists'})
    operation = Operation.objects.get(id=operation_id)
    if operation.user_id != user_id:
        return JsonResponse({'error': 'not exists'})
    if net_id == 0:
        # TODO processed_path = net(raw_path)
        processed_path = operation.raw_image  # TODO delete later
    else:
        # TODO processed_path = net(raw_path)
        processed_path = operation.raw_image  # TODO delete later
    with open(processed_path, 'rb') as f:
        data = f.read()
    return JsonResponse({'data': data})


@login_required
def delete(request):
    user_id = request.user.id

    def delete_operation(operation_id):
        operation = Operation.objects.get(id=operation_id)
        if operation.user_id != user_id:
            return False
        else:
            operation.delete()
            return True

    ids = request.POST.get('ids', [])
    res = [{'id': id_, 'state': delete_operation(id_)} for id_ in ids]
    return JsonResponse({'list': res})


@login_required
def query(request):
    start = request.POST.get('start', 0)
    end = request.POST.get('end', 9999999999)
    start_time = datetime.datetime.fromtimestamp(start, tz=pytz.timezone('UTC'))
    end_time = datetime.datetime.fromtimestamp(end, tz=pytz.timezone('UTC'))
    user_id = request.user.id
    query_set = Operation.objects.filter(user_id=user_id)\
        .filter(upload_time__gt=start_time)\
        .filter(upload_time__lt=end_time)
    return JsonResponse({'list': [get_operation_info(op) for op in query_set]})


@login_required
def get(request, operation_id):
    user_id = request.user.id
    operation = Operation.objects.get(id=operation_id)
    if operation.user_id != user_id:
        return JsonResponse({'error': 'not exists'})
    return JsonResponse(get_operation_info(operation))


def get_operation_info(operation):
    return {
        'id': operation.id,
        'time': time.mktime(operation.upload_time.timetuple()),
        'raw': operation.raw_image,
        'name': operation.raw_image_name
    }