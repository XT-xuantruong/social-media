from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.models import User
from account.serializers import UserSerializer

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend, PostAttachment
from upload.models import Photo
from upload.serializers import PhotoSerializer
from upload.helpers import custom_response
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer, TrendSerializer
from django.forms.models import model_to_dict
import cloudinary.api


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))
    
    trend = request.GET.get('trend', '')
    print(trend)
    if trend:
        posts = posts.filter(body__icontains='#' + trend[:-1])
        
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    user = request.user
    images = request.FILES.getlist('attachments')
    data = []

    post_data = request.POST.copy()
    post_data['created_by'] = user.id

    post_form = PostForm(post_data)

    if post_form.is_valid():
        post = post_form.save(commit=False)
        post.created_by = user
        post.save()

        for image in images:
            try:
                upload_result = cloudinary.uploader.upload(image,folder="post")
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

                attachment_obj = PostAttachment(
                    image=img_obj.url,
                    created_by=user
                )
                attachment_obj.save()
                post.attachments.add(attachment_obj)
                data.append({
                        'photo': model_to_dict(img_obj),  # Trả về thông tin ảnh từ model Photo
                        'attachments': model_to_dict(attachment_obj)  # Trả về thông tin attachment
                    })   
            except  Exception as e:
                return custom_response('Upload images failed!', 'Error', [str(e)], 400)
        post.save()
        post_serializer = PostSerializer(post)
        return custom_response('Post created successfully!','Success', data=post_serializer.data, status_code=201)
    else:
        return custom_response('Invalid form data!','Errors', data=post_form.errors, status_code=400)
    

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})
    
@api_view(['POST'])
def post_create_comment(request, pk):
    comment = Comment.objects.create(body=request.data.get('body'), created_by=request.user)
    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()
    serializer = CommentSerializer(comment)
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)
    return JsonResponse(serializer.data, safe=False)