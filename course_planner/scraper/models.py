from django.db import models
from django.db.models import JSONField

# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=4) # ABCD_V ?
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    credit = models.PositiveSmallIntegerField()
    desc = models.TextField()
    prereqs = JSONField()
    coreqs = JSONField()

    class Meta:
        # Adds a unique constraint to prevent duplicate courses
        # (e.g., 'CPSC 101' should only exist once)
        unique_together = ('subject', 'code')
        # Orders courses by subject and then code by default when querying
        ordering = ['subject', 'code']

    def __str__(self):
        """
        String representation of the Course object, helpful for Django Admin.
        """
        return f"{self.subject} {self.code}: {self.name}"