from django.db import models
from django.utils.translation import ugettext_lazy as _


class Album(models.Model):
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    date = models.DateField(_('날짜'), null=False, blank=False)

    # TODO: 이미지들

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = _('앨범')
        verbose_name_plural = _('앨범')
