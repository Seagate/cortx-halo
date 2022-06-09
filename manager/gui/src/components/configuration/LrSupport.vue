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
  <div class="object-store-container config-page">
    <div>
      <div class="page-title">
        Support
        <SgtTooltipIcon>
          Administrator can change default limits of the object store and also
          override the SSL certificate packaged with the system.
        </SgtTooltipIcon>
      </div>
      <v-divider></v-divider>
    </div>
    <v-expansion-panels v-model="panel">
      <v-expansion-panel data-test="upload-config-panel">
        <v-expansion-panel-header
          ><b>
            Upload Configuration
            <SgtTooltipIcon>
              Administrator can change default limits of the object store and
              also override the SSL certificate packaged with the system.
            </SgtTooltipIcon>
          </b>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="panel-content">
          <v-form v-model="isUploadConfigValid">
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Protocol </v-col>
              <v-col cols="4">
                <SgtDropdown
                  id="protocol"
                  :dropdownOptions="protocolList"
                  placeholder="FTP"
                  v-model="supportConfig.protocol"
                  :rules="[requiredValidation]"
                  data-test="protocol"
                />
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Server Name </v-col>
              <v-col cols="4">
                <v-text-field
                  id="serverName"
                  v-model="supportConfig.serverName"
                  data-test="server-name"
                  :rules="[requiredValidation]"
                  placeholder="Enter Server Name"
                  type="text"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> User Name </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="supportConfig.userName"
                  :rules="[requiredValidation]"
                  data-test="user-name"
                  placeholder="Enter User Name"
                  type="text"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Password </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="supportConfig.password"
                  :rules="[requiredValidation]"
                  data-test="password"
                  placeholder="Enter Password"
                  type="password"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Location </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="supportConfig.location"
                  :rules="[requiredValidation]"
                  data-test="location"
                  placeholder="Enter Location"
                  type="text"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-divider></v-divider>
            <v-row class="field-row">
              <v-col cols="3"></v-col>
              <v-col cols="4" class="button-col">
                <v-btn
                  class="mr-5"
                  color="primary"
                  @click="applyUploadConfig"
                  :disabled="!isUploadConfigValid"
                  :dark="isUploadConfigValid"
                  data-test="apply-btn"
                  >Apply
                </v-btn>
                <v-btn
                  color="csmdisabled"
                  @click="resetConfirmation"
                  depressed
                  dark
                  data-test="reset-btn"
                  >Reset</v-btn
                >
              </v-col>
            </v-row>
          </v-form>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel data-test="support-action-panel">
        <v-expansion-panel-header
          ><b>
            Support Action
            <SgtTooltipIcon>
              Administrator can change default limits of the object store and
              also override the SSL certificate packaged with the system.
            </SgtTooltipIcon>
          </b>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="panel-content">
          <v-row class="field-row">
            <!-- <v-col cols="3" class="field-label"></v-col> -->
            <v-col cols="4" style="min-height: 75px">
              <v-radio-group
                v-if="supportAccountStatus"
                v-model="supportAccountStatus"
                row
                mandatory
                @change="toggleRadio"
                data-test="support-action-status"
              >
                <v-radio label="Enable" value="enable"></v-radio>
                <v-radio label="Disable" value="disable"></v-radio>
              </v-radio-group>
            </v-col>
          </v-row>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from "vue-property-decorator";
import SgtDropdown from "@/lib/components/SgtDropdown/SgtDropdown.vue";
import { Api } from "../../services/Api";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "../../lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";
import SgtTooltipIcon from "@/lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
import { requiredValidation } from "../../utils/validations";

@Component({
  name: "LrSupport",
  components: { SgtDropdown, SgtTooltipIcon },
})
export default class LrSupport extends Vue {
  panel = 0;
  initialLoad = false;
  supportConfig = {};
  supportAccountStatus = "";
  requiredValidation = requiredValidation;
  protocolList = [
    { label: "FTP", value: "FTP" },
    { label: "STP", value: "STP" },
  ];
  resetModal = create<SgtDialogModel>(SgtDialog);
  isUploadConfigValid = false;

  mounted() {
    this.getSupportConfig();
    this.getSupportAccountStatus();
  }

  async getSupportConfig() {
    const resp: any = await Api.getData("config/supportConfig", {
      isDummy: true,
    });
    if (resp && resp.data) {
      Object.assign(this.supportConfig, resp.data);
    }
  }
  async getSupportAccountStatus() {
    const resp: any = await Api.getData("config/supportAccountStatus", {
      isDummy: true,
    });
    this.supportAccountStatus = resp.data?.supportAccountStatus;
  }

  async resetLimitValues() {
    //API call to reset the limit value followed by the getLimits call
    this.getSupportConfig();
  }

  async resetConfirmation() {
    await this.resetModal({
      modalTitle: "Confirmation",
      modalContent: `Are you sure you want to reset the data?`,
      modalType: "prompt",
      modalContentType: "text",
    }).then(async (resp) => {
      if (resp === "yes") {
        this.resetLimitValues();
      }
    });
  }

  async toggleRadio() {
    if (!this.initialLoad) {
      this.initialLoad = true;
    } else {
      const modalContent =
        this.supportAccountStatus == "enable"
          ? "Are you sure you want to enable the account?"
          : "Are you sure you want to disable the account?";
      await this.resetModal({
        modalTitle: "Confirmation",
        modalContent: modalContent,
        modalType: "prompt",
        modalContentType: "text",
      }).then(async (resp) => {
        if (resp === "yes") {
          this.toggleAccount(this.supportAccountStatus);
        }
      });
    }
    // debugger;
  }

  toggleAccount(value: string) {
    //api call to enable/disable account.
  }

  applyUploadConfig() {
    //api call
  }
}
</script>
<style lang="scss" scoped></style>
