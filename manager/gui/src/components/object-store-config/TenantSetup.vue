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
        Name
    </div>
    <v-divider></v-divider>
    <div class="row-padding">
      <v-row class="field-row">
        <v-col cols="2" class="field-label">
          Name 
        </v-col>
        <v-col cols="4">
           <v-text-field
              v-model="userName"
              placeholder="Enter Username"
              outlined
              dense
            ></v-text-field>
        </v-col>
      </v-row>
    </div>
    <v-divider></v-divider>
    <div class="page-title">
        Capacity
    </div>
    <v-divider></v-divider>
    <div class="row-padding">
      <v-row class="field-row">
        <v-col cols="2" class="field-label">
          Number of Servers 
        </v-col>
        <v-col cols="4">
           <v-text-field
              v-model="noOfServers"
              placeholder="Enter Number of Servers"
              outlined
              dense
            ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="2" class="field-label">
          Drives per Server 
        </v-col>
        <v-col cols="4">
           <v-text-field
              v-model="drivesPerServer"
              placeholder="Enter Drives per Server"
              outlined
              dense
            ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="2" class="field-label">
          Total Size 
        </v-col>
        <v-col cols="4">
           <v-text-field
              v-model="totalSize"
              placeholder="Enter Total Size"
              outlined
              dense
              disabled="true"
              append-icon="mdi-post-size"
            ></v-text-field>
        </v-col>
      </v-row>
      <v-row class="field-row">
        <v-col cols="2" class="field-label">
          Erasure Code Parity 
        </v-col>
        <v-col cols="4">
           <SgtDropdown
              :dropdownOptions="ensureCodeParity.data"
              v-model="ensureCodeParity.current"
              height="10px"
            />
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
import { Component, Vue, Watch } from "vue-property-decorator";
import SgtDropdown from "@/lib/components/SgtDropdown/SgtDropdown.vue";
 

@Component({
  name: "TenantSetup",
  components: { SgtDropdown },
})
export default class TenantSetup extends Vue {
  userName: string = "Tenant1";
  noOfServers: number = 4;
  drivesPerServer: number = 4;
  driveSize: number = 64;
  totalSize: number = this.noOfServers * this.drivesPerServer * this.driveSize;
  ensureCodeParity = {
    data: [
      {
        label:"EC:8 (Default)",
        value:"EC:8",
      },
      {
        label:"EC:9",
        value:"EC:9",
      },
      {
        label:"EC:10",
        value:"EC:10",
      },
    ],
    current: {
        label:"EC:8 (Default)",
        value:"EC:8",
      },
  };

  @Watch("noOfServers")
  onNoOfServersChanged(newValue: number, oldValue: number) {
    this.totalSize = this.noOfServers * this.drivesPerServer * this.driveSize;
  }
  @Watch("drivesPerServer")
  onDrivesPerServerChanged(newValue: number, oldValue: number) {
    this.totalSize = this.noOfServers * this.drivesPerServer * this.driveSize;
  }
  
}
</script>
<style lang="scss">
.row-padding {
  padding: 20px 0 0 20px;
}
.mdi-post-size:before{
  content: "Gi"; // The unit will be received from the server
  font-family: $font-family, sans-serif;
  font-size: 16px;

}
</style>