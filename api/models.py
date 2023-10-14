from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  task=models.CharField(max_length=200)
  tocompleted_date=models.DateField()
  completed=models.BooleanField(default=False)
  created=models.DateField(auto_now_add=True)

  def __str__(self):
    return self.task
