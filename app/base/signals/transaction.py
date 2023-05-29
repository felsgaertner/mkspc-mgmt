from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
from app.base.models import Transaction


@receiver(pre_save, sender=Transaction)
def transaction_pre_save(sender, instance: Transaction, **kwargs):
    if instance.pk:
        pre_edit = Transaction.objects.get(pk=instance.pk)

        if pre_edit.amount != instance.amount:
            delta = pre_edit.amount - instance.amount
            account = instance.account
            account.balance = account.balance - delta
            account.save()


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance: Transaction, created, **kwargs):
    if created:
        instance.account.balance += instance.amount
        instance.account.save()


@receiver(pre_delete, sender=Transaction)
def transaction_pre_delete(sender, instance: Transaction, **kwargs):
    instance.account.balance -= instance.amount
    instance.account.save()
