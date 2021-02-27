from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# from django.contrib.auth.models import Group

#auto token ganerated___
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
#___


class UserAccountManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not username:
            raise ValueError(_('Users must have a username'))

        if not email:
            raise ValueError(_('Users must have a email'))

        # if email:
        #     email = self.normalize_email(email)

        # if not password:
        #     raise ValueError("Password is required")

        user = self.model(
            username=username,
            email=email
            # email=self.normalize_email(email),
            # phone_number=phone_number
        )
        user.set_password(password)
        # user.username(username)
        # user.email(email)
        # user.phone_number(phone_number)
        user.save(using=self._db)
        # group = Group.objects.get(name='customer')
        # user.groups.add(group) #register then auto customer add
        return user

    def create_superuser(self,username,email,password):
        user = self.create_user(
            username=username,
            email=email,
            # phone_number=phone_number,
            password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        # user.is_admin = True
        # user.is_management_staff = True
        # user.is_member = True
        user.save(using=self._db)
        return user

# def username_v(value):
#     if value % 2 != 0:
#         raise ValidationError(
#             _('%(value)s is starting min 3 character'),
#             params={'value': value},
#         )
# validators=[username_v]

class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=64,unique=True)
    first_name = models.CharField(max_length=64,blank=True,null=True)
    last_name = models.CharField(max_length=64,blank=True,null=True)
    email = models.EmailField(verbose_name="Email",max_length=64,unique=True,blank=True,null=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(verbose_name="Phone Number",validators=[phone_regex],max_length=15,unique=True,blank=True,null=True)
    featured_image = models.CharField(max_length=500,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs): # Ensures lowercase usernames
        username = self.username
        if username and type(username) in [str]:
            self.username = username.lower()   # Only lower case allowed

        email = self.email
        if email and type(email) in [str]:
            self.email = email.lower() # self.normalize_email(email)                     #nik...

        first_name = self.first_name
        if first_name and type(first_name) in [str]:
            self.first_name = first_name.lower()

        last_name = self.last_name
        if last_name and type(last_name) in [str]:
            self.last_name = last_name.lower()
        super(UserAccount, self).save(*args, **kwargs)

    def get_full_name(self):
        return "{}, {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username


#auto token ganerated___
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
#___

def upload_locations(instance, filename):
    u_id = instance.user.pk
    u_u = instance.user.username
    count = UserImage.objects.filter(user=instance.user).count()
    if count:
        slug = '{}-{}'.format(u_u, count)
    else:
        slug = u_u
    file_extension = filename.split(".")[-1]
    n_f = "%s.%s" %(slug, file_extension)
    return "user/%s/%s" %(u_id, n_f)

class UserImage(models.Model):
    user = models.ForeignKey(UserAccount,related_name='userimage',on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to=upload_locations)
    
    def __str__(self):
        return self.user.username

@receiver(post_delete, sender=UserImage)
def submission_delete(sender, instance, **kwargs):
	instance.user_image.delete(False)

class UserProfile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL,related_name='userprofile',on_delete=models.CASCADE)
	birth_date = models.DateField(null=True,blank=True)
	bio = models.TextField(max_length=500,null=True,blank=True)
	address = models.CharField(max_length=255,null=True,blank=True)
	about = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.user.username
    
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profile_pic/img/profile_dummy.png", null=True, blank=True, upload_to="profile_pic/img/")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name