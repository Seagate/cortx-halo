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
        System Health
        <SgtTooltipIcon>
          Configuration about health of the cluster which includes both hardware
          and software services.
        </SgtTooltipIcon>
      </div>
      <v-divider></v-divider>
    </div>
    <v-expansion-panels v-model="panel">
      <v-expansion-panel>
        <v-expansion-panel-header>
          <b>
            Notification Settings
            <SgtTooltipIcon>
              Configure settings for receiving notifications about alerts in the
              system.
            </SgtTooltipIcon>
          </b>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="panel-content">
          <v-form v-model="isSettingsValid">
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Protocol </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="protocolOptions"
                  placeholder="Protocol"
                  v-model="notificationSettings.protocol"
                  data-test="protocol-dropdown-input"
                />
              </v-col>
            </v-row>

            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Server
                <SgtTooltipIcon>
                  Address of the server. It could be an IP address or a FQDN.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4" data-test="server-input-container">
                <v-text-field
                  v-model="notificationSettings.server"
                  :rules="validationRules.serverAddress"
                  placeholder="Server address"
                  outlined
                  dense
                  id="server-input-field"
                  data-test="server-input"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Port </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.port"
                  :rules="validationRules.portNumber"
                  placeholder="Port number"
                  type="number"
                  min="1"
                  max="65536"
                  outlined
                  dense
                  data-test="port-input"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Sender Email
                <SgtTooltipIcon> Email ID of the sender </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.senderEmail"
                  :rules="validationRules.email"
                  placeholder="Sender Email"
                  type="email"
                  outlined
                  dense
                  data-test="email-input"
                ></v-text-field>
              </v-col>
            </v-row>

            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Sender Password
                <SgtTooltipIcon>
                  Password must contain: Minimum 8 characters, One uppercase
                  letter, One lowercase letter, One special character, One
                  number
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.senderPassword"
                  :rules="validationRules.password"
                  placeholder="Sender Password"
                  type="password"
                  outlined
                  dense
                  data-test="password-input"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Confirm Password </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.confirmPassword"
                  :rules="validationRules.confirmPassword"
                  placeholder="Confirm Password"
                  type="password"
                  outlined
                  dense
                  data-test="confirm-password-input"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Receiver Emails </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.receiverEmails"
                  :rules="validationRules.receiverEmails"
                  placeholder="Receiver Emails"
                  outlined
                  dense
                  data-test="receiver-emails-input"
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> test </v-col>
              <v-col cols="4">
                <input
                  v-model="test"
                  type="text"
                  data-test="test-input-field"
                />
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Verify Config
                <SgtTooltipIcon>
                  This will send a test email to the receiver(s). Click on the
                  checkbox after the email is received. On successful
                  verification, the 'Apply' button will be enabled.
                </SgtTooltipIcon>
              </v-col>
              <v-col class="verify-config-field" cols="6">
                <v-btn
                  class="mr-5"
                  color="primary"
                  :disabled="!isSettingsValid"
                  :dark="isSettingsValid"
                  @click="testEmailNotification"
                  data-test="test-btn"
                >
                  Test
                </v-btn>
                <v-checkbox
                  v-model="isVerified"
                  label="Verified that receiver has recieved the email"
                  data-test="verified-checkbox"
                ></v-checkbox>
              </v-col>
            </v-row>

            <v-divider></v-divider>
            <v-row class="field-row">
              <v-col cols="3"></v-col>
              <v-col cols="4" class="button-col">
                <v-btn
                  class="mr-5"
                  color="primary"
                  @click="applyNotificationSettings"
                  :disabled="disableApply"
                  :dark="isSettingsValid && isVerified"
                  data-test="apply-btn"
                  >Apply
                </v-btn>
                <v-btn
                  color="csmdisabled"
                  @click="resetConfirmation()"
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
    </v-expansion-panels>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtDropdown from "@/lib/components/SgtDropdown/SgtDropdown.vue";
import SgtDropFile from "@/lib/components/SgtDropFile/SgtDropFile.vue";
import { Api } from "@/services/Api";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "@/lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";
import SgtTooltipIcon from "@/lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
import { emailProtocols } from "@/utils/CommonUtil.constant";
import {
  emailRegex,
  passwordRegex,
  ipAddressRegex,
  fqdnRegex,
} from "@/utils/RegexHelpers";

@Component({
  name: "LrSystemHealthConfiguration",
  components: { SgtDropdown, SgtDropFile, SgtTooltipIcon },
})
export default class LrSystemHealthConfiguration extends Vue {
  panel = 0;
  test = "";
  protocolOptions: string[] = [];
  resetModal = create<SgtDialogModel>(SgtDialog);
  isVerified = false;
  isSettingsValid = false;

  notificationSettings = {
    server: null,
    port: null,
    protocol: null,
    senderEmail: null,
    senderPassword: null,
    confirmPassword: null,
    receiverEmails: null,
  };

  validationRules = {
    serverAddress: [
      (val: string) => (val || "").length > 0 || "This field is required",
      (val: string) =>
        ipAddressRegex.test(val) || fqdnRegex.test(val) || "Invalid value",
    ],
    portNumber: [
      (val: string) => (val || "").length > 0 || "This field is required",
      (val: string) => +val <= 65536 || "Invalid value",
    ],
    email: [
      (val: string) => (val || "").length > 0 || "Email is required",
      (val: string) => emailRegex.test(val) || "Invalid email",
    ],
    password: [
      (val: string) => (val || "").length > 0 || "Password is required",
      (val: string) => passwordRegex.test(val) || "Invalid password",
    ],
    confirmPassword: [
      (val: string) => (val || "").length > 0 || "Password is required",
      (val: string) =>
        val === this.notificationSettings.senderPassword ||
        "Passwords don't match",
    ],
    receiverEmails: [
      (val: string) => (val || "").length > 0 || "Email is required",
      (val: string) => {
        const emails = (val || "").split(",");
        return (
          emails.every((email) => emailRegex.test(email.trim())) ||
          "Invalid email"
        );
      },
    ],
  };

  get disableApply() {
    if (this.isSettingsValid && this.isVerified) {
      return false;
    }
    return true;
  }

  async mounted() {
    this.protocolOptions = emailProtocols;
    this.getNotificationSettings();
  }

  async getNotificationSettings() {
    const res: any = await Api.getData(
      "config/system-health/notification-settings",
      {
        isDummy: true,
      }
    );

    this.notificationSettings.protocol = res.data.protocol;
    this.notificationSettings.server = res.data.server;
    this.notificationSettings.port = res.data.port;
    this.notificationSettings.senderEmail = res.data.senderEmail;
    this.notificationSettings.receiverEmails = res.data.receiverEmails;
  }

  testEmailNotification() {
    //API call to test the email notification
    this.testEmailsSentInfo();
  }

  applyNotificationSettings() {
    //API call to apply the notification settings
    this.appliedNotificationSettings();
  }

  async resetConfirmation() {
    const result = await this.resetModal({
      modalTitle: "Confirmation",
      modalContent: `Are you sure you want to reset the notification settings?`,
      modalType: "prompt",
      modalContentType: "html",
    }).then(async (resp) => {
      if (resp === "yes") {
        //API call to reset the notification settings
        this.getNotificationSettings();
      }
    });
  }

  async testEmailsSentInfo() {
    const result = await this.resetModal({
      modalTitle: "Success",
      modalContent: `Emails have been sent to the receivers' addresses. Click the checkbox if the mail has been received.`,
      modalType: "message",
      modalContentType: "text",
    });
  }

  async appliedNotificationSettings() {
    const result = await this.resetModal({
      modalTitle: "Success",
      modalContent: `Notification settings have been applied.`,
      modalType: "message",
      modalContentType: "text",
    });
  }
}
</script>
<style lang="scss" scoped>
.verify-config-field {
  display: flex;

  .v-input--checkbox {
    margin-top: 0;
  }
}
</style>
