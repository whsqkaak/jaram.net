def create_response(request):
    return dict(
        user=request.user,
        message=request.GET.get('message'),
        success=request.GET.get('success'),
        warning=request.GET.get('warning'),
        error=request.GET.get('error'),
    )
