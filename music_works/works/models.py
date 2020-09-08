from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex
from django.db import models


class MusicWork(models.Model):
    iswc = models.CharField(max_length=11, null=True, unique=True, db_index=True)
    title = models.CharField(max_length=300, db_index=True)
    contributors = ArrayField(models.CharField(max_length=200))

    class Meta:
        indexes = [GinIndex(fields=["contributors"])]
