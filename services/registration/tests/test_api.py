"""API tests."""
from collections import namedtuple
import os

import pytest
from werkzeug.exceptions import Unauthorized

from registration.src.api.utils.whitelist import verify
from registration.src.models.accounts import Dev


FakeUser = namedtuple('FakeAccount', ['username', 'encrypted_password'])
FakeRole = namedtuple('FakeRole', ['username'])

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

        class FakeUsernameQuery:
            def __init__(self, accounts):
                self.accounts = accounts

            def get(self, username):
                for candidate in self.accounts:
                    if candidate.username == username:
                        return candidate

        # Patch user model.
        class FakeAccount:
            def __init__(self, accounts):
                self.query = FakeUsernameQuery(accounts)

        fake_users = [
            FakeUser(username='amickey', encrypted_password='p@ssw0rd')
        ]

        mocker.patch(
            'registration.src.api.utils.whitelist.User'
        ).return_value = FakeAccount(fake_users)

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
