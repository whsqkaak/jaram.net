from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.models import Member
from main.utils.validator import file_size


class Semester(models.Model):
    name = models.CharField(_('학기 이름'), max_length=32, null=False, blank=False,
                            help_text="Please use the following format: <em>YYYY년도 N학기</em>.")
    date = models.DateField(_('스터디 학기 등록일'), null=False, blank=False, default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = _('스터디 학기')
        verbose_name_plural = _('스터디 학기')


class Study(models.Model):
    semester = models.ForeignKey(Semester, related_name='semester_of_study')
    leader = models.ForeignKey(Member, related_name='created_study_set')
    members = models.ManyToManyField(Member, related_name='study_set')
    image = models.ImageField(_('대표 이미지'), upload_to='study/main_image/', null=False, blank=False)
    name = models.CharField(_('스터디 이름'), max_length=32, null=False, blank=False)
    description = models.CharField(_('간략한 설명'), max_length=64, null=False, blank=False)
    content = models.TextField(_('계획, 기간 등 상세한 설명'), null=False, blank=False)
    date = models.DateField(_('스터디 등록일'), null=False, blank=False, default=timezone.now)
    attachment = models.FileField(_('첨부 파일'), upload_to='study/attachment/', validators=[file_size], null=True, blank=True)
    is_active = models.BooleanField(_('진행 여부'), null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date']
        verbose_name = _('스터디')
        verbose_name_plural = _('스터디')


class StudyReport(models.Model):
    writer = models.ForeignKey(Member)
    study = models.ForeignKey(Study)
    write_date = models.DateTimeField(_('작성일'), null=False, blank=False, default=timezone.now)
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    content = models.TextField(_('내용'), null=False, blank=False)
    attachment = models.FileField(_('첨부 파일'), upload_to='study/report/attachment/', null=True, blank=True)

    def __str__(self):
        return self.study.name + ' - ' + self.title

    class Meta:
        ordering = ['-write_date']
        verbose_name = _('스터디 보고서')
        verbose_name_plural = _('스터디 보고서')