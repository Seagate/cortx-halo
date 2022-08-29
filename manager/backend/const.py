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

# common constants
# TODO: configure this path
BASE_DIR = "/opt/seagate/halo"
BASE_ETC_DIR = "/etc/halo"

MGMT_PATH = BASE_DIR + "/manager"
MGMT_ETC_DIR = BASE_ETC_DIR + "/manager"

STRING_MAX_VALUE = 250
PATH_PREFIX_MAX_VALUE = 512
PORT_MIN_VALUE = 0
PORT_MAX_VALUE = 65536

# password validation
PASSWORD_SPECIAL_CHARACTER = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
                              "_", "+", "-", "=", "[", "]", "{", "}", "|", "'"]

# REST API Constants
MESSAGE_LITERAL = 'message'

# Error response constants
ERROR_CODE = "error_code"
MESSAGE_ID = "message_id"

UNKNOWN_ERROR = 'UnknownError'
HTTP_ERROR = 'HttpError'

# file operation constants
DEFAULT_SUPPORT_BUNDLE_ROOT = BASE_DIR + '/bundle'
MGMT_TEMP_PATH = MGMT_PATH + "/temp"
MGMT_AUDIT_LOG = MGMT_TEMP_PATH + "/audit_logs/"
MGMT_TMP_FILE_CACHE_DIR = MGMT_TEMP_PATH + "/file_cache/transfer"

# REST FILE HEADER KEY
FILE_HEADER = 'Content-Disposition'

# REST AUTH/TOKEN HEADER KEY AND AUTH/TOKEN TYPE
AUTH_HEADER = 'Authorization'
AUTH_TYPE   = 'Bearer'

# REST/HTTP STATUS CODES
STATUS_SUCCESS  = 200
STATUS_CREATED  = 201
STATUS_CONFLICT = 409

# ERROR RESPONSE KEYS
KEY_RESPONSE_MESSAGE        = 'message'
KEY_ERR_RESPONSE_ERROR_CODE = 'error_code'
KEY_ERR_RESPONSE_MESSAGE_ID = 'message_id'
KEY_ERR_RESPONSE_MESSAGE    = 'message'
KEY_ERR_RESPONSE_FORMAT_ARG = 'error_format_args'
KEY_ERR_RESPONSE_STACKTRACE = 'stacktrace'

# MGMT ERROR MESSAGE IDs
INVALID_REQUEST         = 'MalformedRequest'
UNKNOWN_ERROR           = 'UnknownError'
RESOURCE_EXISTS         = 'ResourceExist'
INTERNAL_ERROR          = 'InternalError'
NOT_FOUND_ERROR         = 'NotFoundError'
INVALID_AUTH_ERROR      = 'InvalidToken'
EXPIRED_AUTH_ERROR      = 'ExpiredToken'
PERMISSION_DENIED_ERROR = 'PermissionDenied'
UNAUTHORIZED            = 'Unauthorized'
RESOURCE_NOT_AVAILABLE  = 'ResourceNotAvailable'
TYPE_ERROR              = 'TypeError'
NOT_IMPLEMENTED         = 'NotImplemented'
SERVICE_CONFLICT        = 'ServiceConflict'
GATEWAY_TIMEOUT         = 'GatewayTimeout'
UNAUTHORIZED_ERROR      = 'UnauthorizedError'
SERVICE_NOT_AVAILABLE   = 'ServiceNotAvailable'
REQUEST_CANCELLED       = 'RequestCancelled'
SETUP_ERROR             = 'SetupError'
HTTP_ERROR              = 'HttpError'
