from django.db import models


# We use model mommy to create our sample model on the fly to test Model Menu
class ModelSample(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """
        Since this is just model sample, lets just return some url
        """
        return '/page/' + self.pk