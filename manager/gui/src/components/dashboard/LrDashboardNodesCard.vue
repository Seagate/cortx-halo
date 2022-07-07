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
    <SgtCard
      :title="nodeCount + ' nodes'"
      :showZoomIcon="true"
      titleInfo="Total number of nodes in the cluster"
      @zoom-click="zoomIconHandler"
    >
      <div class="node-health-cards-container">
        <template v-for="(cardDetail, index) in dashboardCardDetails">
          <SgtInfoContainer
            :key="index"
            :title="$t(cardDetail.title)"
            :count="cardDetail.count"
            :unit="$t(cardDetail.unit)"
            :imgUrl="cardDetail.imgUrl"
            @click="cardClickHandler(cardDetail.description)"
            :backgroundColor="cardDetail.color"
            data-test="info-card"
          />
        </template>
      </div>
    </SgtCard>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtInfoContainer from "@/lib/components/SgtInfoContainer/SgtInfoContainer.vue";
import SgtCard from "@/lib/components/SgtCard/SgtCard.vue";
import { DashboardCardDetail, HealthData } from "./LrDashboardData.model";
import { Api } from "../../services/Api";
import { dashboardCardData } from "./LrDashboardCardData.constant";

@Component({
  name: "LrDashboardNodesCard",
  components: { SgtInfoContainer, SgtCard },
})
export default class LrDashboardNodesCard extends Vue {
  public dashboardCardDetails: DashboardCardDetail[] = [];
  public nodeCount = 0;

  public mounted() {
    this.getHealthData();
  }

  async getHealthData(){
    const data = (await Api.getData("/dashboard/health", {
      isDummy: true,
    })) as HealthData;
    this.nodeCount =
      data.nodes.online +
      data.nodes.offline +
      data.nodes.degraded +
      data.nodes.failed;
    this.dashboardCardDetails = dashboardCardData.clusterNodes.map((datum) => {
      return {
        ...datum,
        count: data.nodes[datum.title],
        imgUrl: this.nodeCount === 0 ? "health-zero-nodes.svg" : datum.imgUrl,
      };
    });
  }

  cardClickHandler(status: string) {
    this.$router.push("/health");
  }

  zoomIconHandler() {
    this.$router.push("/health");
  }
}
</script>
<style lang="scss" scoped>
.node-health-cards-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.info-card-container {
  margin-bottom: 1em;
}
.health-widget-container > .info-card-container {
  width: 100%;
}
.node-health-cards-container > * {
  width: 24%;
}
</style>
