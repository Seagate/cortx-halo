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
  <div class="alert-details-container" v-if="alert">
    <div class="top-section">
      <div class="alert-info-card">
        <div class="alert-info-group">
          <div class="alert-info-title">Resource name</div>
          <div class="alert-info-description">
            {{ alert.hostname }}
          </div>
        </div>
        <div class="alert-info-group">
          <div class="alert-info-title">Alert Type</div>
          <div class="alert-info-description">{{ alert.alert_type }}</div>
        </div>
      </div>

      <div class="alert-info-card">
        <div class="alert-hr-group">
          <div class="alert-info-group">
            <div class="alert-info-title">Severity</div>
            <div class="alert-info-description">{{ alert.severity }}</div>
          </div>
          <div class="alert-info-group">
            <div class="alert-info-title">Created Time</div>
            <div class="alert-info-description">
              {{ formattedTime(alert.created_time) }}
            </div>
          </div>
        </div>
        <div class="alert-info-group">
          <div class="alert-info-title">State</div>
          <div class="alert-info-description">{{ alert.state }}</div>
        </div>
      </div>

      <div class="alert-info-card">
        <div class="alert-info-group">
          <div class="alert-info-title">Reason</div>
          <div class="alert-info-description">
            {{ alert.description }}
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-section">
      <div class="alert-info-item">
        <div class="alert-info-title">Category</div>
        <div class="alert-info-description">{{ alert.category }}</div>
      </div>
      <div class="alert-info-item">
        <div class="alert-info-title">Site</div>
        <div class="alert-info-description">{{ alert.site }}</div>
      </div>
      <div class="alert-info-item">
        <div class="alert-info-title">Rack</div>
        <div class="alert-info-description">
          {{ alertExtendedInfo.rack_id }}
        </div>
      </div>
      <div class="alert-info-item">
        <div class="alert-info-title">Node</div>
        <div class="alert-info-description">{{ alert.node_id }}</div>
      </div>
      <div class="alert-info-item">
        <div class="alert-info-title">Cluster</div>
        <div class="alert-info-description">
          {{ alertExtendedInfo.cluster_id }}
        </div>
      </div>
    </div>

    <div>
      <LrAlertDialog
        v-if="
          alertDetails &&
          alertExtendedInfo &&
          Object.keys(alertExtendedInfo).length > 0
        "
        :modalTitle="'Alert Details'"
        :modalData="alertExtendedInfo"
        :showAlertDetailsDialog.sync="showAlertDetailsDialog"
      />
    </div>
    <div>
      <LrAlertComments
        v-if="alertDetails"
        :id="alertDetails.alert_uuid"
        :showAlertCommentsDialog.sync="showAlertCommentsDialog"
      />
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop, Mixins, Watch } from "vue-property-decorator";
import SgtLabel from "@/lib/components/SgtLabel/SgtLabel.vue";
import LrAlertDialog from "./LrAlertDialog.vue";
import LrAlertComments from "./LrAlertComments.vue";
import SgtSvgIcon from "@/lib/components/SgtSvgIcon/SgtSvgIcon.vue";
import { formatTime } from "@/utils/CommonUtilFunctions";

@Component({
  name: "LrAlertInformation",
  components: { SgtLabel, LrAlertDialog, SgtSvgIcon, LrAlertComments },
})
export default class LrAlertInformation extends Vue {
  @Prop({ required: true }) private alert: any;
  public alertEventDetails: any = [];
  public alertExtendedInfo: any = {};
  public alertDetails: any = {};
  public showAlertDetailsDialog = false;
  public showAlertCommentsDialog = false;
  public addCommentForm = {
    comment_text: "",
  };

  public async mounted() {
    try {
      if (this.alert.extended_info) {
        this.alertDetails = JSON.parse(this.alert.extended_info);
        this.alertExtendedInfo = this.alertDetails.info;
      }
      let tempAlertEventDetails = [];
      if (this.alert.event_details) {
        tempAlertEventDetails = JSON.parse(this.alert.event_details);
      }
      if (tempAlertEventDetails.length > 0) {
        tempAlertEventDetails.forEach((event_detail: any) => {
          const alertEventDetail = {
            name: event_detail.name,
            event_reason: event_detail.event_reason,
            event_recommendation: event_detail.event_recommendation.split("-"),
            showRecommendation: false,
          };
          this.alertEventDetails.push(alertEventDetail);
        });
      } else {
        this.alertEventDetails.push({
          name: this.alertExtendedInfo.resource_id
            ? this.alertExtendedInfo.resource_id
            : "",
          event_reason: this.alert.description,
          event_recommendation: this.alert.health_recommendation
            ? this.alert.health_recommendation.split("-")
            : [],
          showRecommendation: false,
        });
      }
    } catch (e) {
      // tslint:disable-next-line: no-console
      console.log(e);
    }
  }

  formattedTime(val: number) {
    return formatTime(val);
  }

  comment() {
    //comment action
    this.showAlertCommentsDialog = true;
  }
  acknowledge() {
    //acknowledge action
  }
}
</script>

<style lang="scss" scoped>
.alert-details-container {
  margin: 0;

  .top-section {
    margin: 1em 0;
    display: flex;
    gap: 1em;

    & > .alert-info-card {
      flex: 1 1 0;
    }

    .alert-info-card {
      background: #fcfcfd;
      box-shadow: 0px 4px 8px -2px rgba(9, 30, 66, 0.25),
        0px 0px 0px 1px rgba(9, 30, 66, 0.08);
      border-radius: 8px;
      padding: 0.5em 1em;

      .alert-info-group {
        margin: 0 0 1em;
      }

      .alert-hr-group {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
    }
  }

  .alert-info-title {
    font-weight: bold;
  }

  .bottom-section {
    background: #fcfcfd;
    box-shadow: 0px 4px 8px -2px rgba(9, 30, 66, 0.25),
      0px 0px 0px 1px rgba(9, 30, 66, 0.08);
    border-radius: 8px;
    display: flex;
    & > *:not(:last-child) {
      border-right: 1px solid #c4c4c4;
    }
    .alert-info-item {
      flex-grow: 1;
      padding: 0.5em 1em;
      text-align: center;
    }
    .alert-info-item:last-child {
      flex-grow: 2;
    }
  }
}
.alert-info {
  display: inline-block;
  padding-left: 1rem;
  span {
    vertical-align: super;
  }
  .action-btn-block {
    padding-left: 1rem;
  }
}
</style>
