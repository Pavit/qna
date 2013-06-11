from django.db import models
from django.utils.translation import gettext as _
from django.template.defaultfilters import slugify
from core.models import UserProfile


class Question(models.Model):
	question = models.CharField(max_length=250)
	created = models.DateField(auto_now_add=True)
	modified = models.DateField(auto_now=True)
	submitter = models.ForeignKey(UserProfile, null=True, blank=True, default=None, related_name='submissions')
	answered_by = models.ManyToManyField(UserProfile, null=True, blank=True, default=None, related_name='answered')
	slug = models.SlugField(max_length=250, blank=True, null=True)

	class Meta:
		ordering = ['-created']
		verbose_name = _('question')
		verbose_name_plural = _('questions')

	def __unicode__(self):
		return u'%s' %(self.question)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.question)
		super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.CharField(max_length=250)
	selected_by = models.ManyToManyField(UserProfile, null=True, blank=True, default=None, related_name='selections')

	class Meta:
		verbose_name = _('answer')
		verbose_name_plural = _('answers')

	def __unicode__(self):
		return u'%s' %(self.answer)


class Vote(models.Model):
	voter = models.ForeignKey(UserProfile, null=True, blank=True, default=None, related_name='votes')
	answer = models.ForeignKey(Answer, related_name='votes')
	created = models.DateField(auto_now_add=True)

	class Meta:
	    verbose_name = _('vote')
	    verbose_name_plural = _('votes')
