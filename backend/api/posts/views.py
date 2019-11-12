import json
from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models
from . import telegram_bot


def home(request):
    with open("posts/sites/index.html", "r") as f:
        data = f.read()
    return HttpResponse(data)


@user_passes_test(lambda u: u.is_superuser, login_url="/notadmin/")
def admin(request):
    with open("posts/sites/admin.html", "r") as f:
        data = f.read()
    return HttpResponse(data)


@user_passes_test(lambda u: u.is_superuser, login_url="/notadmin/")
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


@csrf_exempt
def telegram_webhook(request):
    if request.method != "POST":
        return

    token = settings.TELEGRAM_BOT_TOKEN
    json_request = json.loads(request.body)

    message = json_request["message"]
    message_id = models.int_id_to_str(message["message_id"])
    chat_id = models.int_id_to_str(message["chat"]["id"])
    unique_id = f"{message_id}_{chat_id}"

    # Rate limit the requests
    last_post_by_user = models.Post.objects.filter(
        post_id__startswith=chat_id,
        platform=models.SocialPlatform.Telegram,
    ).order_by("date")[0]

    current_time = datetime.now()
    timedelta = last_post_by_user.date - current_time
    if timedelta.total_seconds() < 5*60:
        # Exceeded rate limit. Ignore the request
        message = ("The bot has been rate limited to prevent spam. Please "
            "wait for a while before sending again.")
        telegram_bot.send_message(token, chat_id, message)
        return

    # Download the image
    photo = message["photo"]
    file_path = None
    if photo:
        file_id = photo[-1]['file_id']
        filename = telegram_bot.download_image(
            token, file_id, settings.MEDIA_URL)
        file_path = f'{settings.STATIC_URL}{filename}'

    # Save the request into the DB
    date = message["date"]
    author = message['from']['first_name']
    caption = message.get("caption", message.get("text", ""))

    models.Post.objects.create(
        post_id=unique_id, platform=models.SocialPlatform.Telegram,
        date=datetime.fromtimestamp(date),
        author=author, caption=caption, kind=models.ContentType.Image,
        src=file_path
    )
