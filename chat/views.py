from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Reply
from .forms import PostForm, ReplyForm

@login_required
def chat(request):
    posts = Post.objects.all().order_by('-timestamp')
    if request.method == 'POST':
        if 'post_submit' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('chat')
        elif 'reply_submit' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.post_id = request.POST.get('post_id')
                reply.save()
                return redirect('chat')
    post_form = PostForm()
    reply_form = ReplyForm()
    return render(request, 'chat.html', {'posts': posts, 'post_form': post_form, 'reply_form': reply_form})