from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Grade(models.Model):
    name = models.CharField(_('등급 이름'), max_length=10, null=False, blank=False)

    class Meta:
        verbose_name = _('회원 등급')
        verbose_name_plural = _('회원 등급')


class BaseUserManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        email = email or ''

        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name, domain_part.lower()])

        return email

    @staticmethod
    def make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789!@#$^'):
        from django.utils.crypto import get_random_string
        return get_random_string(length, allowed_chars)


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None, **kwargs):
        user = self.model(user_id=user_id, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, **kwargs):
        user = self.create_user(user_id, password, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Member(AbstractBaseUser):
    # 기본 정보
    user_id = models.CharField(_('아이디'), max_length=20, null=False, blank=False, unique=True, db_index=True)
    name = models.CharField(_('이름'), max_length=15, null=False, blank=False)
    email = models.EmailField(_('이메일'), max_length=64, null=True, blank=True, default='')
    phone = models.CharField(_('전화번호'), max_length=20, null=True, blank=True, default='')
    period = models.IntegerField(_('기수'), null=False, blank=False)
    enter_year = models.IntegerField(_('학번(입학년도)'), null=False, blank=False)
    grade = models.ForeignKey(Grade, null=False, blank=False)

    # 부가 정보
    birth = models.DateField(_('생일'), null=True, blank=True)
    sns = models.CharField(_('SNS 주소'), max_length=255, null=True, blank=True)

    # 서버 운영에 필요한 정보
    date_joined = models.DateTimeField(_('가입 날짜'), default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(_('임원진'), default=False)

    USERNAME_FIELD = 'user_id'

    objects = UserManager()

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(param_raw_password):
            self.set_password(param_raw_password)
            self.save(update_fields=['password'])

        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password, setter)

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_username(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('자람 회원')
        verbose_name_plural = _('자람 회원')



