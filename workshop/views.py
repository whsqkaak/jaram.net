from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, redirect
from django.utils.datetime_safe import date
from django.views.generic import View, TemplateView
from main.models import Member, Grade
from main.util import create_response
from workshop.models import WorkShop, WorkShopTask, WorkShopTaskSubmission


class WorkShopView(TemplateView):
	def get(self, request, *args, **kwargs):
		today = date.today()
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
		try:
			ongoing_workshop = WorkShop.objects.get(
				end_date__gte=today,
				start_date__lte=today)
		except ObjectDoesNotExist:
			return redirect('workshop')
		
		return redirect('workshop_detail', id=ongoing_workshop.pk)


class WorkShopListView(TemplateView):
	template_name = 'workshop/list.html'
	
	def get(self, request, *args, **kwargs):
		response = create_response(request)
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
		response['page'] = WorkShop.objects.all()
		return render(request, self.template_name, response)


class WorkShopRegistrationView(TemplateView):
	template_name = 'workshop/registration.html'
	
	def get(self, request, *args, **kwargs):
		
		if not (request.user.is_staff or request.user.is_superuser):
			return redirect('/workshop?error=워크샵 등록 권한이 존재하지 않습니다.')
		
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
		
		try:
			workshop.save()
		except ValidationError:
			return redirect('/workshop/registration/?warning=날짜 형식을 맞추십시오.')
		
		return redirect('/workshop?success=성공적으로 등록되었습니다.')


class WorkShopDetailView(TemplateView):
	template_name = 'workshop/detail.html'
	
	def get(self, request, *args, **kwargs):
		response = create_response(request)
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
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
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
		response['tasks'] = WorkShopTask.objects.all()
		return render(request, self.template_name, response)


class WorkShopTaskRegistrationView(TemplateView):
	template_name = 'workshop/taskRegistration.html'
	
	def get(self, request, *args, **kwargs):
		
		if not (request.user.is_staff and request.user.is_superuser):
			return redirect('/workshop/taskList?error=과제 등록 권한이 존재하지 않습니다.')
		
		response = create_response(request)
		return render(request, self.template_name, response)
	
	def post(self, request, *args, **kwargs):
		data = request.POST
		
		if not (data.get('title') and data.get('content') and data.get('deadline')):
			return redirect('/workshop/taskList/taskRegistration/?error=워크샵 과제 등록에 필요한 정보가 부족합니다.')
		
		workshoptask = WorkShopTask()
		workshoptask.title = data.get('title')
		workshoptask.content = data.get('content')
		workshoptask.deadline = data.get('deadline')
		
		try:
			workshoptask.save()
		except ValidationError:
			return redirect('/workshop/taskList/taskRegistration/?warning=날짜 형식을 맞추십시오.')
		
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
		
		task_duty = False
		for member in workshop_task.duty_member.all():
			if request.user == member:
				task_duty = True
				break
		
		if not task_duty:
			return redirect('/workshop/taskList/%s?error=과제 의무자가 아닙니다.' % kwargs.get('id'))
		
		response['workshop_task'] = workshop_task
		return render(request, self.template_name, response)
	
	def post(self, request, *args, **kwargs):
		data = request.POST
		
		try:
			task = WorkShopTask.objects.get(pk=kwargs.get('id'))
		except ObjectDoesNotExist:
			return redirect('/workshop/taskList/?error=존재하지 않는 워크샵 과제입니다.')
		
		if not (data.get('content')):
			return redirect('/workshop/taskList/%s/taskSubmission?error=과제 제출에 필요한 정보가 부족합니다.' % kwargs.get('id'))
		
		submission_task = WorkShopTaskSubmission()
		submission_task.task = task
		submission_task.presenter = request.user
		submission_task.content = data.get('content')
		submission_task.attachment = request.FILES.get('attachment')
		submission_task.save()
		return redirect('/workshop/taskList/%s/taskSubmissionList' % kwargs.get('id'))


class WorkShopTaskDetailView(TemplateView):
	template_name = 'workshop/taskDetail.html'
	
	def get(self, request, *args, **kwargs):
		response = create_response(request)
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
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
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
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
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
		try:
			workshop_task = WorkShopTask.objects.get(pk=kwargs.get('id'))
		except ObjectDoesNotExist:
			return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')
		
		try:
			workshop_taskSubmission = WorkShopTaskSubmission.objects.get(pk=kwargs.get('task_id'))
		except ObjectDoesNotExist:
			return redirect('/workshop/taskList?error=존재하지 않는 워크샵입니다.')
		
		# 첨부파일 경로 편집
		if workshop_taskSubmission.attachment:
			response['attachment_name'] = workshop_taskSubmission.attachment.name.split("/")[2]
		
		response['workshop_task'] = workshop_task
		response['workshop_taskSubmission'] = workshop_taskSubmission
		return render(request, self.template_name, response)


class WorkShopTaskUpdateView(TemplateView):
	template_name = 'workshop/taskUpdate.html'
	
	def get(self, request, *args, **kwargs):
		response = create_response(request)
		if request.user.grade == Grade.objects.get(name='미승인'):
			return redirect('/main?warning=권한이 없습니다.')
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
			return redirect('/workshop/taskList/%s/taskUpdate?error=과제 제출에 필요한 정보가 부족합니다.' % kwargs.get('id'))
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
		return redirect('workshop_taskSubmissionDetail', id=task.pk, task_id=submission_task.pk)
