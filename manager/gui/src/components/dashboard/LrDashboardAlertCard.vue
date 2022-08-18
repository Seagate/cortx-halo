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
  <div class="alert-widget-container">
    <SgtCard
      :title="$t('alerts')"
      :showZoomIcon="true"
      titleInfo="Total number of alerts"
      @zoom-click="zoomIconHandler"
    >
      <div id="alert-chart" class="center-align"></div>
      <div class="alert-cards-container">
        <template v-for="(cardDetail, index) in dashboardCardDetails">
          <div
            class="card-details py-2 px-3"
            :key="index"
            @click="cardClickHandler(cardDetail.description)"
          >
            <img
              :src="require(`@/assets/images/${cardDetail.imgUrl}`)"
              alt
              class="vertical-middle"
            />
            <span>
              {{ $t(cardDetail.description) }}
              <b> {{ cardDetail.title }} </b></span
            >
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
import { Api } from "../../services/Api";
import { dashboardCardData } from "./LrDashboardCardData.constant";
import * as c3 from "c3";
import * as d3 from "d3";

@Component({
  name: "LrDashboardAlertCard",
  components: { SgtInfoCard, SgtCard },
})
export default class LrDashboardAlertCard extends Vue {
  public dashboardCardDetails: any[] = [];
  totalAlerts = 0;
  public async mounted() {
    const data: any = await Api.getData("/dashboard/alerts", {
      isDummy: true,
    });
    this.dashboardCardDetails = dashboardCardData.alerts.map((datum) => {
      const count = +data.data[datum.description];
      return {
        ...datum,
        title: count,
      };
    });
    this.totalAlerts = this.dashboardCardDetails.reduce(
      (accumulator, currentValue) => accumulator + currentValue.title,
      0
    );
    this.generateAlertChart();
  }

  generateAlertChart() {
    c3.generate({
      bindto: "#alert-chart",
      legend: {
        show: false,
      },
      data: {
        columns: [...this.mapAlertsData(this.dashboardCardDetails)],
        type: "donut",
        onclick: (d) => {
          this.cardClickHandler(d.id);
        },
      },
      color: {
        pattern: ["#DC1F2E", "#AF131F", "#F7A528", "#EA3947", "#00A1DD"],
      },
      donut: {
        width: 25,
        label: { show: false },
      },
      size: {
        width: 220,
        height: 220,
      },
      tooltip: {
        format: {
          value: function (value: string) {
            return value;
          },
        },
      },
    });

    d3.select("#alert-chart .c3-chart-arcs").append("g").attr("class", "inner-circle-div");

    d3.select("#alert-chart .inner-circle-div")
      .append("circle")
      .attr("r", 50)
      .attr("fill", "#FFFFFF")
      .attr("stroke", "gray");

    d3.select("#alert-chart .inner-circle-div")
      .append("text")
      .attr("class", "circle-text")
      .attr("x", -15)
      .text(this.totalAlerts)
      .append("tspan")
      .attr("class", "circle-desc")
      .attr("dy", 20)
      .attr("x", -20)
      .text("Alerts");
  }

  mapAlertsData(alertData: any) {
    return alertData.map((ele: any) => [ele.description, ele.title]);
  }

  cardClickHandler(status: string) {
    this.$router.push({
      name: "alerts",
      params: { severity: status },
    });
  }

  zoomIconHandler() {
    this.$router.push("/alerts");
  }
}
</script>
<style lang="scss" scoped>
::v-deep .circle-text {
  font-size: 1.5rem;
  font-weight: bold;
  .circle-desc {
    font-size: 1rem;
    font-weight: initial;
  }
}
::v-deep .c3-chart-arc {
  path {
    border-radius: 5px;
  }
}
.alert-cards-container {
  padding-left: 3rem;
  .card-details {
    font-size: 1.2rem;
    min-height: 3.3rem;
  }
  .card-details:hover {
    cursor: pointer;
    border: 1px solid #e5e5e5;
  }
}
.center-align {
  text-align: center;
}
.vertical-middle {
  vertical-align: middle;
}
</style>
