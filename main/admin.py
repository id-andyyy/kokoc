from django.contrib import admin
from .models import Articles, Matches, Team, Shop, Comment, NextMatches


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'likes')
    list_display_links = ('id', 'title')


class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'opponent', 'tournament', 'date')
    list_display_links = ('id', 'opponent')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'position', 'is_active', 'tshirt_number')
    list_display_links = ('id', 'name')
    list_filter = ('position', 'is_active')


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_display_links = ['id']


class NextMatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'opponent', 'tournament', 'date')
    list_display_links = ('id', 'opponent')


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Matches, MatchesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(NextMatches, NextMatchesAdmin)
