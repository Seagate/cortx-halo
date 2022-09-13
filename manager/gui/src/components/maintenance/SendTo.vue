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
    <v-dialog
        :value="value"
        @input="$emit('input', value)"
      persistent
      max-width="590"
      class="add-edit-user-dialog"
    >
    <v-card class="body-card">
      <v-card-title class="title-section">
        <span class="title">
            <SgtSvgIcon
                icon="green-tick.svg"
                class="pr-3 pt-2"
            />
            {{ modalTitle }}
        </span>
        <span class="close-btn" @click="$emit('close-popup')">&times;</span>
      </v-card-title>
      <v-divider />
      <v-card-text v-if="!isSentConfirm" class="text-section" >
        <v-row class="pa-6" @click="sendToSeagate()">
            <SgtSvgIcon
                icon="send-bundle.svg"
                tooltip="Send to Seagate"
                class="pr-3"
            />
            <span>Send to Seagate</span>
        </v-row>
        <v-row class="pa-6" @click="sendToServer()">
            <SgtSvgIcon
                icon="send-bundle.svg"
                tooltip="Send to Server"
                class="pr-3"
            />
            <span>Send to Server</span>
        </v-row>
        
      </v-card-text>
      <v-card-text v-else>
          <div class="content-container">
            <v-container>
              <v-row>
                <v-col cols="3">
                  <b>Case ID :</b>
                </v-col>
                <v-col>ar137-y60ti-hsg28</v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Timestamp :</b>
                </v-col>
                <v-col>23-11-2021 12:52 PM</v-col>
              </v-row>
              <v-row>
                <v-col cols="3">
                  <b>Path :</b>
                </v-col>
                <v-col>SgtShared/ar137-y60ti-hsg28/1637652120/support.bundle</v-col>
              </v-row>
            </v-container>
          </div>
        </v-card-text>
      <v-divider />
      <v-card-actions class="action-button-container">
        <v-btn color="csmborder" @click="cancelOperation()" dark>Close</v-btn>
      </v-card-actions>
      <v-overlay
          :absolute="true"
          :value="sendingStatus"
        >
            <v-snackbar
                v-model="sendingStatus"
                centered
                :timeout="-1"
                color="#fff"
                
            >
            <span class="sending-title">
                Sending
            </span>
            
                <v-progress-linear
                indeterminate
                color="primary"
                ></v-progress-linear>
            </v-snackbar>
        </v-overlay>
    </v-card>
    
    </v-dialog>
  </template>
  
  <script lang="ts">
  import { Component, Vue } from "vue-property-decorator";
  import SgtTooltipIcon from "../../lib/components/SgtTooltipIcon/SgtTooltipIcon.vue";
  import SgtSvgIcon from "../../lib/components/SgtSvgIcon/SgtSvgIcon.vue";

  @Component({
    name: "SendTo",
    components: {
      SgtTooltipIcon,
      SgtSvgIcon
    },
  })
  export default class SendTo extends Vue {
    value: boolean = true;
    sendingStatus: boolean = false;
    isSentConfirm: boolean = false;
    modalTitle: string = "Send Support Bundle View";
    
    cancelOperation() {
        this.$emit("close-popup");
        this.modalTitle = "Send Support Bundle View";
        this.isSentConfirm = false;
    }

    sendToSeagate(){
        this.sendingStatus = true;
        setTimeout(() => {
            this.sendingStatus=false;
            this.modalTitle = "Sent to Seagate";
            this.isSentConfirm = true;
        }, 5000);
    }
    
    sendToServer(){
        this.sendingStatus = true;
        setTimeout(() => {
            this.sendingStatus=false;
            this.modalTitle = "Sent to Server";
            this.isSentConfirm = true;
        }, 5000);
    }
  }
  </script>
  <style lang="scss" scoped>
  .v-dialog {
    .row {
      margin-top: 0;
    }
  }
  .title-section {
    display: flex;
    align-items: center;
    justify-content: space-between;
    .title{
        align-items: center;
        display: flex;
    }
    .close-btn {
      color: $primary;
      font-size: 1.5rem;
      cursor: pointer;
    }
  }
  .text-section{
    font-size: 1rem;
    font-weight: bold;

    span{
      cursor: pointer;
    }
  }
  .body-card{
    position: relative;
  }
  .sending-title{
    color: #000;
    font-size: 1rem;
  }
  </style>
  