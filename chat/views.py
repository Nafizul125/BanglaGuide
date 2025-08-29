from django.shortcuts import render
from .models import Post

def chat(request):
    posts = (Post.objects
                .select_related("user")
                .prefetch_related("replies__user")
                .order_by("-timestamp")[:30])
    return render(request, "chat.html", {
        "posts": posts,
        "is_authed": request.user.is_authenticated,
    })
