from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail

from back.managers import UserManager
from django.db.models import QuerySet

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    ROLE_CHOICES = [
        ('FM', 'Фермер'),
        ('BY', 'Покупатель'),
        ('AD', 'Админ')
    ]
    role = models.CharField(max_length=3,
                               choices=ROLE_CHOICES,
                               default='BY',
                               verbose_name='Роль',
                               blank=False)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null = True, blank=True)
    card = models.CharField(max_length=20, null=True, blank=True)
    numbers_of_comments = models.IntegerField(default=0)
    rate = models.FloatField(default=0.0)
    comments = models.ManyToManyField(
        "Comment",
        related_name='comments',
        blank=True,
        verbose_name='Комментарии'
    )
    chats = models.ManyToManyField(
        "Chat",
        related_name='chats',
        blank=True,
        verbose_name='Чаты'
    )
    # items =
    @property
    def get_items(self) -> QuerySet[Item]:
        return Item.objects.filter(farmer__email=self.email)
    def get_orders(self):
        return Order.objects.filter(owner__id=self.id)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.name)
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
