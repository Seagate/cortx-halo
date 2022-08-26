#!/usr/bin/env python3

# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing, please email
# opensource@seagate.com or cortx-questions@seagate.com.

import jwt
import uuid
from functools import wraps
from datetime import datetime, timedelta
from enum import Enum
from manager import const
from manager.backend.user_manager.session import Session
from manager.backend.errors import (MgmtExpiredTokenError,
                                    MgmtInvalidTokenError)


class JWTConst(Enum):
    """Constants defined for JWT."""
    ALGORITHM = 'HS256'
    EXP_DELTA_SECONDS = 90
    EXP_DELTA_DAYS = 1
    AUTH_KEY = const.TOKEN_HEADER


class MgmtTokenManager:

    def __init__(self) -> None:
        """Init Method."""

    def _encode_token(self, payload, kind, secret):
        """Encrypt token.

        Args:
            payload (dict): Information to be included in token.
            kind (str): Type of token. Ex. access or refresh token.
            secret (key): Secret key for token.

        Returns:
            str: Token.
        """
        to_encode = payload.copy()
        to_encode['token_type'] = kind
        if kind == "access_token":
            to_encode.update({
                "exp": datetime.utcnow() +
                timedelta(seconds=JWTConst.EXP_DELTA_SECONDS.value)})
        else:
            to_encode.update({
                "exp": datetime.utcnow() +
                timedelta(days=JWTConst.EXP_DELTA_DAYS.value)})
        return jwt.encode(to_encode, secret,
                          algorithm=JWTConst.ALGORITHM.value)

    def _get_tokens(self, payload, secret):
        """Get access and refresh token.

        Args:
            payload (dict): Information to be included in token.
            secret (key): Secret key for token.

        Returns:
            dict: Access and refresh token.
        """
        access_token = self._encode_token(payload, "access_token", secret)
        refresh_token = self._encode_token(payload, "refresh_token", secret)

        tokens = dict(
            access_token=f"{access_token}",
            refresh_token=f"{refresh_token}"
            )
        return tokens

    def create_tokens(self, session: Session, secret):
        """Create Access and Refresh token.

        Args:
            session (Session): Session object.
            secret (key): Secret key for token.

        Returns:
            dict: Access and refresh token.
        """
        payload = {
            'user_name': session.user_name,
            'user_id': session.user_id,
            'user_type': session.user_type,
            'permissions': session.permissions
        }
        return self._get_tokens(payload, secret)

    def _decode_access_token(self, token, secret):
        """Decrypt access token.

        Args:
            token (str): Access token.
            secret (key): Secret key for token.

        Raises:
            MgmtInvalidTokenError: Invalid access token.
            MgmtExpiredTokenError: Expired token.

        Returns:
            dict: Payload information.
        """
        try:
            payload = jwt.decode(token, secret,
                                 algorithms=JWTConst.ALGORITHM.value)
            if payload['token_type'] != "access_token":
                raise MgmtInvalidTokenError('Invalid access token')
            return payload
        except jwt.ExpiredSignatureError:
            raise MgmtExpiredTokenError('Signature has expired')
        except jwt.InvalidTokenError:
            raise MgmtInvalidTokenError('Invalid access token')

    def _decode_refresh_token(self, token, secret):
        """Decrypt refresh token.

        Args:
            token (str): Access token.
            secret (key): Secret key for token.

        Raises:
            MgmtInvalidTokenError: Invalid access token.
            MgmtExpiredTokenError: Expired token.

        Returns:
            dict: Payload information.
        """
        try:
            payload = jwt.decode(token, secret,
                                 algorithms=JWTConst.ALGORITHM.value)
            if payload['token_type'] != "refresh_token":
                raise MgmtInvalidTokenError('Invalid refresh token')
            return payload
        except jwt.ExpiredSignatureError:
            raise MgmtExpiredTokenError('Sinature has expired')
        except jwt.InvalidTokenError:
            raise MgmtInvalidTokenError('Invalid refresh token')

    def verify_refresh_token(self, token, secret):
        """Validate refresh token.

        Args:
            token (str): Access token.
            secret (key): Secret key for token.

        Returns:
            bool: True/False
            dict: Payload information.
        """
        payload = self._decode_refresh_token(token, secret)
        if payload:
            return True, payload
        return False, None

    @staticmethod
    def create_token_secret():
        """Create secret key for token.

        Returns:
            str: Unique key.
        """
        return str(uuid.uuid4().hex)


# Decorator for validating access token.
def validate_token(secret):
    """Decorator to validate access token.

    Args:
        secret (str): Decrypted key.
    """
    def verify_token(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            token = None
            # Bearer token is passed in the request header
            if JWTConst.AUTH_KEY.value in request.headers:
                bearer_token = request.headers[JWTConst.AUTH_KEY.value]
                token = bearer_token.split()[-1]

            if not token:
                raise MgmtInvalidTokenError('Missing access token')

            jwt_handler = MgmtTokenManager()

            try:
                data = jwt_handler._decode_access_token(token, secret)
                # Create new token with updated timestamp.
                payload = {
                    'user_name': data['user_name'],
                    'user_id': data['user_id'],
                    'user_type': data['user_type'],
                    'permissions': data['permissions']
                }
                updated_token = jwt_handler._get_tokens(payload, secret)
                # Create session object and add it to request.
                session = Session(
                    user_name=data['user_name'],
                    user_id=data['user_id'], user_type=data['user_type'],
                    permissions=data['permissions'],
                    access_token=updated_token['access_token'],
                    refresh_token=updated_token['refresh_token'])
                request.session = session
            except jwt.ExpiredSignatureError:
                raise MgmtExpiredTokenError('Signature has expired')
            except jwt.InvalidTokenError:
                raise MgmtInvalidTokenError('Invalid access token')

            return func(request, *args, **kwargs)
        return wrapped
    return verify_token
