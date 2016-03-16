from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hero(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=400)

	def __str__(self):
		return self.name

class mastery(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	position = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def __position__(self):
		return self.position