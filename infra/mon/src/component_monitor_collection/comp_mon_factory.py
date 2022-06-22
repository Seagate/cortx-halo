# Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.

import inspect
import importlib
import traceback
import const
from cortx.utils.log import Log


class ComponentMonitorFactory:
    """Factory to provide requested component instance"""

    @staticmethod
    def get_component(component):
        component_name = component.split(":")[-1]
        module = component.replace(":", ".")
        try:
            module = importlib.import_module(module)
            comp_collection = inspect.getmembers(module, inspect.isclass)
            for kls_name, kls in comp_collection:
                if component_name.lower() == kls_name.lower():
                    return kls()
        except ModuleNotFoundError as err:
            Log.error(f"Invalid component, {component}. {err}")


if __name__ == '__main__':

    Log.init(service_name="monitor", log_path=const.LOG_PATH, level="INFO")

    component = ComponentMonitorFactory.get_component("server:fan")
    component_info = component.get_info()
    component.check_health_status()
    Log.info(f"Received: {component_info}")
    Log.info(f"Events: {component.events}")
