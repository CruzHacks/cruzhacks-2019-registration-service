#pylint: disable=missing-docstring
import os

DEPLOYMENT_MODE = os.getenv('DEPLOYMENT_MODE', 'prod').lower()

IS_WHITELIST_ENABLED = True
if os.getenv('IS_WHITELIST_ENABLED', 'True').lower() == 'false':
    IS_WHITELIST_ENABLED = False
