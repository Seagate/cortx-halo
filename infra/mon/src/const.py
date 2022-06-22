
# Log config
LOG_PATH = "/tmp/"


COMPONENT_TOOL_MAPPING = {
    "hpe": {
        "server:fan": ["ipmitool"],
        },
    "dell": {
        "server:fan": ["ipmitool", "redish"],
        },
    "corvault": {
        "storage:fan": ["storage_enclosure"]
        }
    }
