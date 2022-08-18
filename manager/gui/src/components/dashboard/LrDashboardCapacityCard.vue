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
  <div class="capacity-widget-container">
    <SgtCard
      :title="$t('capacity')"
      :showZoomIcon="true"
      titleInfo="Cluster Capacity"
      @zoom-click="zoomIconHandler"
    >
      <div class="capacity-info-wrapper">
        <div class="capacity-info">
          <div id="capacity-gauge"></div>
          <div class="total-section">
            {{ $t("total") }} - {{ capacityChartVal(capacityDetails.size) }}
          </div>
        </div>
      </div>
      <div class="content-section pa-2 mt-3">
        <div>
          <div>
            <b>{{ capacityChartVal(capacityDetails.used) }} </b>
          </div>
          <div>
            <img
              :src="require(`@/assets/images/capacity-used.svg`)"
              class="capacity-detail-icons pr-1"
              alt
            />{{ $t("used") }}
          </div>
        </div>
        <div>
          <div>
            <b>{{ capacityChartVal(capacityDetails.available) }}</b>
          </div>
          <div>
            <img
              :src="require(`@/assets/images/capacity-available.svg`)"
              class="capacity-detail-icons pr-1"
              alt
            />{{ $t("available") }}
          </div>
        </div>
      </div>
    </SgtCard>
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import * as c3 from "c3";
import SgtCard from "@/lib/components/SgtCard/SgtCard.vue";
import { CapacityData } from "./LrDashboardData.model";
import { Api } from "../../services/Api";
import * as d3 from "d3";

@Component({
  name: "LrDashboardCapacityCard",
  components: { SgtCard },
})
export default class LrDashboardCapacityCard extends Vue {
  public usedLegendClass = "capacity-badge";
  public chartDataVal: number;
  public capacityDetails: CapacityData = {} as CapacityData;

  public async mounted() {
    const resp: any = await Api.getData("/dashboard/capacity", {
      isDummy: true,
    });

    this.capacityDetails = resp.data;
    const capacityC3Data: Array<[string, number]> = [
      ["Usage", this.capacityDetails.usagePercentage],
    ];

    if (capacityC3Data) {
      this.chartDataVal = capacityC3Data[0][1] ? capacityC3Data[0][1] : 0;
      if (this.chartDataVal < 50) {
        this.usedLegendClass += " capacity-green";
      }
      if (this.chartDataVal >= 50) {
        this.usedLegendClass += " capacity-orange";
      }
      if (this.chartDataVal >= 90) {
        this.usedLegendClass += " capacity-red";
      }
    }

    c3.generate({
      bindto: "#capacity-gauge",
      legend: {
        show: false,
      },
      data: {
        columns: capacityC3Data,
        type: "gauge",
      },
      gauge: {
        label: {
          show: false,
        },
        fullCircle: true,
      },
      tooltip: {
        show: false,
      },
      color: {
        pattern: ["#60B044", "#F7A528", "#DC1F2E"], // the three color levels for the percentage values.
        threshold: {
          values: [50, 90, 100],
        },
      },
      size: {
        width: 280,
        height: 280,
      },
    });

    d3.select("#capacity-gauge .c3-chart-arcs").append("g").attr("class", "inner-circle-div");
    d3.select("#capacity-gauge .inner-circle-div")
      .append("circle")
      .attr("r", 50)
      .attr("fill", "#FFFFFF")
      .attr("stroke", "gray");
    d3.select("#capacity-gauge .inner-circle-div")
      .append("text")
      .attr("class", "circle-text")
      .attr("x", -20)
      .attr("y", 10)
      .text(this.chartDataVal + "%");
  }

  public zoomIconHandler() {
    //Route to capacity page
  }

  public capacityChartVal(chartVal: number) {
    let chartValWithUnit = "";
    const unitList = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
    for (const unit of unitList) {
      chartVal = chartVal / 1024;
      if (chartVal / 100 < 10) {
        chartValWithUnit = `${chartVal.toFixed(2)} ${unit}`;
        break;
      }
    }
    return chartValWithUnit;
  }
}
</script>
<style lang="scss" scoped>
@import "../../../node_modules/c3/c3.min.css";

.capacity-info-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;

  .capacity-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    .legends-and-value {
      width: 100%;
    }
  }
}
.content-section {
  border-top: 1px solid #e3e3e3;
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.capacity-badge {
  height: 14px;
  width: 14px;
  margin-top: 5px;
  border-radius: 50%;
}
.capacity-green {
  background: rgb(110, 190, 73);
}
.capacity-orange {
  background-color: #f7a528;
}
.capacity-red {
  background-color: #dc1f2e;
}
.capacity-available {
  background: rgb(158, 158, 158);
}

@media screen and (min-height: 600px) {
  .cortx-capacity-container {
    height: 50%;
  }
}

.total-section {
  font-weight: bold;
}

::v-deep .circle-text {
  font-size: 1.5rem;
  font-weight: bold;
}
::v-deep .c3-chart-arc {
  path {
    border-radius: 5px;
  }
}
.capacity-detail-icons {
  vertical-align: text-bottom;
}
</style>
