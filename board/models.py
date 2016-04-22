from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.models import Member


class BaseBoardModel(models.Model):
    writer = models.ForeignKey(Member)
    write_date = models.DateTimeField(_('작성일'))
    title = models.CharField(_('제목'), max_length=255, null=True, blank=True, default='')
    content = models.TextField(_('내용'), null=False, blank=False)

    # TODO: 첨부파일, 연관 일정

    class Meta:
        abstract = True


class PlayStorming(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('플레이스토밍')
        verbose_name_plural = _('플레이스토밍')


class Seminar(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('세미나')
        verbose_name_plural = _('세미나')


class EventReport(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('행사보고')
        verbose_name_plural = _('행사보고')
