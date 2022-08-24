<!--
* CORTX-Halo: CORTX-Halo Management GUI.
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
    <div class="page-title">
        Security
    </div>
    <v-divider></v-divider>
    <div class="row-padding">
      <v-row class="field-row">
        <v-col cols="3" class="field-label">
          Enable TLS <SgtTooltipIcon>
                  Enable TLS for the tenant, this is required for Encryption Configuration
                </SgtTooltipIcon> 
        </v-col>
        <v-col cols="2" class="toggle-col">
           <SgtToggle
            :tooltip=" toggleStates.enableTls ? 'On' : 'Off'"
            v-model="toggleStates.enableTls"
            :labelPre = "txtOff"
            :labelPost = "txtOn"
            :areToggleLabel="true"
          ></SgtToggle>
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="3" class="field-label">
          AutoCert <SgtTooltipIcon>
                  MinIO Operator will generate all TLS certificates automatically.<br>Custom certificates: Allow user to provide your own certificates
                </SgtTooltipIcon> 
        </v-col>
        <v-col cols="2">
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="3" class="field-label pl-8">
          Enable AutoCert
        </v-col>
        <v-col cols="2" class="toggle-col">
           <SgtToggle
            :tooltip=" toggleStates.enableAutoCert ? 'On' : 'Off'"
            v-model="toggleStates.enableAutoCert"
            :labelPre = "txtOff"
            :labelPost = "txtOn"
            :areToggleLabel="true"
          ></SgtToggle>
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="3" class="field-label pl-8">
          Custom Certificates 
        </v-col>
        <v-col cols="2" class="toggle-col">
           <SgtToggle
            :tooltip=" toggleStates.enableCustomCert ? 'On' : 'Off'"
            v-model="toggleStates.enableCustomCert"
            :labelPre = "txtOff"
            :labelPost = "txtOn"
            :areToggleLabel="true"
          ></SgtToggle>
        </v-col>
      </v-row>
    </div>
    
    <div class="page-title">
        Encryption <SgtTooltipIcon>How would you like to encrypt the information at rest.</SgtTooltipIcon> 
    </div>
    <v-divider></v-divider>
    <div class="row-padding">
      <v-row class="field-row">
        <v-col cols="3" class="field-label">
          Enable Server Side Encryption 
        </v-col>
        <v-col cols="2" class="toggle-col">
           <SgtToggle
            :tooltip=" toggleStates.enableServerSideEncryption ? 'On' : 'Off'"
            v-model="toggleStates.enableServerSideEncryption"
            :labelPre = "txtOff"
            :labelPost = "txtOn"
            :areToggleLabel="true"
          ></SgtToggle>
        </v-col>
      </v-row>
      </div>
      <v-divider></v-divider>
      <div class="row-padding">
      <v-row class="field-row">
        <v-col cols="4" class="button-col">
          <v-btn
            class="mr-5"
            color="primary"
            >Save
          </v-btn>
          <v-btn
            color="csmdisabled"
            depressed
            dark
            >Reset</v-btn
          >
        </v-col>
      </v-row>
      </div>
    </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import SgtTooltipIcon from "@/lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
import SgtToggle from "@/lib/components/SgtToggle/SgtToggle.vue";

@Component({
  name: "TenantSecurity",
  components: { SgtTooltipIcon, SgtToggle},
})
export default class TenantSecurity extends Vue {
  
  toggleStates = {
    enableTls: true,
    enableAutoCert: true,
    enableCustomCert: false,
    enableServerSideEncryption: false,
  };
  txtOn = "ON";
  txtOff = "OFF";

  
}
</script>
<style lang="scss" scoped>
.row-padding{
  padding: 20px 0 20px 20px;
}
.toggle-col{
  font-weight: bold;
}
</style>