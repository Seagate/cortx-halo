<!--
* CORTX-Halo: CORTX-Halo Management GUI.
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
-->
<template>
  <div class="manage-user-page-container object-store-config-page">
    <div class="page-title">
        Tenant
    </div>
    <v-divider></v-divider>
    <div class="pt-5">
      <SgtTabs :tabsInfo="tabsInfo" @selected="onTabChange" />
    <component :is="activeTab" />
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtTabs from "../../lib/components/SgtTabs/SgtTabs.vue";
import { TabsInfo } from "../../lib/components/SgtTabs/SgtTabs.model";
import TenantSetup from "./TenantSetup.vue"
import TenantSecurity from "./TenantSecurity.vue"
@Component({
  name: "Tenant",
  components: { SgtTabs,TenantSetup,TenantSecurity},
})
export default class Tenant extends Vue {
  public tabsInfo: TabsInfo = [
    {
      id: 1,
      label: "Setup",
    },
    {
      id: 2,
      label: "Security",
    },
    {
      id: 3,
      label: "Audit Log",
    },
    {
      id: 4,
      label: "Monitoring",
    }
  ];

  activeTab: string = "TenantSetup";

  public onTabChange(value: number) {
    switch (value) {
      case 1:
        this.activeTab = "TenantSetup";
        break;
      case 2:
        this.activeTab = "TenantSecurity";
        break;
      case 3:
        this.activeTab = ""; // Placeholder for Audit Log Tab Component.
        break;
      case 4:
        this.activeTab = ""; // Placeholder for Monitoring Tab Component.
        break;
    }
  }
}
</script>

<style lang="scss" scoped>

</style>
