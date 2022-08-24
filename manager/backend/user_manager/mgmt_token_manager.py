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
from datetime import datetime, timedelta
from enum import Enum
from manager.backend.user_manager.error import (MgmtExpiredTokenError,
                                                MgmtInvalidTokenError)


class JWTConst(Enum):
    """Constants defined for JWT."""
    JWT_SECRET = 'secret'
    JWT_ALGORITHM = 'HS256'
    JWT_EXP_DELTA_SECONDS = 90
    JWT_EXP_DELTA_DAYS = 1


class MgmtTokenManager:

    def __init__(self) -> None:
        """Init Method."""
        pass

    def _encode_token(self, payload, token_type, secret):
        """Encrypt token.

        Args:
            payload (dict): Information to be included in token.
            token_type (str): Type of token. Ex. access or refresh token.
            secret (key): Secret key for token.

        Returns:
            str: Token.
        """
        to_encode = payload.copy()
        to_encode['token_type'] = token_type
        if type == "access_token":
            to_encode.update({
                "exp": datetime.utcnow() +
                timedelta(seconds=JWTConst.JWT_EXP_DELTA_SECONDS.value)})
        else:
            to_encode.update({
                "exp": datetime.utcnow() +
                timedelta(days=JWTConst.JWT_EXP_DELTA_DAYS.value)})

        return jwt.encode(to_encode, secret,
                          algorithm=JWTConst.JWT_ALGORITHM.value)

    def create_tokens(self, payload, secret):
        """Create access and refresh token.

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

    def decode_access_token(self, token, secret):
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
                                 algorithms=JWTConst.JWT_ALGORITHM.value)
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
                                 algorithms=JWTConst.JWT_ALGORITHM.value)
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

    def create_token_key(self):
        """Create secret key for token.

        Returns:
            str: Unique key.
        """
        return str(uuid.uuid4().hex)
