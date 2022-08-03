"""
Django provides us with password reset token generator. Tokens are also generated to send verification email for newly registered user. 
Once the user clicks on this account activation token, we will be able to extract that token and decrypt to check if it was an valid email
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type  # This library helps us to utilize the Password reset token generator.


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):   # This will generate the actual hash value we will send accross to the user
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
# By default the token will be valid for 7 days. we can change the value in settings.py
