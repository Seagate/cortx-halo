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
  <div class="node-configuration-container config-page">
    <div class="page-title">
      Cluster Configuration
      <SgtTooltipIcon>
        View/update cluster wide configurations.
      </SgtTooltipIcon>
    </div>

    <v-divider></v-divider>

    <v-expansion-panels v-model="panel">
      <v-expansion-panel>
        <v-expansion-panel-header
          ><b>
            Network Time Protocol (NTP) Settings
          </b></v-expansion-panel-header
        >
        <v-expansion-panel-content class="panel-content">
          <v-form v-model="isNtpDetailsValid">
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                NTP server address
                <SgtTooltipIcon>
                  This is NTP which can be an IP address or a FQDN.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="ntp.serverAddress"
                  :rules="validationRules.serverAddress"
                  placeholder="Server Address"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> NTP time zone offset </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="timeZonesList"
                  placeholder="Time Zone"
                  v-model="ntp.timeZoneOffset"
                />
              </v-col>
            </v-row>

            <v-divider></v-divider>
            <v-row class="field-row">
              <v-col cols="3"></v-col>
              <v-col cols="4" class="button-col">
                <v-btn
                  class="mr-5"
                  color="primary"
                  @click="applyNtpSettings"
                  :disabled="!isNtpDetailsValid"
                  :dark="isNtpDetailsValid"
                  >Apply
                </v-btn>
                <v-btn
                  color="csmdisabled"
                  @click="resetConfirmation('ntp')"
                  depressed
                  dark
                  >Reset</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-header>
          <b>
            Log Configuration
            <SgtTooltipIcon>
              Change the configuration of specific services on selected nodes.
            </SgtTooltipIcon>
          </b>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="panel-content">
          <v-form>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Log Level
                <SgtTooltipIcon>
                  Select one of the log levels from the dropdown. Debug is the
                  most verbose and fatal is the least verbose.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="logLevelsList"
                  placeholder="Log Level"
                  v-model="log.logLevel"
                />
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Nodes
                <SgtTooltipIcon>
                  Select the nodes where the above chosen log level will be
                  applicable.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="nodesList"
                  placeholder="Nodes"
                  v-model="log.nodes"
                  multiple
                />
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Services
                <SgtTooltipIcon>
                  Select the services where the above chosen log level will be
                  applicable on selected nodes.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="servicesList"
                  placeholder="Services"
                  v-model="log.services"
                  multiple
                />
              </v-col>
            </v-row>

            <v-divider></v-divider>
            <v-row class="field-row">
              <v-col cols="3"></v-col>
              <v-col cols="4" class="button-col">
                <v-btn class="mr-5" color="primary" @click="applyLogInfo"
                  >Apply
                </v-btn>
                <v-btn
                  color="csmdisabled"
                  @click="resetConfirmation('log')"
                  depressed
                  dark
                  >Reset</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import SgtTooltipIcon from "@/lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
import SgtDropdown from "@/lib/components/SgtDropdown/SgtDropdown.vue";
import { timeZones, logLevels } from "@/utils/CommonUtil.constant";
import { passwordRegex, ipAddressRegex } from "@/utils/RegexHelpers";
import { Api } from "../../services/Api";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "@/lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";

@Component({
  name: "LrClusterConfiguration",
  components: { SgtTooltipIcon, SgtDropdown },
})
export default class LrClusterConfiguration extends Vue {
  panel = 0;
  resetModal = create<SgtDialogModel>(SgtDialog);
  nodesList = [];
  ntp = {
    serverAddress: null,
    timeZoneOffset: null,
  };

  log = {
    logLevel: null,
    nodes: null,
    services: null,
  };

  servicesList = [];
  timeZonesList = timeZones;
  logLevelsList = logLevels;
  isNtpDetailsValid = false;

  validationRules = {
    serverAddress: [
      (val: string) => (val || "").length > 0 || "This field is required",
      (val: string) => ipAddressRegex.test(val) || "Invalid value",
    ],
  };

  async mounted() {
    this.getNtpData();
    this.getLogData();
    const nodesListRes: any = await Api.getData("maintenance/node-list", {
      isDummy: true,
    });
    this.nodesList = nodesListRes.data.map((nodeInfo: any) => ({
      label: nodeInfo.name,
      value: nodeInfo.id,
    }));

    const servicesListRes: any = await Api.getData("config/services-list", {
      isDummy: true,
    });
    this.servicesList = servicesListRes.data.map((serviceInfo: any) => ({
      label: serviceInfo.name,
      value: serviceInfo.id,
    }));
  }

  async getNtpData() {
    const clusterNtpInfoRes: any = await Api.getData(
      "config/cluster-ntp-info",
      {
        isDummy: true,
      }
    );
    this.ntp = { ...clusterNtpInfoRes.data };
  }

  async getLogData() {
    const clusterLogInfoRes: any = await Api.getData(
      "config/cluster-log-info",
      {
        isDummy: true,
      }
    );
    this.setLogValues(clusterLogInfoRes.data);
  }

  setLogValues(logInfo: any) {
    const modifiedInfo = {
      logLevel: logInfo.logLevel,
      nodes: logInfo.nodes.map((nodeInfo: any) => nodeInfo.id),
      services: logInfo.services.map((serviceInfo: any) => serviceInfo.id),
    };
    this.log = JSON.parse(JSON.stringify(modifiedInfo));
  }

  applyNtpSettings() {
    //API to change the NTP settings of the cluster
  }

  applyLogInfo() {
    //API call to change the Log settings of the cluster
  }

  async resetConfirmation(section: "ntp" | "log") {
    const result = await this.resetModal({
      modalTitle: "Confirmation",
      modalContent: `Are you sure you want to reset the ${section} data?`,
      modalType: "prompt",
      modalContentType: "html",
    }).then(async (resp) => {
      if (resp === "yes") {
        if (section === "ntp") {
          //API call to reset the NTP data of the cluster
          this.getNtpData();
        } else {
          //API call to reset the Log data of the cluster
          this.getLogData();
        }
      }
    });
  }
}
</script>
<style lang="scss" scoped></style>
