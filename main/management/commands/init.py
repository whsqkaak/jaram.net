from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from main.models import Grade, Member


def create_grade(name):
    try:
        grade = Grade.objects.get(name=name)
    except ObjectDoesNotExist:
        grade = Grade(name=name)

    grade.group = Group.objects.get(name=name)
    grade.save()


def create_group(name, grant_permission_action=None):
    try:
        group = Group.objects.get(name=name)
    except ObjectDoesNotExist:
        group = Group(name=name)

    if grant_permission_action:
        group.save()
        grant_permission_action(group)
    group.save()


def grant_permission(group, app_label, models=None, exclude_models=None):
    permissions = Permission.objects.filter(content_type__app_label=app_label)

    if models:
        for model in models:
            permissions = permissions.filter(content_type__model=model)

    if exclude_models:
        for model in exclude_models:
            permissions = permissions.exclude(content_type__model=model)

    for permission in permissions:
        group.permissions.add(permission)


class Command(BaseCommand):
    help = 'init server'

    @staticmethod
    def grant_active_group(active):
        grant_permission(active, 'board', exclude_models=['eventreport'])
        grant_permission(active, 'schedule')
        grant_permission(active, 'study')
        grant_permission(active, 'workshop')

    def handle(self, *args, **options):
        self.init_group()
        self.init_grade()
        self.init_admin()

    def init_group(self):
        create_group('OB', lambda g: grant_permission(g, 'board', models=['Board']))
        create_group('준OB', lambda g: grant_permission(g, 'board', models=['Board']))
        create_group('정회원', lambda g: grant_permission(g, 'board', models=['Board']))
        create_group('준회원', lambda g: grant_permission(g, 'board', models=['Board']))
        create_group('수습회원')

        create_group('미승인')
        create_group('활동', Command.grant_active_group)
        create_group('비활동')

        create_group('임원진', lambda g: grant_permission(g, 'board', models=['eventreport']))

    def init_grade(self):
        create_grade('OB')
        create_grade('준OB')
        create_grade('정회원')
        create_grade('준회원')
        create_grade('수습회원')
        create_grade('미승인')

    def init_admin(self):
        try:
            admin = Member.objects.get(user_id='admin')
        except ObjectDoesNotExist:
            admin = Member(user_id='admin')

        admin.name = '관리자'
        admin.email = 'admin@jaram.net'
        admin.period = 0
        admin.enter_year = 00
        admin.grade = Grade.objects.filter(name='정회원')[0]
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('Jaram@2016Admin')
        admin.save()
