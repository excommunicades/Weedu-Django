from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import MaxValueValidator

from django.db import models

from publish.models.models import Shop

from publish.models.models import Purchase

def get_model(model):

    if model == 'Shop':
        
        from publish.models.models import Shop

        return Shop

    if model == 'Purchase':

        from publish.models.models import Purchase

        return Purchase
class Weedu_UserManager(BaseUserManager):

    def get_by_natural_key(self, username):

        return self.get(username=username)

    def create_user(self, username, email, password=None, **extra_fields):

        if not email:
            raise ValueError('Пользователь должен иметь email')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Weedu_User(AbstractBaseUser, PermissionsMixin):

    """ToDo user model"""

    # first_name = models.CharField(max_length=30, blank=False, null=False)
    # last_name = models.CharField(max_length=30, blank=False, null=False)

    username = models.CharField(
                            max_length=30,
                            blank= False,
                            null=False,
                            unique=True,
                            )

    email = models.EmailField(
                        unique=True,
                        blank=False,
                        null=False,
                        )

    password = models.CharField(
                            max_length=128,
                            blank=False,
                            null=False,
                            )

    avatar = models.ImageField(upload_to='users_avatar/', null=True, blank=True)

    expirience = models.SmallIntegerField(
                                    default=0,
                                    null=False,
                                    blank=True,
                                    validators=[MaxValueValidator(100)])

    level = models.SmallIntegerField(
                                default=0,
                                null=False,
                                blank=False,)

    purchased_products = models.ManyToManyField(get_model('Shop'), through=get_model('Purchase'))

    praise = models.SmallIntegerField(default=0, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    is_authenticated = models.BooleanField(default=False)

    registered_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    # courses_completed = models.SmallIntegerField()

    # quiz_completed = models.SmallIntegerField()

    # ...

    USERNAME_FIELD = 'username'

    objects = Weedu_UserManager()
