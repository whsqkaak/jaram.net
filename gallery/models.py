import os

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Album(models.Model):
    gphoto_id = models.BigIntegerField(_('구글 포토 앨범 ID'), null=False, blank=False, db_index=True)
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    description = models.TextField(_('설명'), null=True, blank=True)
    main_url = models.CharField(_('대표 이미지 주소'), max_length=255, null=False, blank=False)
    thumbnail_url = models.CharField(_('미리보기 이미지 주소'), max_length=255, null=False, blank=False)
    date = models.DateField(_('날짜'), null=False, blank=False)
    pub_date = models.DateTimeField(_('등록 날짜'), null=False, blank=True)
    update_date = models.DateTimeField(_('수정 날짜'), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = _('앨범')
        verbose_name_plural = _('앨범')


class Photo(models.Model):
    album = models.ForeignKey(Album)
    gphoto_id = models.BigIntegerField(_('구글 포토 사진 ID'), null=False, blank=False, db_index=True)
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    description = models.TextField(_('설명'), null=True, blank=True)
    image_url = models.CharField(_('작은 이미지 주소'), max_length=255, null=False, blank=False)
    image_2048_url = models.CharField(_('최대 2048 사이즈 이미지 주소'), max_length=255, null=False, blank=False)
    image_origin_url = models.CharField(_('원본 이미지 주소'), max_length=255, null=False, blank=False)
    date = models.DateTimeField(_('시간'), null=False, blank=False)
    pub_date = models.DateTimeField(_('등록 날짜'), null=False, blank=True)
    update_date = models.DateTimeField(_('수정 날짜'), null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = _('사진')
        verbose_name_plural = _('사진')
