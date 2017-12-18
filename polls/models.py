from django.db import models
from django.utils import timezone
import datetime


# Create your models here.


class Question(models.Model):
    question_text = models.CharField(verbose_name='質問文', max_length=200)
    pub_date = models.DateTimeField(verbose_name='発行日')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    class Meta:
        verbose_name = verbose_name_plural = "質問"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = verbose_name_plural = "選択肢"
