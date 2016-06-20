from django.core.management import BaseCommand
from main.models import Grade, Member


class Command(BaseCommand):
    help = 'init server'

    def handle(self, *args, **options):
        self.init_grade()
        self.init_admin()

    def init_grade(self):
        Grade(name='OB').save()
        Grade(name='준OB').save()
        Grade(name='정회원').save()
        Grade(name='준회원').save()
        Grade(name='수습회원').save()

    def init_admin(self):
        admin = Member()
        admin.user_id = 'admin'
        admin.name = '관리자'
        admin.email = 'admin@jaram.net'
        admin.period = 0
        admin.enter_year = 00
        admin.grade = Grade.objects.get(name='정회원')
        admin.is_active = True
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password('Jaram@2016Admin')
        admin.save()
