from django.db import models

class Movie(models.Model):
	sourceID=models.IntegerField()
	source=models.TextField()	
	year=models.TextField()
	title=models.TextField()
	numReviews=models.IntegerField()
	description=models.TextField()
	actors=models.TextField()