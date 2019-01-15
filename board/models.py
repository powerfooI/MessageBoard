from django.db import models

# Create your models here.


class Message(models.Model):
    def __str__(self):
        return self.send_time.date()

    message_text = models.TextField()
    send_time = models.DateTimeField()
    wechat_id = models.CharField(max_length=64)
    response_text = models.TextField(null=True, blank=True)
