from django.shortcuts import render, get_object_or_404, reverse
from .models import Post
from django.views import generic, View
from django.http import HttpResponseRedirect


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 3


class DetailView(generic.DetailView):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "liked": liked
            },
        )


class PostLike(View):
    def post(self, request, slug):
           post = get_object_or_404(Post, slug=slug)
           if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
           else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))




    

