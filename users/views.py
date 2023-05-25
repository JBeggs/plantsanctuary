from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.views.generic import FormView, UpdateView, TemplateView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    RetrieveAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Address, PhoneNumber, Profile
from .permissions import IsUserAddressOwner, IsUserProfileOwner
from .serializers import (
    AddressReadOnlySerializer,
    PhoneNumberSerializer,
    ProfileSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
    UserSerializer,
    VerifyPhoneNumberSerialzier
)
from .form import UserForm, PhoneNumberForm, ProfileForm, AddressForm

User = get_user_model()


# class UserRegisterationAPIView(RegisterView):
#     """
#     Register new users using phone number or email and password.
#     """
#     serializer_class = UserRegistrationSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#
#         response_data = ''
#
#         email = request.data.get('email', None)
#         phone_number = request.data.get('phone_number', None)
#
#         if email and phone_number:
#             res = SendOrResendSMSAPIView.as_view()(request._request, *args, **kwargs)
#
#             if res.status_code == 200:
#                 response_data = {"detail": _(
#                     "Verification e-mail and SMS sent.")}
#
#         elif email and not phone_number:
#             response_data = {"detail": _("Verification e-mail sent.")}
#
#         else:
#             res = SendOrResendSMSAPIView.as_view()(request._request, *args, **kwargs)
#
#             if res.status_code == 200:
#                 response_data = {"detail": _("Verification SMS sent.")}
#
#         return Response(response_data,
#                         status=status.HTTP_201_CREATED,
#                         headers=headers)
#
#
# class UserLoginAPIView(LoginView):
#     """
#     Authenticate existing users using phone number or email and password.
#     """
#     serializer_class = UserLoginSerializer


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Send OTP
            phone_number = str(serializer.validated_data['phone_number'])

            user = User.objects.filter(
                phone__phone_number=phone_number).first()

            sms_verification = PhoneNumber.objects.filter(
                user=user, is_verified=False).first()

            sms_verification.send_confirmation()

            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches and verify the user.
    """
    serializer_class = VerifyPhoneNumberSerialzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            message = {'detail': _('Phone number successfully verified.')}
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GoogleLogin(SocialLoginView):
#     """
#     Social authentication with Google
#     """
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "call_back_url"
#     client_class = OAuth2Client


class ProfileAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsUserProfileOwner,)

    def get_object(self):
        return self.request.user.profile


class UserAPIView(RetrieveAPIView):
    """
    Get user details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class AddressViewSet(ReadOnlyModelViewSet):
    """
    List and Retrieve user addresses
    """
    queryset = Address.objects.all()
    serializer_class = AddressReadOnlySerializer
    permission_classes = (IsUserAddressOwner,)

    def get_queryset(self):
        res = super().get_queryset()
        user = self.request.user
        return res.filter(user=user)

#
# class UserView(FormView):
#
#     template_name = 'user.html'
#
#     def get(self, request, *args, **kwargs):
#         user_form = UserForm()
#         user_form.prefix = 'user_form'
#         phonenumber_form = PhoneNumberForm()
#         phonenumber_form.prefix = 'phonenumber_form'
#         profile_form = ProfileForm()
#         profile_form.prefix = 'profile_form'
#         # Use RequestContext instead of render_to_response from 3.0
#         return self.render_to_response(self.get_context_data({
#             'user_form': user_form,
#             'phonenumber_form': phonenumber_form,
#             'profile_form': profile_form,
#         }))
#
#     def get_context_data(self, data, **kwargs):
#
#         kwargs['user_form'] = data['user_form']
#         kwargs['phonenumber_form'] = data['phonenumber_form']
#         kwargs['profile_form'] = data['profile_form']
#
#         return super().get_context_data(**kwargs)
#
#
#     def post(self, request, *args, **kwargs):
#
#         user_form = UserForm(self.request.POST, prefix='user_form')
#         phonenumber_form = PhoneNumberForm(self.request.POST, prefix='phonenumber_form ')
#         profile_form = ProfileForm(self.request.POST, prefix='profile_form ')
#
#         if user_form.is_valid() and phonenumber_form.is_valid() and profile_form.is_valid():
#             ### do something
#             return HttpResponseRedirect('')
#         else:
#             return self.form_invalid(user_form, phonenumber_form, profile_form, **kwargs)
#
#     def form_invalid(self, user_form, phonenumber_form, profile_form, **kwargs):
#         user_form.prefix = 'user_form'
#         phonenumber_form.prefix = 'phonenumber_form'
#         profile_form.prefix = 'profile_form'
#
#         return self.render_to_response(self.get_context_data({
#             'user_form': user_form,
#             'phonenumber_form': phonenumber_form,
#             'profile_form': profile_form,
#         }))


class UserView(LoginRequiredMixin, TemplateView):

    user_form = UserForm
    user_form.prefix = 'user_form'
    phonenumber_form = PhoneNumberForm
    phonenumber_form.prefix = 'phonenumber_form'
    profile_form = ProfileForm
    profile_form.prefix = 'profile_form'
    address_form = AddressForm
    address_form.prefix = 'address_form'
    template_name = 'user.html'

    def post(self, request, *args, **kwargs):

        post_data = request.POST or {}
        saved = False
        if 'first_name' in post_data \
                and 'last_name' in post_data \
                and 'email' in post_data:
            user_form = self.user_form(post_data, instance=request.user)
            user_valid = user_form.is_valid()
            if user_valid:
                self.user_save(user_form)
                saved = True
        else:
            user_form = self.user_form(instance=request.user)

        if 'phonenumber_form-phone_number' in post_data:
            phonenumber_form = self.phonenumber_form(post_data, prefix='phonenumber_form',
                                                     instance=PhoneNumber.objects.filter(user=request.user).first())
            phonenumber_valid = phonenumber_form.is_valid()
            if phonenumber_valid:
                self.phonenumber_save(phonenumber_form)
                saved = True
        else:
            phonenumber_form = self.phonenumber_form(prefix='phonenumber_form',
                                                     instance=PhoneNumber.objects.filter(user=request.user).first())
        if 'profile_form-bio' in post_data:

            profile_form = self.profile_form(post_data, prefix='profile_form',
                                             instance=Profile.objects.filter(user=request.user).first())
            profile_valid = profile_form.is_valid()
            if profile_valid:
                self.profile_save(profile_form)
                saved = True
        else:
            profile_form = self.profile_form(prefix='profile_form',
                                             instance=Profile.objects.filter(user=request.user).first())
        if 'address_form-street_address' in post_data:
            address_form = self.address_form(post_data, prefix='address_form')
            address_valid = address_form.is_valid()
            if address_valid:
                self.address_save(address_form)
                saved = True
        else:
            address_form = self.address_form(post_data, prefix='address_form')

        if saved:
            return redirect(request.META.get('HTTP_REFERER'))
        if request.user.is_anonymous:
            return redirect('/accounts/login/')

        context = self.get_context_data(
            user_form=user_form,
            phonenumber_form=phonenumber_form,
            profile_form=profile_form,
            address_form=address_form
        )

        context['addresses'] = Address.objects.filter(user=request.user)
        context['user'] = User.objects.filter(pk=request.user.id).first()
        context['phonenumber'] = PhoneNumber.objects.filter(user=request.user).first()

        return self.render_to_response(context)

    def user_save(self, form):

        user = User.objects.get(id=self.request.user.id)

        for key in form.data:
            exec('user.{} = form.data["{}"]'.format(key.replace("'", ''), key))
        user.is_active = True
        user.save()

        messages.success(self.request, "{} saved successfully".format(user))
        return user

    def phonenumber_save(self, form):

        phonenumber = PhoneNumber.objects.filter(user=self.request.user).first()
        if phonenumber:
            for key in form.changed_data:
                exec('phonenumber.{} = form.cleaned_data["{}"]'.format(key.replace("'", ''), key))
            phonenumber.save()
            messages.success(self.request, "{} saved successfully".format(phonenumber))
        else:
            phonenumber = PhoneNumber()
            phonenumber.user = self.request.user
            for key in form.changed_data:
                exec('phonenumber.{} = form.cleaned_data["{}"]'.format(key.replace("'", ''), key))
            phonenumber.save()

        return phonenumber

    def profile_save(self, form):

        profile = form.save(commit=False)
        if 'profile_form-avatar' in self.request.FILES:
            profile.avatar = self.request.FILES['profile_form-avatar']
        profile.user = self.request.user
        profile.save()
        messages.success(self.request, "{} saved successfully".format(profile))

        return profile

    def address_save(self, form):

        address = form.save(commit=False)
        address.user = self.request.user
        address.save()
        messages.success(self.request, "{} saved successfully".format(address))
        return address

    def get(self, request, *args, **kwargs):

        if request.user.is_anonymous:
            messages.success(self.request, "Please Login")
            return redirect("/")

        return self.post(request, *args, **kwargs)
