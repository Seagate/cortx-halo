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

import pytest
import uuid
from datetime import datetime, timedelta
from manager.backend.user_manager.mgmt_token_manager import MgmtTokenManager

pytestmark = pytest.mark.unit


def test_encode_decode_jwt_token():
    """Test By encoding & decoding JWT."""
    jwt_manager = MgmtTokenManager()
    payload = {
        'user_id': str(uuid.uuid4().hex),
        'user_role': 'manager',
        'permission': ['get alert', 'list alert'],
        'exp': datetime.utcnow() + timedelta(seconds=90)
    }
    jwt_secret = jwt_manager.create_token_key()
    tokens = jwt_manager.create_tokens(payload, jwt_secret)
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']

    # Decode access token
    try:
        jwt_manager.decode_access_token(access_token, jwt_secret)
    except Exception as e:
        assert False, f'Failed to decode access token.Error {e}'

    # Decode refresh token
    try:
        jwt_manager.verify_refresh_token(refresh_token, jwt_secret)
    except Exception as e:
        assert False, f'Failed to decode refresh token.Error {e}'
