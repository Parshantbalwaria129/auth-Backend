from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, EmailOtpModel, phoneOtpModel
from .utils import SendEmailOtp, VarifyOTP, SendPhoneOtp
import random
from datetime import timedelta, datetime
from .serializers import GetUserProfileSerializer


@api_view(['POST'])
def checkUsernameAvailability(request):
    try:
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists', 'flag': 'exists'}, status=status.HTTP_306_RESERVED)
        else:
            return Response({'message': 'Username available', 'flag': 'available'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkEmailAvailability(request):
    try:
        email = request.data.get('email')
        if User.objects.filter(email=email).exists() or UserProfile.objects.filter(secondEmail=email).exists():
            return Response({'error': 'Email already exists', 'flag': 'exists'}, status=status.HTTP_306_RESERVED)
        else:
            return Response({'message': 'Email available', 'flag': 'available'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkPhoneAvailability(request):
    try:
        phone = request.data.get('phone')
        if UserProfile.objects.filter(phone=phone).exists() or UserProfile.objects.filter(secondPhone=phone).exists():
            return Response({'error': 'Phone number already exists', 'flag': 'exists'}, status=status.HTTP_306_RESERVED)
        else:
            return Response({'message': 'Phone Number available', 'flag': 'available'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def sendEmailOtp(request):
    try:
        email = request.data.get('email')
        otp = random.randint(100000, 999999)
        otp_mail = SendEmailOtp()

        if otp_mail.send_otp(email, otp):
            if EmailOtpModel.objects.filter(email=email).exists():
                EmailOtpModel.objects.filter(email=email).delete()
            otpModel = EmailOtpModel.objects.create(
                email=email, otp=otp, validTime=(datetime.now() + timedelta(minutes=5)))
            otpModel.save()

            return Response({'message': 'OTP sent successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Mail not sent', 'flag': 'mailNotSent'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def registerUser(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        otp = request.data.get('otp')

        verifyotp = VarifyOTP(otpField=email, otp=otp)
        if verifyotp.isExist():
            if verifyotp.isValid():
                user = User.objects.create_user(
                    username=username, email=email, password=password)
                user.save()
                userProfile = UserProfile.objects.create(
                    username=user)
                userProfile.save()
                verifyotp.delete()
                return Response({'message': 'User registered successfully', 'flag': 'success'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'OTP expired', 'flag': 'expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'OTP not valid', 'flag': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendPhoneOtp(request):
    try:
        phone = request.data.get('phone')
        otp = random.randint(100000, 999999)
        phoneotp = SendPhoneOtp()
        if phoneotp.sendOtp(phone, otp):
            if phoneOtpModel.objects.filter(phone=phone).exists():
                phoneOtpModel.objects.filter(phone=phone).delete()

            otpmodel = phoneOtpModel.objects.create(
                phone=phone, otp=otp, validTime=(datetime.now() + timedelta(minutes=5)))
            otpmodel.save()
            return Response({'message': 'OTP sent successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'OTP not sent', 'flag': 'otpNotSent'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendEmailUpdateOtp(request):
    try:
        email = request.data.get('email')
        otp = random.randint(100000, 999999)
        otp_mail = SendEmailOtp()

        if otp_mail.send_otp(email, otp):
            otpModel = EmailOtpModel.objects.create(
                email=email, otp=otp, validTime=(datetime.now() + timedelta(minutes=5)))
            otpModel.save()
            return Response({'message': 'OTP sent successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Mail not sent', 'flag': 'mailNotSent'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateEmail(request):
    try:
        email = request.data.get('email')
        otp = request.data.get('otp')
        verifyOtp = VarifyOTP(otpField=email, otp=otp)
        if verifyOtp.isExist():
            if verifyOtp.isValid():
                user = request.user
                user.email = email
                user.save()
                verifyOtp.delete()
                return Response({'message': 'Email updated successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'OTP expired', 'flag': 'expired'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'OTP not valid', 'flag': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verifyAndUpdate(request):
    try:
        for _, value in request.data.items():
            field = otp = ''
            for key, value in value.items():
                if key == 'secondEmail' or key == 'phone' or key == 'secondPhone':
                    field = value
                    fieldKey = key
                if key == 'otp':
                    otp = value
            verifyOtp = VarifyOTP(otpField=field, otp=otp)
            if verifyOtp.isExist():
                if verifyOtp.isValid():
                    user = request.user
                    print(fieldKey, " : ", field)
                    userProfile = UserProfile.objects.get(username=user)
                    setattr(userProfile, fieldKey, field)
                    userProfile.save()
                    # verifyOtp.delete()
                    return Response({'message': f'{fieldKey} updated successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'OTP expired', 'flag': 'expired'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'OTP not valid', 'flag': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    try:
        user = request.user
        userProfile = UserProfile.objects.get(username=user)
        for key, value in request.data.items():
            setattr(userProfile, key, value)

        userProfile.save()
        return Response({'message': 'Profile updated successfully', 'flag': 'success'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try:
        # In response we will send all the fields of UserProfile model and email from User model
        user = request.user
        if (not UserProfile.objects.filter(username=user).exists()):
            userProfile = UserProfile.objects.create(username=user)
            userProfile.save()
        userProfile = UserProfile.objects.get(username=user)
        serializer = GetUserProfileSerializer(userProfile)
        data = serializer.data
        data['email'] = user.email
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({'error': 'Something went wrong', 'flag': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
