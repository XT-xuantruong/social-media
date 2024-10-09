from django.http import JsonResponse, HttpResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from .forms import SignupForm,ProfileForm
from .models import User, FriendshipRequest
from upload.models import Photo
from upload.serializers import PhotoSerializer
from upload.helpers import custom_response
from .serializers import UserSerializer, FriendshipRequestSerializer
import cloudinary.api


@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.avatar,
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()
        url = f'http://127.0.0.1:8000/activateemail/?email={user.email}&id={user.id}' 
        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "hoanglong200703@gmail.com",
            [user.email],
            fail_silently=False,
        )

        # Send verification email later!
    else:
        message = form.errors.as_json()
    
    print(message)

    return JsonResponse({'message': message}, safe=False)


@api_view(['POST'])
def editprofile(request):
    user = request.user
    email = request.data.get('email')
    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        image = request.FILES.get('avatar')
        data = []
        try:
            upload_result = cloudinary.uploader.upload(image,folder="avatar")
            img_obj = Photo(
                id=upload_result['public_id'],
                url=upload_result['secure_url'],
                filename=upload_result['original_filename'],
                format=upload_result['format'],
                width=upload_result['width'],
                height=upload_result['height'],
                created_at=upload_result['created_at'],
            )
            img_obj.save()
            serializer = PhotoSerializer(img_obj)
            data.append(serializer.data)

            form_data = request.POST.copy()
            form_data['avatar'] = img_obj.url
            
            form = ProfileForm(form_data, instance=user)
            if form.is_valid():
                form.save()
                
            serializer = UserSerializer(user)
            return JsonResponse({'message': 'information updated', 'data': img_obj.url, 'user': serializer.data})
    
        except  Exception as e:
            return custom_response('Upload images failed!', 'Error', [str(e)], 400)
    
@api_view(['POST'])
def editpassword(request):
    user = request.user
    
    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)
        

@api_view(['GET'])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()
    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests
    }, safe=False)

@api_view(['GET'])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})


@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_requests = FriendshipRequest.objects.filter(created_for=request.user, created_by=user)
    for friendship_request in friendship_requests:
        friendship_request.status = status
        friendship_request.save()
    message=""
    if(status=="accepted"):
        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()
        request_user = request.user
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()
        message="accepted request"
    else:
        message="rejected request"

    return JsonResponse({'message': message})

def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(id=id, email=email)
        user.is_active = True
        user.save()
    
        return HttpResponse('The user is now activated. You can go ahead and log in!')
    else:
        return HttpResponse('The parameters is not valid!')