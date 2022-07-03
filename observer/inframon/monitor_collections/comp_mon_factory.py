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
import const
from cortx.utils.log import Log
from component import Component


class ComponentMonitorFactory:
    """Factory to provide requested component instance"""

    @staticmethod
    def get_component(element, component):
        module = ".".join([element, component])
        try:
            module = importlib.import_module(module)
            comp_collection = inspect.getmembers(module, inspect.isclass)
            for _, kls in comp_collection:
                if issubclass(kls, Component) and component.lower() == kls.NAME.lower():
                    return kls()
        except ModuleNotFoundError as err:
            Log.error(f"Invalid component, {component}. {err}")


if __name__ == '__main__':

    Log.init(service_name="monitor", log_path=const.LOG_PATH, level="INFO")

    component = ComponentMonitorFactory.get_component(element="server", component="fan")
    component.fan_list = ["Fan 1", "Fan 2"]
    component.check_health_status()
    component_data = component.get_data("Fan 1")
    Log.info(f"Received: {component_data}")
    Log.info(f"Fan Data Collection: {component.data_collection}")
    while component.data_collection:
        print("\nFan Data: ", component.data_collection.pop(0))
