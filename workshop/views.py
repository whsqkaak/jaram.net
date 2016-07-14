from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import View, TemplateView
from main.models import Member
from main.util import create_response
from workshop.models import WorkShop ,WorkShopTask, WorkShopTaskSubmission


class WorkShopListView(TemplateView):
    template_name = 'workshop/list.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['page'] = WorkShop.objects.all()
        return render(request, self.template_name, response)


class WorkShopRegistrationView(TemplateView):
    template_name = 'workshop/registration.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, create_response(request))

    def post(self, request, *args, **kwargs):
        data = request.POST

        if not (data.get('start_date') and data.get('end_date') and data.get('subject') and data.get('content')):
            return redirect('/workshop/registration/?error=워크샵 등록에 필요한 정보가 부족합니다.')

        workshop = WorkShop()
        workshop.start_date = data.get('start_date')
        workshop.end_date = data.get('end_date')
        workshop.content = data.get('content')
        workshop.subject = data.get('subject')

        workshop.save()

        return redirect('/workshop?success=성공적으로 등록되었습니다.')


class WorkShopDetailView(TemplateView):
    template_name = 'workshop/detail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        try:
            workshop = WorkShop.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵입니다.')

        response['workshop'] = workshop
        return render(request, self.template_name, response)


class WorkShopTaskListView(TemplateView):
    template_name = 'workshop/taskList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        response['tasks'] = WorkShopTask.objects.all()
        return render(request, self.template_name, response)


class WorkShopTaskRegistrationView(TemplateView):
    template_name = 'workshop/taskRegistration.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST

        if not (data.get('title') and data.get('content') and data.get('deadline') and data.get('duty_member') ):
            return redirect('/workshop/taskList/taskRegistration/?error=워크샵 과제 등록에 필요한 정보가 부족합니다.')

        workshoptask = WorkShopTask()
        workshoptask.title = data.get('title')
        workshoptask.content = data.get('content')
        workshoptask.deadline = data.get('deadline')

        workshoptask.save()

        for member in Member.objects.filter(pk__in=data.get('member').split(',')).all():
            workshoptask.duty_member.add(member)

        workshoptask.save()

        return redirect('/workshop/taskList?success=성공적으로 등록되었습니다.')


class WorkShopTaskSubmissionView(TemplateView):
    template_name = 'workshop/taskSubmission.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵입니다.')

        response['workshop_task'] = workshop_task
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST

        try:
            task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵 과제입니다.')

        if not (data.get('content')):
            return redirect('/workshop/taskList/?error=과제 제출에 필요한 정보가 부족합니다.')

        submission_task = WorkShopTaskSubmission()
        submission_task.task = task
        submission_task.presenter = request.user
        submission_task.content = data.get('content')
        submission_task.attachment = request.FILES.get('attachment')
        submission_task.save()
        return redirect('workshop_taskDetail', id=task.pk)
        # TODO : 성공 메시지 출력


class WorkShopTaskDetailView(TemplateView):
    template_name = 'workshop/taskDetail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵입니다.')

        response['workshop_task'] = workshop_task
        response['members'] = workshop_task.duty_member.all()
        return render(request, self.template_name, response)


class WorkShopTaskSubmissionListView(TemplateView):
    template_name = 'workshop/taskSubmissionList.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')

        response['workshop_task'] = workshop_task
        response['tasks'] = WorkShopTaskSubmission.objects.filter(task=workshop_task)
        return render(request, self.template_name, response)


class WorkShopTaskSubmissionDetailView(TemplateView):
    template_name = 'workshop/taskSubmissionDetail.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')

        try:
            workshop_taskSubmission = WorkShopTaskSubmission.objects.get(pk=kwargs.get('task_id'))
        except ObjectDoesNotExist:
            return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')

        response['workshop_task'] = workshop_task
        response['workshop_taskSubmission'] = workshop_taskSubmission
        return render(request, self.template_name, response)


class WorkShopTaskUpdateView(TemplateView):
    template_name = 'workshop/taskUpdate.html'

    def get(self, request, *args, **kwargs):
        response = create_response(request)

        try:
            workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵입니다.')

        response['workshop_task'] = workshop_task

        try:
            workshop_taskSubmission = WorkShopTaskSubmission.objects.get(pk=kwargs.get('task_id'))
        except ObjectDoesNotExist:
            return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')

        response['workshop_taskSubmission'] = workshop_taskSubmission
        return render(request, self.template_name, response)

    def post(self, request, *args, **kwargs):
        data = request.POST

        try:
            task = WorkShopTask.objects.get(pk=kwargs.get('id'))
        except ObjectDoesNotExist:
            return redirect('/workshop?error=존재하지 않는 워크샵 과제입니다.')

        if not (data.get('content')):
            return redirect('/workshop/taskList/?error=과제 제출에 필요한 정보가 부족합니다.')
        try:
            submission_task = WorkShopTaskSubmission.objects.get(pk=kwargs.get('task_id'))
        except ObjectDoesNotExist:
            return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')

        submission_task.task = task
        submission_task.presenter = request.user
        submission_task.content = data.get('content')
        submission_task.attachment = request.FILES.get('attachment')
        submission_task.__class__.objects.filter(id=task.pk).update()
        submission_task.save()
        return redirect('workshop_taskSubmissionDetail', id=task.pk ,task_id=submission_task.pk)
