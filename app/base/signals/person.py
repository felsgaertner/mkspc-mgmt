from django.dispatch import receiver
from django.db.models.signals import post_save
from app.base.models import Person, Account


@receiver(post_save, sender=Person)
def person_post_save(sender, instance: Person, created: bool, **kwargs):
    if created:
        Account.objects.create(user=instance)
