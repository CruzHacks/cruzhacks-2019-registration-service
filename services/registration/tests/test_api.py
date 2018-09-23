"""API tests."""
import os

import pytest
from werkzeug.exceptions import Unauthorized

from registration.src.api import whitelist

class TestWhitelist:
    """Tests if a user can access a whitelisted function."""
    #pylint: disable=no-self-use

    @staticmethod
    @pytest.fixture(autouse=True)
    def patch_is_whitelist_enabled(mocker):
        """Guarantees that the whitelist is enabled."""
        mocker.patch('registration.src.api.IS_WHITELIST_ENABLED').return_value = True

    @staticmethod
    @whitelist
    def _fake_function(uid=None, token=None):
        """Acts as some function to be whitelisted."""
        return '{}:{}'.format(uid, token)

    def test_success(self, mocker):
        """Good UID and matching token."""
        mocker.patch.dict(os.environ, {'amickey_token': 'ucsc'})
        assert TestWhitelist._fake_function(uid='amickey', token='ucsc') == 'amickey:ucsc'

    @pytest.mark.parametrize('test_environ,test_uid,test_token', [
        ({'amickey_token': 'uw'}, 'amickey', 'ucsc'),  # Good UID, bad token.
        ({}, 'amickey', 'ucsc')  # Bad UID.
    ])
    def test_unauthorized(self, mocker, test_environ, test_uid, test_token):
        """Unauthorized, UID and token do not match whitelist."""
        mocker.patch.dict(os.environ, test_environ)
        mocker.patch('registration.src.api.IS_WHITELIST_ENABLED').return_value = True
        with pytest.raises(Unauthorized):
            TestWhitelist._fake_function(uid=test_uid, token=test_token)
