/*
 * CORTX-Halo: Halo Management GUI.
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
 * along with this program. If not, see https://www.gnu.org/licenses/.
 * For any questions about this software or licensing,
 * please email opensource@seagate.com.
 */

export const tenantTableConst = {
    searchConfig: {
      placeholder: "Search",
      advanceForm: [
        {
          type: "textbox",
          name: "tenantname",
          label: "Tenant Name",
          placeholder: "Enter Tenant Name",
          value: "",
        },
        {
          type: "textbox",
          name: "state",
          label: "State",
          placeholder: "Enter State",
          value: "",
        },
        {
          type: "textbox",
          name: "rawcapacity",
          label: "Raw Capacity",
          placeholder: "Enter Raw Capacity",
          value: "",
        },
        {
            type: "textbox",
            name: "usage",
            label: "Usage",
            placeholder: "Enter Usage",
            value: "",
          },
          {
            type: "textbox",
            name: "pools",
            label: "Pools",
            placeholder: "Enter Pools",
            value: "",
          },
      ],
    },
    tenantTable: {
      isMultiSelect: true,
      itemKey: "alert_uuid",
      headers: [
        {
          text: "Tenant Name",
          value: "tenantname",
        },
        {
          text: "State",
          value: "state",
        },
        {
          text: "Raw Capacity",
          value: "rawcapacity",
        },
        {
            text: "Usage",
            value: "usage",
          },
          {
            text: "Pools",
            value: "pools",
          },
        {
          text: "",
          value: "action",
          type: "action",
          align: "end",
          sortable: false,
          actionList: ["", ""],
        },
      ],
    },
  };
  