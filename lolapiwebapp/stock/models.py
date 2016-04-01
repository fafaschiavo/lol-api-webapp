from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Hero(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	title = models.CharField(max_length=400)
	key = models.CharField(max_length=200, default = '-')

	def __str__(self):
		return self.name

	def __key__(self):
		return self.key

class mastery(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	position = models.IntegerField(default=0)

	def __str__(self):
		return self.name

	def __position__(self):
		return self.position

class Rune(models.Model):
	id_riot = models.IntegerField(default=0)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=400)
	tier = models.IntegerField(default=0)
	rune_type = models.CharField(max_length=200)
	bonus = models.DecimalField(max_digits=6, decimal_places=2)
	honest_text = models.CharField(max_length=200)
	is_percentage = models.IntegerField(default=0)

	def __str__():
		return self.name

	def __description__():
		return self.description

	def __rune_type__():
		return self.rune_type

	def __bonus__():
		return self.bonus

	def __honest_text__():
		return self.honest_text

	def __is_percentage__():
		return self.is_percentage