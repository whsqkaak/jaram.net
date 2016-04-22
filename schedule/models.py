from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    date = models.DateTimeField(_('날짜'), null=False, blank=False)
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    link_page = models.CharField(_('연결 페이지'), max_length=255, null=True, blank=True, default='')

    class Meta:
        ordering = ['-date']
        verbose_name = _('행사')
        verbose_name_plural = _('행사')