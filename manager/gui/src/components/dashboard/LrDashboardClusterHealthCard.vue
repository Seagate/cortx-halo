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
  <div class="health-widget-container">
    <SgtCard title="cluster Health" :showZoomIcon="false">
      <div class="cluster-health-card-container">
        <template v-if="clusterDetails.status">
          <SgtInfoCard
            :title="clusterDetails.name"
            :description="`${clusterDetails.status}`"
            :imgUrl="getClusterHealthImgUrl(clusterDetails.status)"
            @click="cardClickHandler('/health')"
            :backgroundColor="getClusterHealthBackground(clusterDetails.status)"
          />
        </template>
      </div>
    </SgtCard>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtInfoCard from "@/lib/components/SgtInfoCard/SgtInfoCard.vue";
import SgtCard from "@/lib/components/SgtCard/SgtCard.vue";
import { Api } from "../../services/Api";
import { dashboardCardData } from "./LrDashboardCardData.constant";

@Component({
  name: "LrDashboardClusterHealthCard",
  components: { SgtInfoCard, SgtCard },
})
export default class LrDashboardClusterHealthCard extends Vue {
  public clusterDetails: any = {};

  mounted() {
    Api.getData("/dashboard/health", {
      isDummy: true,
    }).then((resp: any) => {
      this.clusterDetails = resp["cluster"];
    });
  }

  cardClickHandler(routePath: string) {
    this.$router.push(routePath);
  }

  getClusterHealthImgUrl(
    healthType: "offline" | "degraded" | "failed" | "online"
  ) {
    if (healthType && dashboardCardData.clusterHealth[healthType])
      return dashboardCardData.clusterHealth[healthType].image;
    else return dashboardCardData.clusterHealth["offline"].image;
  }

  getClusterHealthBackground(
    healthType: "offline" | "degraded" | "failed" | "online"
  ) {
    if (healthType && dashboardCardData.clusterHealth[healthType])
      return dashboardCardData.clusterHealth[healthType].color;
    else return "#FFFFFF";
  }
}
</script>
<style lang="scss" scoped>
.info-card-container {
  margin-bottom: 1em;
}
.health-widget-container > .info-card-container {
  width: 100%;
}
</style>
