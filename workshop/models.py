from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.models import Member


class WorkShop(models.Model):
    start_date = models.DateField(_('워크숍 시작 날짜'), null=True, blank=True)
    end_date = models.DateField(_('워크숍 끝 날짜'), null=True, blank=True)
    subject = models.CharField(_('주제'), max_length=255, null=False, blank=False)
    content = models.TextField(_('내용'), null=True, blank=True, default='')

    # TODO: 일정표, 오픈일?

    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['-id']
        verbose_name = _('워크숍')
        verbose_name_plural = _('워크숍')


class WorkShopTask(models.Model):
    title = models.CharField(_('과제 제목'), max_length=255, null=False, blank=False)
    content = models.TextField(_('과제 내용'), null=False, blank=False)
    duty_member = models.ManyToManyField(Member)
    deadline = models.DateTimeField(_('제출 마감일'), null=True, blank=True)
    # TODO: 첨부파일

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = _('워크숍 과제')
        verbose_name_plural = _('워크숍 과제')


class WorkShopTaskSubmission(models.Model):
    task = models.ForeignKey(WorkShopTask)
    presenter = models.ForeignKey(Member)
    content = models.TextField(_('내용'), null=True, blank=True, default='')
    date = models.DateTimeField(_('제출일'), null=False, blank=False, default=timezone.now)

    def __unicode__(self):
        return self.presenter.name + ' - ' + self.presenter.name

    class Meta:
        ordering = ['-id']
        verbose_name = _('워크숍 과제 제출')
        verbose_name_plural = _('워크숍 과제 제출')
