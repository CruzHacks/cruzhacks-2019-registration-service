"""API tests."""
from collections import namedtuple
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

        FakeUser = namedtuple('FakeAccount', ['username', 'encrypted_password'])
        FakeRole = namedtuple('FakeRole', ['username'])

        # Implements the interface of a query from a table.
        class FakeUsernameQuery:
            pass

        # Implements the interface of an account table (e.g. User, Dev, Director, Organizer)
        class FakeAccount:
            def __init__(self):
                self.query = FakeUsernameQuery()
        
        mocker.patch('registration.src.api.utils.whitelist.User').return_value = FakeAccount()
        mocker.patch('registration.src.api.utils.whitelist.Dev').return_value = FakeAccount()
        mocker.patch('registration.src.api.utils.whitelist.Director').return_value = FakeAccount()
        mocker.patch('registration.src.api.utils.whitelist.Organizer').return_value = FakeAccount()

        def get_user(uid):
            users = {
                'amickey': FakeUser(
                    username='amickey',
                    encrypted_password=b'$2b$12$kVp2MoxWtYJhGWCT5fi4k.JH93YK6iHmaBo3fhfUB42eyrUJS.FNO' # p@ssw0rd
                ),
                'yikes': FakeUser(
                username='yikes',
                encrypted_password=b'$2b$12$kVp2MoxWtYJhGWCT5fi4k.JH93YK6iHmaBo3fhfUB42eyrUJS.FNO' # p@ssw0rd
                )
            }
            return users.get(uid)

        def get_devs(uid):
            roles = {
                'amickey': FakeRole(username='amickey')
            }
            return roles.get(uid)
      
        def get_directors(uid):
            roles = {
                'yikes': FakeRole(username='yikes')
            }
            return roles.get(uid)

        def get_organizers(uid):
            roles = {}
            return roles.get(uid)

        mocker.patch(
            'registration.src.api.utils.whitelist.User.query.get'
        ).side_effect = get_user

        mocker.patch(
            'registration.src.api.utils.whitelist.Dev.query.get'
        ).side_effect = get_devs

        mocker.patch(
            'registration.src.api.utils.whitelist.Director.query.get'
        ).side_effect = get_directors

        mocker.patch(
            'registration.src.api.utils.whitelist.Organizer.query.get'
        ).side_effect = get_organizers

    @staticmethod
    @verify({Dev})
    def _fake_function(uid=None, token=None):
        """Acts as some function to be whitelisted."""
        return '{}:{}'.format(uid, token)

    def test_success(self, mocker):
        """Good UID, good token, good groups."""
        assert TestWhitelist._fake_function(uid='amickey', token='p@ssw0rd') == 'amickey:p@ssw0rd'

    @pytest.mark.parametrize('test_uid, test_token', [
        (   # Bad UID.
            'my_uid_doesnt_exist',
            'token',
        ),
        (   # Good UID, bad token
            'yikes',
            'my_token_doesnt_match',
        ),
        (   # Good UID, good token, bad groups (not in Dev)
            'yikes',
            'p@ssw0rd',
        )
    ])
    def test_unauthorized(self, mocker, test_uid, test_token):
        """Unauthorized, UID and token do not match whitelist."""
        with pytest.raises(Unauthorized):
            TestWhitelist._fake_function(uid=test_uid, token=test_token)
