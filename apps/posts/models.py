# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from apps.users.models import CustomUser, TeacherProfile

class Course(models.Model):
    """Course model representing subjects that can be taught"""
    name = models.CharField(_('course name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    """Model for hiring posts created by learners"""
    # Status choices for the post
    STATUS_DRAFT = 'draft'
    STATUS_POSTED = 'posted'
    STATUS_TEACHER_CHOSEN = 'teacher-chosen'
    STATUS_TEACHER_RESPONDED = 'teacher-responded'
    STATUS_MATCHED = 'matched'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_POSTED, _('Posted')),
        (STATUS_TEACHER_CHOSEN, _('Teacher Chosen')),
        (STATUS_TEACHER_RESPONDED, _('Teacher Responded')),
        (STATUS_MATCHED, _('Matched')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Frequency choices for teaching sessions
    FREQUENCY_ONCE = 'once'
    FREQUENCY_DAILY = 'daily'
    FREQUENCY_WEEKLY = 'weekly'
    FREQUENCY_BIWEEKLY = 'biweekly'
    FREQUENCY_MONTHLY = 'monthly'
    
    FREQUENCY_CHOICES = [
        (FREQUENCY_ONCE, _('One-time')),
        (FREQUENCY_DAILY, _('Daily')),
        (FREQUENCY_WEEKLY, _('Weekly')),
        (FREQUENCY_BIWEEKLY, _('Bi-weekly')),
        (FREQUENCY_MONTHLY, _('Monthly')),
    ]
    
    # Basic post information
    title = models.CharField(_('title'), max_length=200)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    # Teaching details
    courses = models.ManyToManyField(Course, related_name='posts', verbose_name=_('teaching courses'))
    preferred_start_date = models.DateField(_('preferred start date'))
    preferred_start_time = models.TimeField(_('preferred start time'))
    duration_minutes = models.IntegerField(_('duration in minutes'), default=60)
    frequency = models.CharField(_('frequency'), max_length=20, choices=FREQUENCY_CHOICES, default=FREQUENCY_ONCE)
    number_of_sessions = models.IntegerField(_('number of sessions'), default=1)
    
    # Location
    teaching_place = models.CharField(_('teaching place'), max_length=255)
    is_online = models.BooleanField(_('is online'), default=False)
    
    # Financial details
    teaching_fee = models.DecimalField(_('teaching fee'), max_digits=10, decimal_places=2)
    is_hourly_rate = models.BooleanField(_('is hourly rate'), default=True)
    
    # Requirements and description
    teacher_requirements = models.TextField(_('teacher requirements'), blank=True)
    description = models.TextField(_('description'), blank=True)
    
    # Relationships
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_posts',
        verbose_name=_('learner')
    )
    applying_teachers = models.ManyToManyField(
        TeacherProfile, 
        through='TeacherApplication',
        related_name='applied_posts',
        verbose_name=_('applying teachers')
    )
    chosen_teacher = models.ForeignKey(
        TeacherProfile, 
        on_delete=models.SET_NULL, 
        related_name='chosen_posts',
        null=True, 
        blank=True,
        verbose_name=_('chosen teacher')
    )
    
    # Status information
    status = models.CharField(_('status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    is_direct_request = models.BooleanField(_('is direct request'), default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('post')
        verbose_name_plural = _('posts')
    
    def __str__(self):
        return self.title


class TeacherApplication(models.Model):
    """Model for teacher applications to posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='applications')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='post_applications')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    message = models.TextField(_('message'), blank=True)
    proposed_fee = models.DecimalField(_('proposed fee'), max_digits=10, decimal_places=2, null=True, blank=True)
    is_selected = models.BooleanField(_('is selected'), default=False)
    
    class Meta:
        unique_together = ('post', 'teacher')
        ordering = ['-created_at']
        verbose_name = _('teacher application')
        verbose_name_plural = _('teacher applications')
    
    def __str__(self):
        return f"{self.teacher} application for {self.post}"


class PostFeedback(models.Model):
    """Model for feedback after a teaching session"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feedback')
    from_learner = models.BooleanField(_('from learner'), default=True)
    rating = models.PositiveSmallIntegerField(_('rating'), choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(_('comment'), blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('post feedback')
        verbose_name_plural = _('post feedback')
    
    def __str__(self):
        source = "Learner" if self.from_learner else "Teacher"
        return f"{source} feedback for {self.post}"