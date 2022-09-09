<!--
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
* along with this program. If not, see <https://www.gnu.org/licenses/>.
* For any questions about this software or licensing,
* please email opensource@seagate.com.
-->
<template>
   <div>
    <div class="manage-user-page-container object-store-config-page">
      <div class="page-title">
          Object Store Configuration
      </div>
      <v-divider></v-divider>
    </div>
    <SgtDataTable
      ref="tenantTable"
      :headers="tenantTableConfig.tenantTable.headers"
      :records="tenantData"
      :searchConfig="tenantTableConfig.searchConfig"
      :headerButton="{ name: 'createTenant', label: 'Create Tenant' }"
      @createTenant="$router.push({name:'tenant'})"
    />
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { tenantTableConst } from "./ObjectStoreConfig.constant";
import { Api } from "../../services/Api";
import SgtDataTable from "../../lib/components/SgtDataTable/SgtDataTable.vue";

@Component({
  name: "ObjectStoreConfigHome",
  components: {
    SgtDataTable,
  },
})
export default class ObjectStoreConfigHome extends Vue {
  public tenantTableConfig = tenantTableConst;
  public tenantData = [];
  public async mounted() {
    const res: any = await Api.getData("object-store-config", {
      isDummy: true,
    });
    this.tenantData = res.data;
   }
}
</script>

<style lang="scss" scoped>
</style>
