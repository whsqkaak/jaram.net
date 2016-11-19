from django import template
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Grade(models.Model):
    name = models.CharField(_('등급 이름'), max_length=10, null=False, blank=False)
    group = models.ForeignKey(Group, null=False, blank=False)

    def __str__(self):
        return self.name

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

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


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


class Member(AbstractBaseUser, PermissionsMixin):
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
    profile = models.ImageField(_('프로필 이미지'), upload_to='member/profile/', null=True, blank=True)

    # 서버 운영에 필요한 정보
    date_joined = models.DateTimeField(_('가입 날짜'), default=timezone.now)
    is_active = models.BooleanField(_('활성화 여부'), default=True)
    is_staff = models.BooleanField(_('사이트 관리 권한'), default=False)

    USERNAME_FIELD = 'user_id'

    objects = UserManager()

    def __str__(self):
        return self.name

    def to_dict(self):
        result = dict()

        result['id'] = self.pk
        result['name'] = self.name
        result['period'] = self.period
        result['grade'] = self.grade.name

        if self.profile:
            result['profile'] = self.profile.url

        return result

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

    def enter_year_short(self):
        return self.enter_year % 100

    def get_level(self, groups):
        if self.is_superuser or self.is_staff:
            return 0

        if Group.objects.get(name='임원진') in self.groups.all():
            return 1

        if self.groups.filter(pk__in=groups.values_list('pk', flat=True)).exists():
            return 2

        return 3

    class Meta:
        ordering = ['-id']
        verbose_name = _('자람 회원')
        verbose_name_plural = _('자람 회원')


class Notice(models.Model):
    title = models.CharField(_('제목'), max_length=255, null=True, blank=True, default='')
    write_date = models.DateTimeField(_('작성일'), null=False, blank=False, default=timezone.now)
    url = models.URLField(_('관련글'), null=True, blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('공지')
        verbose_name_plural = _('공지')