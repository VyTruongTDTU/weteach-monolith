from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager for CustomUser."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with the given email and password."""
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model where email is the unique identifier for authentication."""
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class LearnerProfile(models.Model):
    """Profile model for learners."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='learner_profile')
    bio = models.TextField(_('bio'), blank=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    address = models.CharField(_('address'), max_length=255, blank=True)

    def __str__(self):
        return f"Learner Profile: {self.user.email}"


class TeacherProfile(models.Model):
    """Profile model for teachers."""
    learner_profile = models.OneToOneField(LearnerProfile, on_delete=models.CASCADE, related_name='teacher_profile')
    qualifications = models.TextField(_('qualifications'), blank=True)
    experience = models.TextField(_('experience'), blank=True)
    is_verified = models.BooleanField(_('verified teacher'), default=False)

    def __str__(self):
        return f"Teacher Profile: {self.learner_profile.user.email}"