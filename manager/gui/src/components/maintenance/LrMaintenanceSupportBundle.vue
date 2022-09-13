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
  <div class="maintenance-support-bundle-page">
    <div class="top-section">
      <div class="page-title">Support bundle</div>
      <div class="description">
        Generate and download support bundle for Seagate support
      </div>
    </div>
    <div class="filters-section">
      <v-divider></v-divider>
      <div class="form-element-container">
        <div class="form-element">
          <label for="">Node</label>
          <SgtDropdown
            placeholder="Node"
            :dropdownOptions="nodeOptions"
            v-model="selectedNode"
          />
        </div>
        <div class="form-element">
          <label for="">Time Period</label>
          <v-menu
            ref="menu"
            v-model="timePeriodMenu"
            :close-on-content-click="false"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                :value="dates"
                name="time-period"
                placeholder="Time Period"
                color="green"
                readonly
                v-bind="attrs"
                v-on="on"
                class="pt-0"
                outlined
                dense
                :class="{ 'invalid-range': timePeriod.length === 1 }"
              >
                <template v-slot:append>
                  <v-icon
                    color="primary"
                    @click="timePeriodMenu = !timePeriodMenu"
                    >mdi-calendar-month-outline</v-icon
                  >
                </template>
              </v-text-field>
            </template>
            <v-date-picker
              color="csmprimary"
              v-model="timePeriod"
              :max="new Date().toISOString().slice(0, 10)"
              range
              @change="printDates"
            ></v-date-picker>
          </v-menu>
        </div>
      </div>

      <v-divider></v-divider>

      <div class="form-element-container">
        <div class="form-element">
          <label for="">Component</label>
          <SgtDropdown
            placeholder="Component"
            :dropdownOptions="['CSM', 'S3']"
            v-model="selectedComponent"
            @download="downloadBundle(data)"
          />
        </div>
        <div class="form-element">
          <label for="">Text</label>
          <v-text-field
            v-model="filterText"
            placeholder="Text"
            outlined
            dense
          ></v-text-field>
        </div>
      </div>
      <v-divider></v-divider>
    </div>
    <v-btn
      color="primary"
      class="bundle-cta-btn"
      :disabled="isDisableCTA"
      elevation="0"
      @click="generateSupportBundle"
      >Generate</v-btn
    >

    <SgtDataTable
      :headers="supportBundleConfig.supportBundleTable.headers"
      :records="supportBundleData"
      :searchConfig="supportBundleConfig.searchConfig"
      @zoom="moreInfoHandler"
      @sendTo="sendToHandler"
    />
    <SendTo 
    v-if="sendToStatus"
    @close-popup="sendToStatus = false" />

    <v-dialog v-model="bundleDetailView" max-width="800px" persistent>
      <v-card>
        <v-card-title>
          <div class="title-container">
            <SgtSvgIcon
              icon="green-tick.svg"
              class="title-icon"
              disableClick="true"
            />
            <div class="title-content">Bundle Deatil View</div>
          </div>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div class="content-container">
            <v-container>
              <v-row>
                <v-col cols="3">
                  <b>Bundle Id :</b>
                </v-col>
                <v-col>{{bundleViewDetails.bundleId}}</v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Timestamp :</b>
                </v-col>
                <v-col>{{bundleViewDetails.timestamp}}</v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Status :</b>
                </v-col>
                <v-col>{{bundleViewDetails.status}}</v-col>
              </v-row>
              <v-row>
                <v-col cols="3" class="modal-sub-title">
                  <b>Parameters</b>
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Component :</b>
                </v-col>
                <v-col>{{bundleViewDetails.parameters.component}}</v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Node :</b>
                </v-col>
                <v-col>{{bundleViewDetails.parameters.node.name}}</v-col>
              </v-row>
            </v-container>
          </div>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="action-button-container">
          <v-btn color="csmborder" dark
            @click="bundleDetailView=false">Close</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtDropdown from "@/lib/components/SgtDropdown/SgtDropdown.vue";
import SgtDataTable from "@/lib/components/SgtDataTable/SgtDataTable.vue";
import SgtSvgIcon from "@/lib/components/SgtSvgIcon/SgtSvgIcon.vue";
import { Api } from "../../services/Api";
import { lrMaintenanceSupportBundleConst } from "./LrMaintenance.constant";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "@/lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";
import { formatTime } from "@/utils/CommonUtilFunctions";
import SendTo from "./SendTo.vue"
import moment from "moment";
@Component({
  name: "LrMaintenanceSupportBundle",
  components: { SgtDropdown, SgtDataTable, SgtDialog, SgtSvgIcon, SendTo},
})
export default class LrMaintenanceSupportBundle extends Vue {
  selectedNode: string = "";
  selectedComponent: string = "";
  filterText: string = "";
  dates: string = "";
  timePeriod: string[] = [];
  timePeriodMenu: boolean = false;
  supportBundleData = [];
  nodeOptions = [];
  supportBundleConfig = lrMaintenanceSupportBundleConst;
  moreInfoModel = create<SgtDialogModel>(SgtDialog);
  sendToStatus: boolean = false
  bundleDetailView: boolean = false
  bundleViewDetails = {
    "bundleId": "2fe291da-c999-44a6",
    "timestamp": "1637652160",
    "status": "In progress",
    "parameters": {
      "component": "CSM",
      "node": {
        "name": "Node1",
        "id": "1"
      }
    }
  }
  get isDisableCTA() {
    let isDisable = true;
    if (
      this.selectedNode &&
      this.selectedComponent &&
      this.timePeriod.length === 2
    ) {
      isDisable = false;
    }
    return isDisable;
  }

  public dateRange = {
    startDate: 0,
    endDate: 0,
  };

  public printDates() {
    switch (this.timePeriod.length) {
      case 1:
        this.dates = this.dates[0];
        break;
      case 2:
        this.dates =
          this.timePeriod[0] > this.timePeriod[1]
            ? this.timePeriod.reverse().join(" ~ ")
            : this.timePeriod.join(" ~ ");
        break;
    }
  }

  async mounted() {
    const supportBundleRes: any = await Api.getData(
      "maintenance/support-bundle",
      {
        isDummy: true,
      }
    );
    this.supportBundleData = supportBundleRes.data;

    const nodeListRes: any = await Api.getData("maintenance/node-list", {
      isDummy: true,
    });
    this.nodeOptions = nodeListRes.data.map((datum: any) => ({
      label: datum.name,
      value: datum.id,
    }));
  }

  async moreInfoHandler(data: any) {
    this.bundleViewDetails = data;
    console.log(this.supportBundleData);
    console.log(data);
    this.bundleDetailView = true;
    this.bundleViewDetails.timestamp = formatTime(this.bundleViewDetails.timestamp)
  }

  generateSupportBundle() {
    if (this.timePeriod[0] > this.timePeriod[1]) {
      this.dateRange.startDate = moment(
        moment(this.timePeriod[1]).toDate()
      ).unix();
      this.dateRange.endDate =
        moment(moment(this.timePeriod[0]).toDate()).unix() + 86399;
    } else {
      this.dateRange.startDate = moment(
        moment(this.timePeriod[0]).toDate()
      ).unix();
      this.dateRange.endDate =
        moment(moment(this.timePeriod[1]).toDate()).unix() + 86399;
    }
    //API call to generate the support bundle
  }

  downloadBundle(data: any) {
    //API call to receive the support bundle
  }
  sendToHandler(data: any){
    this.sendToStatus = true;
  }
}
</script>
<style lang="scss" scoped>
.maintenance-support-bundle-page {
  .page-title {
    font-weight: bold;
  }

  .bundle-cta-btn {
    margin-bottom: 1em;
  }

  .v-divider {
    margin: 20px 0;
  }

  .form-element-container {
    display: flex;
    align-items: center;
    gap: 6em;
    .form-element {
      max-width: 550px;
      display: flex;
      justify-content: space-between;
      flex-grow: 1;
      label {
        margin-top: 8px;
        font-weight: bold;
        width: 140px;
      }

      & > div {
        max-width: 400px;
      }
    }
  }
}
.title-container {
  width: 100%;
  .close-btn {
    cursor: pointer;
    float: right;
  }
  .title-content {
    display: inline-block;
    font-weight: bold;
  }
  .title-icon {
    vertical-align: top;
    padding-right: 0.5rem;
  }
}
.v-picker {
  width: 100%;
}
.modal-sub-title{
  color: #000;
  font-size: 1rem;
}
</style>
