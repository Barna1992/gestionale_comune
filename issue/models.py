from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

STATUS_CHOICES = (
    (1, _("Inserita")),
    (2, _("Presa in carico")),
    (3, _("Risolta")),
    (4, _("Riaperta")),
    (5, _("Da verificare"))
)
RELEVANCE_CHOICES = (
    (1, _("Bassa")),
    (2, _("Media")),
    (3, _("Alta")),
)


# class User(models.Model):
# 	first_name = models.CharField(max_length=30)
# 	last_name = models.CharField(max_length=30)
# 	email = models.EmailField(max_length=50)
#
# 	def __str__(self):
# 	   return '{} {}'.format(self.first_name, self.last_name)
class Issue(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateTimeField(auto_now=True)
	assignee = models.ManyToManyField(User)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', null=True, blank=True)
	description = models.TextField()
	state = models.IntegerField(choices=STATUS_CHOICES, default=1)
	priority = models.IntegerField(choices=RELEVANCE_CHOICES, default=2)
	expired_date = models.DateField(auto_now=False, null=True, blank=True)

	def __str__(self):
		return '{}'.format(self.title)

	def get_absolute_url(self):
		return reverse('issue-detail', kwargs={'pk': self.pk})

	def priority_verbose(self):
		return dict(RELEVANCE_CHOICES)[self.priority]

	def state_verbose(self):
		return dict(STATUS_CHOICES)[self.state]

class Comment(models.Model):
    post = models.ForeignKey(Issue,on_delete=models.CASCADE,related_name='comments')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_comments', null=True, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
