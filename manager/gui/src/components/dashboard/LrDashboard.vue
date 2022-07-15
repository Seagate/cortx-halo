<!--
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
-->
<template>
  <div class="dashboard-container">
    <v-row class="top-row">
      <v-col cols="3">
        <LrDashboardClusterHealthCard />
      </v-col>
      <v-col cols="9">
        <LrDashboardNodesCard />
      </v-col>
    </v-row>
    <v-row class="bottom-row">
      <v-col cols="3">
        <v-row>
          <v-col>
            <LrDashboardAlertCard />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <LrDashboardBgActivitiesCard />
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="9">
        <v-row>
          <v-col cols="6"> <LrDashboardPerformanceCard /></v-col>
          <v-col cols="6"><LrDashboardCapacityCard /></v-col>
        </v-row>
        <v-row>
          <v-col>
            <LrDashboardStorageComponentsCard />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import LrDashboardCapacityCard from "./LrDashboardCapacityCard.vue";
import LrDashboardStorageComponentsCard from "./LrDashboardStorageComponentsCard.vue";
import LrDashboardPerformanceCard from "./LrDashboardPerformanceCard.vue";
import LrDashboardClusterHealthCard from "./LrDashboardClusterHealthCard.vue";
import LrDashboardAlertCard from "./LrDashboardAlertCard.vue";
import LrDashboardBgActivitiesCard from "./LrDashboardBgActivitiesCard.vue";
import LrDashboardNodesCard from "./LrDashboardNodesCard.vue";
@Component({
  name: "LrDashboard",
  components: {
    LrDashboardCapacityCard,
    LrDashboardStorageComponentsCard,
    LrDashboardPerformanceCard,
    LrDashboardClusterHealthCard,
    LrDashboardAlertCard,
    LrDashboardBgActivitiesCard,
    LrDashboardNodesCard,
  },
})
export default class LrDashboard extends Vue {}
</script>
<style lang="scss" scoped>
.dashboard-container {
  background-color: transparent;
  height: 100%;
}
.top-row,
.bottom-row {
  min-height: min(30%, 300px);
  display: flex;
  flex-wrap: nowrap;
  gap: 20px;

  & > * {
    width: 33.33%;
    flex-grow: 1;
  }
}
</style>
