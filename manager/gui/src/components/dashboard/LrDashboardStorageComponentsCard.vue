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
  <div class="storage-components-widget-container">
    <SgtCard
      :title="$t('storageComponents')"
      titleInfo="Cluster component list"
    >
      <div class="storage-cards-container">
        <template v-for="(cardDetail, index) in dashboardCardDetails">
          <SgtInfoCard
            :key="index"
            :title="cardDetail.title"
            :description="$t(cardDetail.description)"
            :imgUrl="cardDetail.imgUrl"
            @click="cardClickHandler(cardDetail.navPath)"
            data-test="info-card"
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
import {
  StorageComponentsData,
  DashboardCardDetail,
} from "./LrDashboardData.model";
import { dashboardCardData } from "./LrDashboardCardData.constant";

@Component({
  name: "LrDashboardStorageComponentsCard",
  components: { SgtInfoCard, SgtCard },
})
export default class LrDashboardStorageComponentsCard extends Vue {
  public dashboardCardDetails: DashboardCardDetail[] = [];

  public async mounted() {
    const data: any = await Api.getData("/dashboard/storage-components", {
      isDummy: true,
    });
    this.dashboardCardDetails = dashboardCardData.storageComponents.map(
      (datum) => ({
        ...datum,
        title: data.data[datum.description as keyof StorageComponentsData],
      })
    );
  }

  cardClickHandler(routePath: string) {
    // nav path given in dashboardCardDetails will be received here and it can be used for redirects
  }
}
</script>
<style lang="scss" scoped>
.storage-cards-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}
.storage-cards-container > * {
  margin-bottom: 1em;
  width: 32%;
}
</style>
