from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .models import Board, Post, Topic
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    boards = Board.objects.all()

    return render(request, 'home.html', {'boards': boards})


def boards_topic(request, id):
    board = get_object_or_404(Board, pk=id)
    return render(request, 'topic.html', {'board': board})


@login_required
def new_topic(request, id):
    board = get_object_or_404(Board, pk=id)
    # user = User.objects.first()
    user = request.user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = user
            topic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'), topic=topic, created_by=user)
        return redirect('boards_topic', id=board.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, id,  topic_id):
    topic = get_object_or_404(Topic, board__pk=id, pk=topic_id)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, id, topic_id):
    topic = get_object_or_404(Topic, board__pk=id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', id=id, topic_id=topic.pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
