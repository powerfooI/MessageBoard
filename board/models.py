from django.db import models

# Create your models here.

class Message(models.Model):
    def __str__(self):
        suffix = ''
        if len(self.message_text) > 30:
            suffix = '...'
        return '(' + str(self.send_time.date()) + ')' + self.message_text[:30] + suffix

    message_text = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    wechat_id = models.CharField(max_length=64)
    response_text = models.TextField(null=True, blank=True)
    is_checked = models.BooleanField(default=False)
