from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hero(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=400)

	def __str__(self):
		return self.name