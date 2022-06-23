
# Log config
LOG_PATH = "/tmp/"


SERVER = "server"
STORAGE = "storage"

SERVER_TOOL_MAPPING = {
    "server": {
        "hpe": {
            "fan": ["ipmitool"],
            },
        "dell": {
            "fan": ["ipmitool", "redish"],
            }
        }
    }

STORAGE_TOOL_MAPPING = {
    "storage": {
        "corvault": {
            "fan": ["storage_enclosure"]
            }
        }
    }

# Tool command functions
LIST = "list"
GET = "get"
