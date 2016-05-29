from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.models import Member


class Study(models.Model):
    leader = models.ForeignKey(Member, related_name='created_study_set')
    members = models.ManyToManyField(Member, related_name='study_set')
    image = models.ImageField(_('대표 이미지'), null=False, blank=False)
    title = models.CharField(_('스터디 이름'), max_length=32, null=False, blank=False)
    description = models.CharField(_('간략한 설명'), max_length=64, null=False, blank=False)
    content = models.TextField(_('계획, 기간 등 상세한 설명'), null=False, blank=False)
    date = models.DateField(_('스터디 등록일'), null=False, blank=False, default=timezone.now)
    is_active = models.BooleanField(_('진행 여부'), null=False, blank=False, default=False)

    class Meta:
        ordering = ['-date']
        verbose_name = _('스터디')
        verbose_name_plural = _('스터디')


class StudyReport(models.Model):
    writer = models.ForeignKey(Member)
    write_date = models.DateTimeField(_('작성일'), null=False, blank=False, default=timezone.now)
    content = models.TextField(_('내용'), null=False, blank=False)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('스터디 보고서')
        verbose_name_plural = _('스터디 보고서')