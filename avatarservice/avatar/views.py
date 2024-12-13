from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AvatarSerializer, AvatarListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .models import Avatar
from django.http import HttpResponse
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from django.conf import settings
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from .models import Avatar


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    token_payload = request.auth
    user_id = token_payload.get("user_id")
    if not user_id:
        return Response({"error": "Invalid token payload"}, status=400)
    image = request.FILES.get('image') # penser a ajouter securite
    if not image:
        return Response({"error": "invalid image provided"}, status=400)
    try:
        avatar = Avatar.objects.filter(Userid=user_id).first()
        return Response({"message": "Image uploaded successfully"})
    except Avatar.DoesNotExist:
        avatar = Avatar.objects.create(
        Userid=user_id,
        image=image
        )
        return Response({"message": "Image uploaded successfully", "uuid": avatar.uuid}, status=201)

    # Logique d'upload ou autre




        # serializer = AvatarSerializer(data=request.data)
        # try:
        # 	image = Avatar.objects.get(Userid=22588)# a remplacer une fois jwt etabli
        # 	return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except Avatar.DoesNotExist:
        # 	return Response(serializer.data, status=status.HTTP_201_CREATED)
            # si il ne
    # serializer = AvatarSerializer(data=request.data)
    # if serializer.is_valid():
    # 	serializer.save()
    # 	return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#modifier pour chercher userId et supprimer l'ancien

@api_view(['GET'])
def get_image(request, img_id):
    try:
        avatar = Avatar.objects.get(uuid = img_id)
        with open(avatar.image.path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            response['Cache-Control'] = 'max-age=3600'  # duree cache a ajuster
            logging.info(f"returning image from id: {img_id}");
            return response
    except Avatar.DoesNotExist:
        with open('images/avatar_default.jpg', 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            response['Cache-Control'] = 'max-age=3600'  # duree cache a ajuster
            logging.info(f"uuid not found returning fallback image");
            return response



@api_view(['GET'])
def get_avatar_list(request):
    users = Avatar.objects.all()
    serializer = AvatarListSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
