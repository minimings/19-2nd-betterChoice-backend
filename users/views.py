import bcrypt
import jwt
import json
import my_settings

from django.views     import View
from django.http      import JsonResponse

from users.models     import User, UserCoupon, Coupon, UserLike, PhoneCheck

class SignUpView(View):
    def post(self, request):

        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']
            nickname = data['nickname']

            if not my_settings.EMAIL_CHECK.match(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)
            
            if not my_settings.PASSWORD_CHECK.match(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'EMAIL_ALREADY_EXIST'}, status=400)
            
            if User.objects.filter(nickname=nickname).exists():
                return JsonResponse({'MESSAGE':'NICKNAME_ALREADY_EXIST'}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')
            
            User.objects.create(
                email     = email,
                password  = hashed_password,
                nickname  = nickname,
                is_social = False
            )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE': 'JSON_DECODE_ERROR'}, status=400)