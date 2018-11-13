from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from . import forms
from . import models


def home(request):
    with open("posts/sites/index.html", "r") as f:
        data = f.read()
    return HttpResponse(data)


@user_passes_test(lambda u: u.is_superuser, login_url="/notadmin/")
def admin(request):
    with open("posts/sites/admin.html", "r") as f:
        data = f.read()
    return HttpResponse(data)


def admin_input(request):
    if request.method == "POST":
        form = forms.PostForm(request.POST)

        if form.is_valid():
            # Save the object
            # Check if there is any media
            data = form.cleaned_data
            if data["mediaSrc"]:
                media = models.Media.objects.create(kind="image", src=data["mediaSrc"])
                models.Post.objects.create(
                    author=data["author"], platform=data["platform"],
                    caption=data["caption"], media=media)
            else:
                models.Post.objects.create(
                    author=data["author"], platdata=data["platdata"],
                    caption=data["caption"], media=media)
            return render(request, "posts/admin_input.html", {"form": form, "success": True})
    else:
        form = forms.PostForm()
        return render(request, "posts/admin_input.html", {"form": form})
