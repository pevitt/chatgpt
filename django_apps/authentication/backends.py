from django.contrib.auth import get_user_model


class EmailAuthBackend():
    """
    Authentication using auth user model by email
    """

    def authenticate(self, email=None, password=None, **kwargs):

        UserModel = get_user_model()
        if email is None:
            email = kwargs.get('email')
        try:
            user = UserModel._default_manager.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
