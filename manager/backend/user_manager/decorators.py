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
from functools import wraps
from manager.backend.user_manager.mgmt_token_manager import MgmtTokenManager
from manager.backend.user_manager.session import Session
from manager.backend.user_manager.error import (MgmtInvalidTokenError,
                                                MgmtExpiredTokenError,
                                                MgmtMissingToken)


# Decorator for validating access token.
def validator(secret):
    def validate_token(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            token = None
            # Bearer token is passed in the request header
            if 'Authorization' in request.headers:
                bearer_token = request.headers['Authorization']
                token = bearer_token.split()[-1]

            if not token:
                raise MgmtMissingToken('Missing access token')

            jwt_handler = MgmtTokenManager()

            try:
                data = jwt_handler.decode_access_token(token, secret)

                # Create new token with updated timestamp.
                updated_token = jwt_handler.create_tokens(data, secret)

                # Create session object and add it to request.
                session = Session(
                    data['user_id'], data['user_role'],
                    data['permission'], updated_token)
                request.session = session
            except jwt.ExpiredSignatureError:
                raise MgmtExpiredTokenError('Signature has expired')
            except jwt.InvalidTokenError:
                raise MgmtInvalidTokenError('Invalid access token')

            return func(request, *args, **kwargs)
        return wrapped
    return validate_token
