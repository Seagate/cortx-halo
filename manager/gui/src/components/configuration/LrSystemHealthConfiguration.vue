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
              <v-col cols="3" class="field-label">
                SMTP Server
                <SgtTooltipIcon>
                  Address of the SMTP server. It could be an IP address or a
                  FQDN.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.smtpServer"
                  :rules="validationRules.serverAddress"
                  placeholder="SMTP Server"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>

            <!-- <v-row class="field-row">
              <v-col cols="3" class="field-label"> Protocol </v-col>
              <v-col cols="4">
                <SgtDropdown
                  :dropdownOptions="protocolOptions"
                  placeholder="Protocol"
                  v-model="notificationSettings.protocol"
                />
              </v-col>
            </v-row> -->

            <v-row class="field-row">
              <v-col cols="3" class="field-label"> SMTP Port </v-col>
              <v-col cols="4">
                <v-text-field
                  v-model="notificationSettings.smtpPort"
                  :rules="validationRules.portNumber"
                  placeholder="SMTP Port"
                  type="number"
                  min="1"
                  max="65536"
                  outlined
                  dense
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
                ></v-text-field>
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
                >
                  Test
                </v-btn>
                <v-checkbox
                  v-model="isVerified"
                  label="Verified that receiver has recieved the email"
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
                  >Apply
                </v-btn>
                <v-btn
                  color="csmdisabled"
                  @click="getLimit(true)"
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
  isVerified = false;
  isSettingsValid = false;

  notificationSettings = {
    smtpServer: null,
    smtpPort: null,
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
      (val: string) => {
        /*eslint-disable*/
        debugger;
        return (
          val === this.notificationSettings.senderPassword ||
          "Passwords don't match"
        );
      },
    ],
    receiverEmails: [
      (val: string) => (val || "").length > 0 || "Email is required",
      (val: string) => {
        let validation: string | boolean = false;
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
    const res: any = await Api.getData(
      "config/system-health/notification-settings",
      {
        isDummy: true,
      }
    );
    this.notificationSettings = {
      ...res.data,
      confirmPassword: res.data.senderPassword,
    };
  }

  testEmailNotification() {
    //API call to test the email notification
  }

  applyNotificationSettings() {
    //API call to apply the notification settings
  }
}
</script>
<style lang="scss" scoped>
.verify-config-field {
  display: flex;
  align-items: center;
}
</style>
