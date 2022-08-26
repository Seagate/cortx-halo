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

import json


class Session:

    def __init__(self, user_name, user_id, user_type,
                 permissions, access_token=None,
                 refresh_token=None) -> None:
        """Instantiation Method for Session class.

        Args:
            user_name (str): Name of User.
            user_id (str): User id.
            user_type (str): Type or Role of user.
            permissions (dict): Permission dict.
            access_token (str): Encrypted access token.
            refresh_token (str): Encrypted refresh token.
        """
        self._user_name = user_name
        self._user_id = user_id
        self._user_type = user_type
        self._permissions = permissions
        self._access_token = access_token
        self._refresh_token = refresh_token

    @property
    def user_name(self):
        return self._user_name

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_type(self):
        return self._user_type

    @property
    def permissions(self):
        return self._permissions

    @property
    def access_token(self):
        return self._access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    def __str__(self):
        """Return human-readable string representation of this class."""
        return json.dumps({
            'user_name': self._user_name,
            'user_id': self._user_id,
            'user_type': self._user_type,
            'permissions': self.permissions,
            'access_token': self.access_token,
            'refresh_token': self._refresh_token
        })
