/*
 * CORTX-CSM: CORTX Management web.
 * Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 * For any questions about this software or licensing,
 * please email opensource@seagate.com.
 */
export const AppConst = {
  navItems: [
    {
      title: "dashboard",
      path: "/dashboard",
      iconDefault: "icons/dashboard-grey.svg",
      iconActive: "icons/dashboard-white.svg",
      requiredAccess: "alerts",
    },
    {
      title: "health",
      path: "/health",
      iconDefault: "icons/health-grey.svg",
      iconActive: "icons/health-white.svg",
      requiredAccess: "sysconfig",
    },
    {
      title: "manage",
      path: "/manage",
      iconDefault: "icons/manage-grey.svg",
      iconActive: "icons/manage-white.svg",
      requiredAccess: "s3accounts",
    },
    {
      title: "configuration",
      path: "/configuration",
      iconDefault: "icons/settings-grey.svg",
      iconActive: "icons/settings-white.svg",
      requiredAccess: "configuration",
    },
    {
      title: "maintenance",
      path: "/maintenance",
      iconDefault: "icons/maintenance-grey.svg",
      iconActive: "icons/maintenance-white.svg",
      requiredAccess: "sysconfig",
    },
    {
      title: "object store",
      path: "/object-store",
      iconDefault: "icons/object-store-grey.svg", // #TODO: change the object-store-white.svg
      iconActive: "icons/object-store-white.svg",
      requiredAccess: "sysconfig", // #TODO: this is temp untill i get fixed thing
    }
  ],
};
