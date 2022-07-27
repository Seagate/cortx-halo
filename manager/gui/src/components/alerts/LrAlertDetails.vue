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
  <div>
    <div class="top-section">
      <span class="section-title">Alert</span>
      <div class="action-icons">
        <SgtSvgIcon
          icon="recommendation-icon.svg"
          hoverIcon="recommendation-hover-icon.svg"
          tooltip="Recommendation"
          @click="recommendation(alertDetails)"
        />
        <SgtSvgIcon
          :disabled="alertDetails && alertDetails.acknowledged"
          icon="acknowledge-icon.svg"
          hoverIcon="acknowledge-hover-icon.svg"
          tooltip="Acknowledge"
          @click="singleAcknowledge(alertDetails)"
        />
        <SgtSvgIcon
          icon="comment-default.svg"
          hoverIcon="comment-hover.svg"
          tooltip="Comment"
          @click="comment(alertDetails)"
        />
        <SgtSvgIcon
          icon="magnify-icon.svg"
          hoverIcon="magnify-hover-icon.svg"
          tooltip="View"
          @click="openDetails(alertDetails)"
        />
      </div>
    </div>
    <LrAlertInformation
      v-if="alertDetails && alertDetails.alert_uuid"
      :alert="alertDetails"
    />

    <h2 class="alert-title-container mt-2 py-3">
      Occurrences
      <SgtTooltipIcon>
        <template>
          <div class="i-content">
            Displays all the alerts which are generated.
          </div>
        </template>
      </SgtTooltipIcon>
    </h2>
    <v-divider></v-divider>
    <LrAlert
      v-if="alertDetails"
      :alertId="alertId"
      :resourceInfo="alertDetails && alertDetails.host_id"
    />
    <LrAlertComments
      v-if="showAlertCommentsDialog"
      :id="selectedRecord.alert_uuid"
      :showAlertCommentsDialog.sync="showAlertCommentsDialog"
    />
    <LrAlertDialog
      v-if="selectedRecord"
      :modalTitle="'Alert Details'"
      :modalData="selectedRecord"
      :showAlertDetailsDialog.sync="showAlertDetailsDialog"
    />
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop, Mixins } from "vue-property-decorator";
import { lrAlertConst } from "./LrAlert.constant";
import LrAlert from "./LrAlert.vue";
import LrAlertInformation from "./LrAlertInformation.vue";
import { Api } from "../../services/Api";
import SgtTooltipIcon from "@/lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
import SgtSvgIcon from "@/lib/components/SgtSvgIcon/SgtSvgIcon.vue";
import AlertMixin from "../../mixins/AlertMixin";
import LrAlertComments from "@/components/alerts/LrAlertComments.vue";
import LrAlertDialog from "@/components/alerts/LrAlertDialog.vue";

@Component({
  name: "LrAlertDetails",
  components: {
    LrAlert,
    LrAlertInformation,
    SgtTooltipIcon,
    SgtSvgIcon,
    LrAlertComments,
    LrAlertDialog,
  },
})
export default class LrAlertDetails extends Mixins(AlertMixin) {
  @Prop({ required: true }) private alertId: string;
  alertDetails: any = null;
  mounted() {
    Api.getData("alerts/list", { isDummy: true }).then((resp: any) => {
      const alertsList: any[] = resp["data"];
      this.alertDetails = alertsList.find(
        (ele) => ele.alert_uuid === this.alertId
      );
    });
  }
}
</script>
<style lang="scss" scoped>
.alert-title-container {
  font-weight: bold;
}
.top-section {
  display: flex;
  justify-content: space-between;
  .section-title {
    font-size: 1.5rem;
    font-weight: bold;
  }
  .action-icons {
    display: flex;
    align-items: center;
    gap: 10px;
  }
}
</style>
