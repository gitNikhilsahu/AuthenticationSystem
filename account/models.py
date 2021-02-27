from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.models import Group
#auto token ganerated___
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import os


class UserAccountManager(BaseUserManager):
    def create_user(self,username,email,password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')
        if password is None:
            raise TypeError('Password should not be none..')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        # group = Group.objects.get(name='customer')
        # user.groups.add(group) #register then auto customer add
        return user

    def create_superuser(self,username,email,password=None):
        if password is None:
            raise TypeError('Password should not be none..')

        user = self.create_user(username,email,password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30,unique=True,db_index=True)
    first_name = models.CharField(max_length=64,blank=True,null=True)
    last_name = models.CharField(max_length=64,blank=True,null=True)
    email = models.EmailField(max_length=255,unique=True,db_index=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(verbose_name="Phone Number",validators=[phone_regex],max_length=15,unique=True,db_index=True,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='Date Joined',default=timezone.now)
    last_login= models.DateTimeField(verbose_name='Last Login',auto_now=True)
    date_updated = models.DateTimeField(verbose_name="date updated",auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserAccountManager()

    def save(self, *args, **kwargs):
        email = self.email
        if email and type(email) in [str]:
            self.email = email.lower()

        first_name = self.first_name
        if first_name and type(first_name) in [str]:
            self.first_name = first_name.lower()

        last_name = self.last_name
        if last_name and type(last_name) in [str]:
            self.last_name = last_name.lower()
        super(UserModel, self).save(*args, **kwargs)

    def get_full_name(self):
        return "{}, {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'access': str(refresh.access_token)
    #     }

#auto token ganerated___
@receiver(post_save, sender=UserModel)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
#___nik

def upload_location(instance, filename):
    u_pk = instance.user.pk
    u_n = instance.user.username
    slug = '{}-{}'.format(u_n, u_pk)
    file_extension = filename.split(".")[-1]
    n_f = "%s.%s" %(slug, file_extension)
    return "users/%s/%s" %(u_pk,n_f)

class UserProfile(models.Model):
    user = models.OneToOneField(UserModel,related_name='userprofile',on_delete=models.CASCADE)
    birth_date = models.DateField(null=True,blank=True)
    image = models.ImageField(upload_to=upload_location)
    bio = models.TextField(max_length=500,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.user.username

@receiver(post_delete, sender=UserProfile)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)

@receiver(post_save,sender=UserModel)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
