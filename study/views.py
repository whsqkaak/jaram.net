from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View, TemplateView
from django.db.models.query import EmptyQuerySet
from main.models import Member, Grade
from main.util import create_response
from study.models import Study, StudyReport, Semester


class StudyListView(TemplateView):
    template_name = 'list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        try:
            semesters = Semester.objects.all()
            response['semesters'] = semesters
        except ObjectDoesNotExist:
            return redirect('/main?error=스터디 학기가 존재하지 않습니다.')
        semester = semesters[int(request.GET.get('semester', 0))]
        response['semester'] = semester
        response['page'] = Study.objects.filter(semester=semester).filter(is_active=True).all()
        return render(request, self.template_name, response)


class StudyDetailView(TemplateView):
    template_name = 'detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        try:
            study = Study.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/study?error=존재하지 않는 스터디입니다.')

        response['study'] = study
        response['reports'] = study.studyreport_set.order_by('-write_date').all()
        response['members'] = study.members.all()

        return render(request, self.template_name, response)


class StudyReportView(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        try:
            study = Study.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/study?error=존재하지 않는 스터디입니다.')
        
        if request.user not in study.members.all():
            return redirect('/study/%s?error=스터디 멤버만 보고서 작성이 가능합니다.' % kwargs.get('id'))
        response['study'] = study
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST

        try:
            study = Study.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/study?error=존재하지 않는 스터디입니다.')

        if not (data.get('title') and data.get('content')):
            return redirect('/study?error=입력된 정보가 올바르지 않습니다.')

        StudyReport(writer=request.user,
                    study=study,
                    write_date=timezone.now(),
                    title=data.get('title'),
                    content=data.get('content'),
                    attachment=request.FILES.get('attachment')).save()

        return redirect('/study?success=성공적으로 등록되었습니다.')


class StudyRegistrationView(TemplateView):
    template_name = 'registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.grade == Grade.objects.get(name='미승인'):
            return redirect('/main?warning=권한이 없습니다.')
        return render(request, self.template_name, create_response(request))

    def post(self, request, *args, **kwargs):
        data = request.POST
        file = request.FILES

        if not (data.get('name') and data.get('description') and data.get('member')
                and data.get('content') and file.get('image')):
            return redirect('/study/registration/?error=스터디 등록 신청에 필요한 정보가 부족합니다.')

        study = Study()
        study.leader = request.user
        study.name = data.get('name')
        study.description = data.get('description')
        study.content = data.get('content')
        study.image = file.get('image')

        study.save()

        for member in Member.objects.filter(pk__in=data.get('member').split(',')).all():
            study.members.add(member)

        study.save()

        return redirect('/study?success=성공적으로 등록되었습니다.')


class SearchUserApiView(View):
    def get(self, request, *args, **kwargs):
        response = dict()
        response_results = list()
        response['results'] = response_results

        if not request.GET.get('query'):
            return JsonResponse(response)

        result = Member.objects.filter(grade__name__in=['수습부원', '준회원', '정회원', '준OB']) \
            .filter(name__icontains=request.GET.get('query'))

        for member in result.all():
            member_dict = dict()
            member_dict['id'] = member.pk
            member_dict['title'] = member.name
            if member.profile:
                member_dict['image'] = member.profile.url
            else:
                member_dict['image'] = static('mainapp/img/profile_default.png')
            member_dict['price'] = '%d기' % member.period
            member_dict['description'] = member.grade.name
            response_results.append(member_dict)
        print(response)
        return JsonResponse(response)
