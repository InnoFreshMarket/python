from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail

from back.managers import UserManager
from django.db.models import QuerySet


class CommentManager(models.Manager):
    def create_comment(self, name, text, rate):
        chat = self.create(name=name, text=text, rate=rate)
        return chat


class Comment(models.Model):
    objects = CommentManager()
    date = models.DateTimeField(null=True, auto_now=True, verbose_name='Время отправки')
    name = models.CharField(null=True, max_length=100, verbose_name='Отправитель')
    rate = models.IntegerField(null=False, verbose_name='Оценка')
    text = models.CharField(null=True, max_length=2048, verbose_name='Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Item(models.Model):
    name = models.CharField(max_length=63, verbose_name='Название')
    cost_retail = models.FloatField(verbose_name='Розничная цена')
    cost_wholesale = models.FloatField(blank=True, null=True, verbose_name='Оптовая цена')
    doc = models.FileField(upload_to='uploads/', verbose_name='Фото')
    date = models.DateField(verbose_name='Дата готовности', blank=True, null=True)
    farmer = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Владелец')
    number = models.FloatField(verbose_name='Количество товара')
    number_wholesale = models.FloatField(blank=True, null=True, verbose_name='Мин. кол-во товара для оптовой закупки')
    description = models.CharField(max_length=63, verbose_name='Описание')
    expire_date = models.DateField(verbose_name='Дата окончания срока годности', blank=True, null=True)
    number_for_month = models.FloatField(blank=True, null=True, verbose_name='Количество товара на месяц(подписка)')
    subscriptable = models.BooleanField(verbose_name="Возможность подписки")
    ITEM_CHOICES = [
        ('FR', 'Фрукты'),
        ('VE', 'Овощи'),
        ('OT', 'Другие')
    ]
    category = models.CharField(max_length=2,
                                choices=ITEM_CHOICES,
                                default='OT',
                                verbose_name='Категории',
                                )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class OrderItemsManager(models.Manager):
    def create_order_item(self, amount, item, farmer, user):
        order = self.create(amount=amount, item=item, farmer=farmer, user=user)
        return order


class ChatManager(models.Manager):
    def create_chat(self, user1, user2, name1, name2):
        chat = self.create(user1=user1, user2=user2, name1=name1, name2=name2)
        return chat


class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель', null=True)
    text = models.CharField(max_length=2048, blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'


class Chat(models.Model):
    objects = ChatManager()
    user1 = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель1', null=True,
                              related_name='user1')
    user2 = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель2', null=True,
                              related_name='user2')
    name1 = models.CharField(max_length=255, null=True, verbose_name='Название чата1')
    name2 = models.CharField(max_length=255, null=True, verbose_name='Название чата2')
    messages = models.ManyToManyField(
        "Message",
        related_name="messages",
        blank=True,
        verbose_name='Сообщения'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Order(models.Model):
    status = models.BooleanField(verbose_name='Статус покупки', default=False)
    items = models.ManyToManyField(
        "OrderItems",
        related_name='items_name_123',
        blank=True,
        verbose_name='Товары'
    )
    date = models.DateField(verbose_name='Дата покупки', auto_now=True)
    PAYMENT_CHOICES = [
        ('CA', 'Карта'),
        ('BC', 'Юр. лицо'),
        ('CS', 'Наличные')
    ]
    SHIPPING_CHOICES = [
        ('CA', 'Самолет'),
        ('BC', 'Поезд'),
    ]

    payment = models.CharField(max_length=3,
                               choices=PAYMENT_CHOICES,
                               default='BY',
                               verbose_name='Роль',
                               blank=True,
                               null=True)
    shipping_address = models.CharField(verbose_name='Адрес доставки', null=True, blank=True)
    way_of_shipping = models.CharField(max_length=3,
                                       choices=PAYMENT_CHOICES,
                                       default='BY',
                                       verbose_name='Роль',
                                       blank=True,
                                       null=True)
    date_of_receive = models.DateField(verbose_name='Дата получения заказа', blank=True, null=True)
    total_price = models.FloatField(verbose_name='Общая стоимость', default=0)
    owner = models.ForeignKey('User', on_delete=models.deletion.CASCADE)


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
    phone_number = models.CharField(max_length=20, null=True, blank=True)
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


class OrderItems(models.Model):
    objects = OrderItemsManager()
    amount = models.IntegerField('Количество товара', default=0)
    item = models.ForeignKey('Item', on_delete=models.deletion.CASCADE, verbose_name='Покупка')
    farmer = models.ForeignKey('User', on_delete=models.deletion.CASCADE, verbose_name='Фермер')
    user = models.ForeignKey('User', on_delete=models.deletion.CASCADE, verbose_name='Покупатель')


class Message(models.Model):
    sender = models.ForeignKey("User", on_delete=models.deletion.CASCADE, verbose_name='Отправитель', null=True)
    text = models.CharField(max_length=2048, blank=False, null=True)
    created_at = models.DateTimeField(auto_now=True, null=False, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'


class ChatManager(models.Manager):
    def create_chat(self, user1, user2, name1, name2):
        chat = self.create(user1=user1, user2=user2, name1=name1, name2=name2)
        return chat


class Chat(models.Model):
    objects = ChatManager()
    user1 = models.ForeignKey(User, on_delete=models.deletion.CASCADE, verbose_name='Отправитель1', null=True,
                              related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.deletion.CASCADE, verbose_name='Отправитель2', null=True,
                              related_name='user2')
    name1 = models.CharField(max_length=255, null=True, verbose_name='Название чата1')
    name2 = models.CharField(max_length=255, null=True, verbose_name='Название чата2')
    messages = models.ManyToManyField(
        "Message",
        related_name="messages",
        blank=True,
        verbose_name='Сообщения'
    )

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Order(models.Model):
    status = models.BooleanField('Статус покупки', default=False)
    date = models.DateField()
