from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.response import Response
from .serializers import  AvatarListSerializer
from rest_framework import status
from .models import Avatar
from rest_framework.views import APIView
import logging
import uuid
import jwt
import os


class AvatarUploadView(APIView):
    def validate_jwt_token(self, request):
        """
        Custom JWT token validation method.

        Args:
            request (Request): Incoming HTTP request

        Returns:
            dict: Decoded token payload if valid
        Raises:
            ValidationError: If token is invalid
        """
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            raise ValidationError("Invalid Authorization header format")

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                'django-insecure-dquen$ta141%61x(1^cf&73(&h+$76*@wbudpia^^ecijswi=q',
                algorithms=['HS256']
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")

    def post(self, request):
        """
        Handle avatar upload with JWT authentication
        """
        try:
            # Validate token and extract payload
            token_payload = self.validate_jwt_token(request)
            user_id = token_payload.get('user_id')
            if not user_id:
                return Response(
                    {"error": "No user_id found in token"},
                    status=status.HTTP_400_BAD_REQUEST
                    )
            image = request.FILES.get('image') # penser a ajouter securite tests sur l'image
            if not image:
                return Response(
                    {"error": "invalid image provided"},
                    status=status.HTTP_400_BAD_REQUEST
                    )

        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        try:
            avatar = Avatar.objects.get(Userid=user_id)
            old_img_path  =f"images/{avatar.uuid}.jpg"
            if (os.path.exists(old_img_path)):
                os.remove(old_img_path)
            avatar.image = image
            avatar.uuid = uuid.uuid4()
            avatar.save()
            return Response(
                {"message": f"Image uploaded successfully {avatar.uuid}"}
                )
        except Avatar.DoesNotExist:
            avatar = Avatar.objects.create(
            Userid=user_id,
            image=image
            )
            return Response(
                {"message": "Image uploaded successfully", "uuid": avatar.uuid},
                  status=201
                  )


@api_view(['GET'])
def get_image(request, img_id):
    try:
        avatar = Avatar.objects.get(uuid = img_id)
        with open(avatar.image.path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            response['Cache-Control'] = 'max-age=3600'  # duree cache a ajuster
            logging.info(f"returning image from id: {img_id}");
            return response
    except (Avatar.DoesNotExist,FileNotFoundError):
            with open('default_image/avatar_default.jpg', 'rb') as image_file:
                response = HttpResponse(image_file.read(), content_type='image/jpeg')
                response['Cache-Control'] = 'max-age=3600'  # duree cache a ajuster
                logging.info(f"uuid not found returning fallback image");
                return response

class AvatarListView(APIView):
    def validate_jwt_token(self, request):
        """
        Custom JWT token validation method.

        Args:
            request (Request): Incoming HTTP request

        Returns:
            dict: Decoded token payload if valid
        Raises:
            ValidationError: If token is invalid
        """
        # Get Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header.startswith('Bearer '):
            raise ValidationError("Invalid Authorization header format")

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(
                token,
                'django-insecure-dquen$ta141%61x(1^cf&73(&h+$76*@wbudpia^^ecijswi=q',
                algorithms=['HS256']
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise ValidationError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValidationError("Invalid token")

    def get(self, request):
        """
        Return user list with corresponding uuid
        """
        try:
            self.validate_jwt_token(request)
            users = Avatar.objects.all()
            serializer = AvatarListSerializer(users, many=True)
            return JsonResponse(serializer.data, safe=False)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



