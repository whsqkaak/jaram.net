from django.core.exceptions import ValidationError


def file_size(value):
	limit = 20 * 1024 * 1024
	if value.size > limit:
		raise ValidationError('첨부파일의 크기는 20MB 이하여야 합니다.')