from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.shortcuts import redirect
 

# Create your views here.
def post_list(request):
    posts = Post.objects.all #filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    done = False
    if request.method == 'POST':        
        form = CommentForm(request.POST)
        if form.is_valid():             
            com = form.save(commit=False)  
            if request.POST.get('parent',None):
               com.parent_id = int(request.POST.get('parent'))          
            com.post = post 
            com.created_date = timezone.now()       
            com.save()
            done = True

    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html',  {'post': post,'form': form , 'done':done })




def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

 