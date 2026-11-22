from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Имя")
    email = models.EmailField(unique=True, verbose_name="Email")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
