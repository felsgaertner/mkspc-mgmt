from django.db.models.signals import post_save
from django.dispatch import receiver

from app.base.models import Transaction, Booking


@receiver(post_save, sender=Booking)
def booking_post_save(sender, instance: Booking, created: bool, **kwargs):
    amount = instance.calculated_price
    with_transaction = instance.end_time and amount
    description = f'{instance.type.label} ({instance.duration or 0} Min)'

    # Create or update existing Transaction
    transaction = Transaction.objects.filter(booking=instance).first()
    if transaction:
        if with_transaction:
            transaction.amount = -amount
            transaction.description = description
            transaction.save()
        else:
            transaction.delete()

    elif with_transaction:
        Transaction.objects.create(
            account=instance.user.account,
            amount=-amount,
            description=description,
            booking=instance,
        )
