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
 * along with this program. If not, see https://www.gnu.org/licenses/.
 * For any questions about this software or licensing,
 * please email opensource@seagate.com.
 */

export const lrHealthConst = {
  searchConfig: {
    placeholder: "Search",
    advanceForm: [
      {
        type: "dropdown",
        name: "resource",
        label: "Resource",
        placeholder: "Select the Resource",
        options: [
          {
            label: "Cluster",
            value: "cluster"
          },
          {
            label: "Site",
            value: "site"
          },
          {
            label: "Rack",
            value: "rack"
          },
          {
            label: "Node",
            value: "node"
          }
        ],
        value: {
          label: "Cluster",
          value: "cluster"
        },
        editable: true
      },
      {
        type: "textbox",
        name: "resource-id",
        label: "Resource ID",
        placeholder: "Enter Resource ID",
        editable: true
      },
      {
        type: "dropdown",
        name: "resource-status",
        label: "Status",
        placeholder: "Select the status",
        options: [
          {
            label: "Online",
            value: "online"
          },
          {
            label: "Offline",
            value: "offline"
          }
        ],
        value:{
          label: "Online",
          value: "online"
        },
        editable: true
      }
    ]
  },
  healthTable: {
    isMultiSelect: true,
    itemKey: "alert_uuid",
    headers: [
      {
        text: "Resource",
        value: "resource",
        width: "150px",
      },
      {
        text: "Resource ID",
        value: "id",
        width: "300px",
      },
      {
        text: "Status",
        value: "status",
        type: "custom",
        width: "150px",
      },
      {
        text: "Last Updated",
        value: "last_updated_time",
        type: "date",
      },
      {
        text: " ",
        value: "actionColumn",
        type: "custom",
        align: "end",
        sortable: false,
      },
    ],
  },
  severityList: {
    online: "#6ebe49",
    offline: "#dc1f2e",
    failed: "#dc1f2e",
    degraded: "#f7a528",
    unknown: "#9e9e9e",
  },
};
