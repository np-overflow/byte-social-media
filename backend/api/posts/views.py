from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def home(request):
    with open("posts/sites/index.html", "r") as f:
        data = f.read()
    return HttpResponse(data)


@user_passes_test(lambda u: u.is_superuser, login_url="/notadmin/")
def admin(request):
    with open("posts/sites/admin.html", "r") as f:
        data = f.read()
    return HttpResponse(data)
