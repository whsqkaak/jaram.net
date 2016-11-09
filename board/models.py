from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.models import Member
from main.utils.validator import file_size


class BasePostModel(models.Model):
    writer = models.ForeignKey(Member)
    write_date = models.DateTimeField(_('작성일'), null=False, blank=False, default=timezone.now)
    title = models.CharField(_('제목'), max_length=255, null=True, blank=True, default='')
    content = models.TextField(_('내용'), null=False, blank=False, default='')
    attachment = models.FileField(_('첨부 파일'), upload_to='board/attachment/', validators=[file_size], null=True, blank=True)
    thumbnail = models.ImageField(_('미리보기'), upload_to='board/thumbnail/', null=True, blank=True)
    emphasis = models.BooleanField(_('게시글 강조'), default=False)
    hit = models.IntegerField(_('조회수'), default=0)
    # TODO: 연관 일정

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Board(models.Model):
    name = models.CharField(_('게시판 이름'), max_length=128, null=False, blank=False)
    eng_name = models.CharField(_('게시판 영어 이름'), max_length=128, null=False, blank=False, unique=True, db_index=True)
    usable_group = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('게시판')
        verbose_name_plural = _('게시판')


class Post(BasePostModel):
    board = models.ForeignKey(Board)

    def __str__(self):
        return self.board.name + ' - ' + self.title

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('게시글')
        verbose_name_plural = _('게시글')


class Comment(BasePostModel):
    board = models.ForeignKey(Board)
    post = models.ForeignKey(Post)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies')

    def __str__(self):
        return str(self.post) + ' - ' + self.title

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('댓글')
        verbose_name_plural = _('댓글')

# TODO: reply 모델, 뷰 만들기
