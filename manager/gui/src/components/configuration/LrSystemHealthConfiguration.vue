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
          Administrator can change default limits of the object store and also
          override the SSL certificate packaged with the system.
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
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Unde,
              nulla.
            </SgtTooltipIcon>
          </b>
        </v-expansion-panel-header>
        <v-expansion-panel-content class="panel-content">
          <v-form v-model="isLimitsValid">
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                SMTP Server
                <SgtTooltipIcon>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Harum, dicta.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Sender Email
                <SgtTooltipIcon>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Harum, dicta.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Protocol
                <SgtTooltipIcon>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Harum, dicta.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                SMTP Port
                <SgtTooltipIcon>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit.
                  Harum, dicta.
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
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
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label"> Confirm Password </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Receiver Emails
                <SgtTooltipIcon>
                  Password must contain: Minimum 8 characters, One uppercase
                  letter, One lowercase letter, One special character, One
                  number
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
                  outlined
                  dense
                ></v-text-field>
              </v-col>
            </v-row>
            <v-row class="field-row">
              <v-col cols="3" class="field-label">
                Verify Config
                <SgtTooltipIcon>
                  Password must contain: Minimum 8 characters, One uppercase
                  letter, One lowercase letter, One special character, One
                  number
                </SgtTooltipIcon>
              </v-col>
              <v-col cols="4">
                <v-text-field
                  placeholder="Enter SMTP Server"
                  min="1"
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
                  @click="applyLimit"
                  :disabled="!isLimitsValid"
                  :dark="isLimitsValid"
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

@Component({
  name: "LrSystemHealthConfiguration",
  components: { SgtDropdown, SgtDropFile, SgtTooltipIcon },
})
export default class LrSystemHealthConfiguration extends Vue {
  panel = 0;
}
</script>
<style lang="scss" scoped></style>
