from django.db import models

# Create your models here.
class Course(models.Model):
    subject = models.CharField(max_length=4)
    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=255)
    credit = models.PositiveSmallIntegerField()

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