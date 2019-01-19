"""API tests."""
import os

import pytest
from werkzeug.exceptions import Unauthorized

from registration.src.api.utils.whitelist import verify
from registration.src.models.accounts import Dev


class TestWhitelist:
    """Tests if a user can access a whitelisted function."""
    #pylint: disable=no-self-use

    @staticmethod
    @pytest.fixture(autouse=True)
    def before_all_patching(mocker):
        """Things to patch before all tests."""
        # Enable the whitelist/accounts.
        mocker.patch(
            'registration.src.api.utils.whitelist.IS_WHITELIST_ENABLED'
        ).return_value = True

        # Patch user model.
        class Fake_User:
            def __init__(self):
                self.username = 'amickey'
                self.encrypted_password = 'p@ssw0rd!'
        mocker.patch(
            'registration.src.api.utils.whitelist.User.query.get'
        ).return_value = Fake_User()

    @staticmethod
    @verify({Dev})
    def _fake_function(uid=None, token=None):
        """Acts as some function to be whitelisted."""
        return '{}:{}'.format(uid, token)

    # TODO
    def test_success(self, mocker):
        """Good UID, good token, good groups."""
        assert TestWhitelist._fake_function(uid='amickey', token='ucsc') == 'amickey:ucsc'

    # TODO
    @pytest.mark.parametrize('test_uid, test_token', [
        (   # Bad UID.
            'u',
            't',
        ),
        (   # Good UID, bad token
            'u',
            't',
        ),
        (   # Good UID, good token, bad groups (not in Dev)
            'u',
            't',
        )
    ])
    def test_unauthorized(self, mocker, test_environ, test_uid, test_token):
        """Unauthorized, UID and token do not match whitelist."""
        with pytest.raises(Unauthorized):
            TestWhitelist._fake_function(uid=test_uid, token=test_token)
