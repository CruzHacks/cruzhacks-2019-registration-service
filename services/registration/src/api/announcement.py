"""API resources for managing announcements."""
import logging

from webargs import fields
from webargs.flaskparser import use_kwargs
from flask_restful import abort, Resource

from registration.src.api.base import add_and_commit
from registration.src.api.utils.whitelist import verify, GIDS
from registration.src.db import DB, query_response_to_dict
from registration.src.models.announcement import Announcement

LOG = logging.getLogger(__name__)


class AllAnnouncements(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for registering a user or retrieving registered user(s)."""
    def get(self):
        """Gets all announcements."""
        announcements = Announcement.query.all()
        if announcements is None:
            return []
        return [query_response_to_dict(a) for a in announcements]


class SingleAnnouncement(Resource):
    # pylint: disable=no-member, unused-argument, too-many-arguments, too-many-locals, no-self-use
    """Endpoints for registering a user or retrieving registered user(s)."""
    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'title': fields.String(required=True),
        'post_date': fields.DateTime(required=True),
        'message': fields.String(missing=None)
    })
    @verify({GIDS['dev']})
    def post(self, uid, token, title, post_date, message):
        """Creates an announcement.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        :param title: title of the announcement
        :type  title: string
        :param post_date: When the announcement was submitted.  In format of 'yyyy-mm-ddThh:mm:ss'.
                          For example, 2014-12-22T03:12:58.019077 is valid/accepted.
        :type  post_date: string
        :param message: [OPTIONAL] More specific description of the announcement
        :type  message: string
        """
        a = Announcement(title, post_date, message=message)  # pylint: disable=invalid-name
        try:
            add_and_commit(a)
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            DB.session.rollback()
            LOG.exception(e)
            abort(500, message='Internal server error')
        return {'status': 'success'}

    @use_kwargs({
        'uid': fields.String(required=True),
        'token': fields.String(required=True),
        'title': fields.String(required=True),
        'post_date': fields.DateTime(required=True)
    })
    @verify({GIDS['dev']})
    def delete(self, uid, token, title, post_date):
        """Deletes an announcement.

        :param uid: UID to authenticate as
        :type  uid: string
        :param token: token (really a password) for the given UID
        :type  token: string
        :param title: title of the announcement
        :type  title: string
        :param post_date: When the announcement was submitted.  In format of 'yyyy-mm-ddThh:mm:ss'.
                          For example, 2014-12-22T03:12:58.019077 is valid/accepted.
        :type  post_date: string
        """
        a = Announcement.query.get((title, post_date))  # pylint: disable=invalid-name
        if a is None:
            abort(404, message='Announcement does not exist')
        try:
            DB.session.delete(a)
            DB.session.commit()
        except Exception as e:  # pylint: disable=broad-except,invalid-name
            DB.session.rollback()
            LOG.exception(e)
            abort(500, message='Internal server error')
        return {'status': 'success'}
