from django.db import models
from accounts.models import User
from django.db.models import Q, F


class Benefactor(models.Model):
    STATUS_CHOICE = (
        (0, 0),
        (1, 1),
        (2, 2)
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.SmallIntegerField(choices=STATUS_CHOICE, default=0)
    free_time_per_week = models.PositiveIntegerField(default=0)


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    reg_number = models.CharField(max_length=10)


class TaskManager(models.Manager):
    def related_tasks_to_charity(self, user):
        return Task.objects.filter(charity__user__exact=user)

    def related_tasks_to_benefactor(self, user):
        return Task.objects.filter(assigned_benefactor__user__exact=user)

    def all_related_tasks_to_user(self, user):
        return Task.objects.filter(
            Q(assigned_benefactor__user__exact=user) | Q(charity__user__exact=user)
            | Q(state__iexact='P')
                                   )


class Task(models.Model):
    GENDER_CHOICE = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    STATE_CHOICE = (
        ('P', "Pending"),
        ('W', "Waiting"),
        ('A', "Assigned"),
        ('D', 'Done')
    )
    assigned_benefactor = models.ForeignKey(Benefactor, null=True, on_delete=models.SET_NULL)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, null=True)
    age_limit_from = models.IntegerField(null=True, blank=True)
    age_limit_to = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    gender_limit = models.CharField(max_length=1, choices=GENDER_CHOICE, null=True, blank=True)
    state = models.CharField(max_length=1, choices=STATE_CHOICE, default='P')
    title = models.CharField(max_length=60)
    objects = TaskManager()

