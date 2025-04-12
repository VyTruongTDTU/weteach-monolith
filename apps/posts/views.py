from django.shortcuts import render
from django.views.generic import TemplateView
from apps.posts.models import Post, Course
from apps.users.models import TeacherProfile

class HomePageView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured posts
        context['featured_posts'] = Post.objects.filter(
            status=Post.STATUS_POSTED
        ).order_by('-created_at')[:6]
        
        # Featured teachers
        context['featured_teachers'] = TeacherProfile.objects.filter(
            is_verified=True
        ).order_by('?')[:4]  # Random selection
        
        # Popular courses
        context['popular_courses'] = Course.objects.all()[:8]
        
        return context
    