"""Payment utility functions

These are mostly one-off functions. Define the bulk of Stripe operations on
:py:cls:`readthedocs.payments.forms.StripeResourceMixin`.
"""

import stripe
from django.conf import settings

stripe.api_key = getattr(settings, 'STRIPE_SECRET', None)


def delete_customer(customer_id):
    """Delete customer from Stripe, cancelling subscriptions"""
    try:
        customer = stripe.Customer.retrieve(customer_id)
        customer.delete()
    except stripe.error.InvalidRequestError:
        pass


def cancel_subscription(customer_id, subscription_id):
    """Cancel Stripe subscription, if it exists"""
    try:
        customer = stripe.Customer.retrieve(customer_id)
        if hasattr(customer, 'subscriptions'):
            subscription = customer.subscriptions.retrieve(subscription_id)
            subscription.delete()
    except stripe.error.StripeError:
        pass