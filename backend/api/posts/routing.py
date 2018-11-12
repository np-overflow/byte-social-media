from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/posts/$', consumers.PostConsumer),
    url(r'^ws/admin/$', consumers.AdminPostConsumer),
]
