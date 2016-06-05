from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from main.util import create_response
from study.models import Study, StudyReport


class StudyListView(TemplateView):
    template_name = 'list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['page'] = Study.objects.filter(is_active=True).all()
        return render(request, self.template_name, response)


class StudyDetailView(TemplateView):
    template_name = 'detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
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
            response['study'] = Study.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/study?error=존재하지 않는 스터디입니다.')

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
