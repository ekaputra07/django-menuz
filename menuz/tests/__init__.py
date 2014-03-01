from django.db import models

from menuz.registry import menuz

class ModelSample(models.Model):
    """
    Sample model to use on tests only, this will enable us to test Model Menu
    """
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        """
        Since this is just model sample, lets just return some url
        """
        return '/page/' + self.pk

menuz.register(ModelSample)