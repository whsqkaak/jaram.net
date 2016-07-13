from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.models import Member


class BaseBoardModel(models.Model):
    writer = models.ForeignKey(Member)
    write_date = models.DateTimeField(_('작성일'), null=False, blank=False, default=timezone.now)
    title = models.CharField(_('제목'), max_length=255, null=True, blank=True, default='')
    content = models.TextField(_('내용'), null=False, blank=False)
    attachment = models.FileField(_('첨부 파일'), upload_to='board/attachment/', null=True, blank=True)

    # TODO: 연관 일정

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class PlayStorming(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('플레이스토밍')
        verbose_name_plural = _('플레이스토밍')


class PlayStormingComment(BaseBoardModel):
    board = models.ForeignKey(PlayStorming)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('플레이스토밍 댓글')
        verbose_name_plural = _('플레이스토밍 댓글')


class Seminar(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('세미나')
        verbose_name_plural = _('세미나')


class SeminarComment(BaseBoardModel):
    board = models.ForeignKey(Seminar)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('세미나 댓글')
        verbose_name_plural = _('세미나 댓글')


class EventReport(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('행사보고')
        verbose_name_plural = _('행사보고')


class EventReportComment(BaseBoardModel):
    board = models.ForeignKey(EventReport)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('행사보고 댓글')
        verbose_name_plural = _('행사보고 댓글')


class Announcement(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('공지사항')
        verbose_name_plural = _('공지사항')


class GraduatingBoard(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('졸업생게시판')
        verbose_name_plural = _('졸업생게시판')


class GraduatingBoardComment(BaseBoardModel):
    board = models.ForeignKey(GraduatingBoard)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('졸업생게시판 댓글')
        verbose_name_plural = _('졸업생게시판 댓글')


class StudentBoard(BaseBoardModel):
    class Meta:
        ordering = ['-write_date']
        verbose_name = _('재학생게시판')
        verbose_name_plural = _('재학생게시판')


class StudentBoardComment(BaseBoardModel):
    board = models.ForeignKey(StudentBoard)

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('재학생게시판 댓글')
        verbose_name_plural = _('재학생게시판 댓글')

#TODO: reply 모델, 뷰 만들기