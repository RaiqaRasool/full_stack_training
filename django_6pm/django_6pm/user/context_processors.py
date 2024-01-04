from user.models import Profile


def profile(request):
    profile = None
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id)
    return {"profile": profile}
