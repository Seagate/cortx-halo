
# Log config
LOG_PATH = "/tmp/"

SERVER = "server"
STORAGE = "storage"

# Enable/Disbale component monitoring
COMPONENT_MONITORING_COLLECTION = {
    "server": ["fan"],
    "storage": []
}

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

EVENT_SCHEMA_FILE = "common/response.json"

DEFAULT_HEALTH_ATTRIBUTES = [
    "health",
    "health-numeric",
    "health-reason",
    "health-reason-numeric",
    "health-recommendation",
    "health-recommendation-numeric"
]
