from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Articles, Comment


def news(request):
    page = request.GET.get('page')
    if page:
        page = int(page) - 1
    else:
        page = 0
    articles = Articles.objects.all().order_by('-created_at')
    carousel_articles, another_articles = articles[page * 11:page * 11 + 3], articles[page * 11 + 3:page * 11 + 8]
    attrs = {'carousel_articles': carousel_articles, 'another_articles': another_articles, 'page': page,
             'pred_page': page - 1, 'next_page': page + 1}
    return render(request, 'news/news.html', attrs)


@login_required
def news_detail(request, news_id):
    news = get_object_or_404(Articles, id=news_id)
    count_likes = news.liked_by.count()

    news.count_likes = count_likes
    news.save()

    user_liked = request.user in news.liked_by.all()
    comments = Comment.objects.filter(news=news)
    count_comments = comments.count()

    return render(request, 'news/id_news.html', {
        'news': news,
        'user_liked': user_liked,
        'comments': comments,
        'count_comments': count_comments
    })


@login_required
def add_comment(request, news_id):
    if request.method == 'POST':
        news = get_object_or_404(Articles, id=news_id)
        comment_content = request.POST.get('comment')
        if comment_content:
            Comment.objects.create(user=request.user, news=news, content=comment_content)
            news.count_comments = Comment.objects.filter(news=news).count()
            news.save()
        return redirect('news_detail', news_id=news.id)


@login_required
def delete_comment(request, comment_id):
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            news = comment.news
            comment.delete()
            news.count_comments = Comment.objects.filter(news=news).count()
            news.save()
            updated_count = news.count_comments
            return JsonResponse({'success': True, 'count_comments': updated_count})
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


@login_required
def like_post(request, news_id):
    news = get_object_or_404(Articles, id=news_id)
    if request.user in news.liked_by.all():
        news.liked_by.remove(request.user)
        liked = False
    else:
        news.liked_by.add(request.user)
        liked = True
    count_likes = news.liked_by.count()
    news.count_likes = count_likes
    news.save()

    return JsonResponse({'likes': count_likes, 'liked': liked})
