from django.db import models

# Create your models here.
class RawLog(models.Model):
    phone_number = models.CharField(max_length=20)
    raw_text = models.CharField(max_length=2000)
    state = models.CharField(max_length=2)

    def __str__(self):
        return '%s: %s (%s)' % (
            self.phone_number, self.raw_text, self.state)

class FarmData(models.Model):
    crop = models.CharField(max_length=200)
    pest = models.CharField(max_length=200)
    harvest = models.CharField(max_length=200)
    raw_log = models.OneToOneField(to=RawLog)
    media_url = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=2)

    def __str__(self):
        return '%s, %s, %s, %s (%s)' % (
           self.crop, self.pest, self.harvest, self.state, self.raw_log.pk)
