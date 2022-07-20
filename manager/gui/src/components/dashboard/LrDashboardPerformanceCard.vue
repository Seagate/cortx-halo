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
  <div class="performance-widget-container">
    <SgtCard
      :title="$t('performance')"
      :showZoomIcon="true"
      @zoom-click="zoomIconHandler"
    >
      <div class="performance-cards-container">
        <template v-for="(cardDetail, index) in dashboardCardDetails">
          <div
            class="info-card-container"
            :key="index"
            @click="cardClickHandler(cardDetail.navPath)"
          >
            <v-row>
              <v-col cols="5">
                <div class="info-title">{{ $t(cardDetail.title) }}</div>
                <v-row>
                  <v-col cols="5">
                    <img
                      :src="require(`@/assets/images/${cardDetail.imgUrl}`)"
                      alt
                    />
                  </v-col>
                  <v-col cols="7 py-7 pl-7">
                    <div class="card-info">
                      <span class="count-container"
                        ><span class="count">{{ cardDetail.count }}</span>
                        <span class="unit">{{ cardDetail.unit }}</span>
                      </span>
                    </div>
                  </v-col>
                </v-row>
              </v-col>
              <v-col cols="7" class="graph-img">
                <img
                  width="100%"
                  :src="require(`@/assets/images/${cardDetail.imgUrl2}`)"
                  alt
                />
              </v-col>
            </v-row>
          </div>
        </template>
      </div>
    </SgtCard>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtInfoCard from "@/lib/components/SgtInfoCard/SgtInfoCard.vue";
import SgtCard from "@/lib/components/SgtCard/SgtCard.vue";
import { PerformanceData, DashboardCardDetail } from "./LrDashboardData.model";
import { Api } from "../../services/Api";
import { dashboardCardData } from "./LrDashboardCardData.constant";

@Component({
  name: "LrDashboardPerformanceCard",
  components: { SgtInfoCard, SgtCard },
})
export default class LrDashboardPerformanceCard extends Vue {
  public dashboardCardDetails: DashboardCardDetail[] = [];

  public mounted() {
    Api.getData("/dashboard/performance", { isDummy: true }).then(
      (resp: any) => {
        this.dashboardCardDetails = dashboardCardData.performance.map(
          (datum) => ({
            ...datum,
            count: resp.data[datum.title],
          })
        );
      }
    );
  }

  public zoomIconHandler() {
    //Route to capacity page
  }

  cardClickHandler(routePath: string) {
    this.$router.push(routePath);
  }
}
</script>
<style lang="scss" scoped>
.info-card-container {
  border: 1px solid #e5e5e5;
  padding: 1.25em 1.25em;
  margin-bottom: 0.75em;
  .info-title {
    padding-bottom: 1em;
  }
  .count-container {
    display: flex;
    align-items: flex-end;
    .count {
      font-weight: bold;
      font-size: 2rem;
    }
    .unit {
      padding-bottom: 0.5em;
      padding-left: 0.2em;
    }
  }
}
.graph-img {
  text-align: right;
}
.info-card-container:hover {
  box-shadow: 0px 6px 15px #e5e5e5;
}
</style>
