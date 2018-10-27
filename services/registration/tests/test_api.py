"""API tests."""
import os

import pytest
from werkzeug.exceptions import Unauthorized

from registration.src.api.utils.whitelist import verify, GIDS


class TestWhitelist:
    """Tests if a user can access a whitelisted function."""
    #pylint: disable=no-self-use

    @staticmethod
    @pytest.fixture(autouse=True)
    def patch_is_whitelist_enabled(mocker):
        """Guarantees that the whitelist is enabled."""
        mocker.patch(
            'registration.src.api.utils.whitelist.IS_WHITELIST_ENABLED'
        ).return_value = True

    @staticmethod
    @verify({GIDS['dev']})
    def _fake_function(uid=None, token=None):
        """Acts as some function to be whitelisted."""
        return '{}:{}'.format(uid, token)

    def test_success(self, mocker):
        """Good UID and matching token."""
        mocker.patch.dict(
            os.environ,
            {
                'amickey_salt': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e',
                'amickey_hashed': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e4/QWxiiHHFEoPGQA36QONCiPpG2zTO6',
                'amickey_groups': 'admin,dev,team'
            }
        )
        assert TestWhitelist._fake_function(uid='amickey', token='ucsc') == 'amickey:ucsc'

    @pytest.mark.parametrize('test_environ,test_uid,test_token', [
        (   # Good UID, bad token, good groups.
            {
                'amickey_salt': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e',
                'amickey_hashed': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e4/QWxiiHHFEoPGQA36QONCiPpG2zTO6',
                'amickey_groups': 'admin,dev,team'
            },
            'amickey',
            'uw'
        ),
        (   # Good UID, good token, bad groups.
            {
                'amickey_salt': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e',
                'amickey_hashed': '$2a$12$2sDqlA7N4izk8cWrFcqQ8e4/QWxiiHHFEoPGQA36QONCiPpG2zTO6',
                'amickey_groups': 'judge'
            },
            'amickey',
            'uw'
        ),
        (   # Bad UID.
            {},
            'amickey',
            'ucsc'
        )
    ])
    def test_unauthorized(self, mocker, test_environ, test_uid, test_token):
        """Unauthorized, UID and token do not match whitelist."""
        mocker.patch.dict(os.environ, test_environ)
        with pytest.raises(Unauthorized):
            TestWhitelist._fake_function(uid=test_uid, token=test_token)
