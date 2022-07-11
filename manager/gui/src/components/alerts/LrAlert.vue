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
  <div v-if="showDataTable">
    <SgtDataTable
      ref="alertDataTable"
      :headers="alertConst.alertTable.headers"
      :records="alerts"
      :searchConfig="alertConst.searchConfig"
      :isMultiSelect="alertConst.alertTable.isMultiSelect"
      :multiSelectButtons="alertConst.alertTable.multiSelectButtons"
      :chips="chips"
      :itemKey="alertConst.alertTable.itemKey"
      @recommend="recommendation($event)"
      @comment="comment($event)"
      @singleAcknowledge="singleAcknowledge($event)"
      @occurrences="occurrencesHandler($event)"
      @zoom="openDetails($event)"
      @acknowledge="multiAcknowledge($event)"
      @update-record="updateRecord($event)"
    >
      <template v-slot:severity="{ data }">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-avatar
              v-bind="attrs"
              v-on="on"
              :color="getColor(data)"
              size="16"
            ></v-avatar>
          </template>
          <span class="text-capitalize">{{ data.severity }}</span>
        </v-tooltip>
      </template>
      <template v-slot:description="{ data }">{{ data.description }}</template>
    </SgtDataTable>
    <LrAlertDialog
      v-if="selectedRecord"
      :modalTitle="'Alert Details'"
      :modalData="selectedRecord"
      :showAlertDetailsDialog.sync="showAlertDetailsDialog"
    />
    <LrAlertComments
      v-if="showAlertCommentsDialog"
      :id="selectedRecord.alert_uuid"
      :showAlertCommentsDialog.sync="showAlertCommentsDialog"
    />
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop, Watch, PropSync } from "vue-property-decorator";
import SgtDataTable from "@/lib/components/SgtDataTable/SgtDataTable.vue";
import { lrAlertConst } from "./LrAlert.constant";
import { Api } from "../../services/Api";
import LrAlertDialog from "./LrAlertDialog.vue";
import LrAlertComments from "./LrAlertComments.vue";
import {
  SgtDataTableFilterSortPag,
  PaginationModel,
} from "@/lib/components/SgtDataTable/SgtDataTableFilterSortPag.model";
import { SgtFilterObject } from "@/lib/components/SgtChips/SgtFilterObject.model";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "@/lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";

@Component({
  name: "LrAlert",
  components: { SgtDataTable, LrAlertDialog, LrAlertComments },
})
export default class LrAlert extends Vue {
  @Prop({ required: false }) private alertId: string;
  @Prop({ required: false }) private severity: string;
  alertConst: any = JSON.parse(JSON.stringify(lrAlertConst));
  alerts: any = [];
  showDataTable = false;
  chips: SgtFilterObject[] = [];
  showAlertDetailsDialog = false;
  selectedRecord: any = null;
  showAlertCommentsDialog = false;
  public acknowledgeModal = create<SgtDialogModel>(SgtDialog);

  mounted() {
    this.getAlertsList();
    if (this.severity) {
      this.setSeverityFilter();
    }
    if (this.alertId) {
      let headers = this.alertConst?.alertTable?.headers;
      let actionColumn = headers[headers?.length - 1];
      actionColumn.actionList = [];
      this.alertConst.alertTable.isMultiSelect = false;
      //   getMethod for selected alert
      this.showDataTable = true;
    } else {
      this.showDataTable = true;
    }
  }

  getAlertsList(queryFilters?: string) {
    const filter = queryFilters ? `?${queryFilters}` : "";
    const endpoint = `alerts/list${filter}`;
    Api.getData(endpoint, { isDummy: true }).then((resp: any) => {
      this.alerts = resp["data"];
    });
  }

  setSeverityFilter() {
    if (this.severity) {
      let filterList: SgtFilterObject[] = [];
      const advanceForm = [...this.alertConst.searchConfig.advanceForm];
      const updatedAdvanceForm = advanceForm.map((element) => {
        if (element.name === "severity") {
          element.value = this.severity;
          filterList.push({
            label: element.label,
            name: element.name,
            value: element.value,
          });
        }
        return element;
      });
      this.alertConst.searchConfig.advanceForm = updatedAdvanceForm;
    }
  }

  getColor(item: any) {
    return this.alertConst.severityList[item.severity];
  }

  updateRecord(tableDataConfig: SgtDataTableFilterSortPag) {
    let queryFilters = ``;
    tableDataConfig.filterList.forEach((filter) => {
      queryFilters += `${filter.name}=${filter.value}`;
    });
    this.getAlertsList(queryFilters);
    this.chips = tableDataConfig.filterList;
  }

  openDetails(selectedRow: any) {
    this.selectedRecord = null;
    this.selectedRecord = JSON.parse(JSON.stringify(selectedRow));
    this.selectedRecord.extended_info = JSON.parse(
      this.selectedRecord.extended_info
    );
    this.showAlertDetailsDialog = true;
  }

  comment(selectedRow: any) {
    this.selectedRecord = null;
    this.selectedRecord = JSON.parse(JSON.stringify(selectedRow));
    this.showAlertCommentsDialog = true;
  }

  multiAcknowledge(data: any) {
    //multi select action
  }

  async singleAcknowledge(data: any) {
    const result = await this.acknowledgeModal({
      modalTitle: "Confirmation",
      modalContent: `Are you sure you want to acknowledge this alert?`,
      modalType: "prompt",
      modalContentType: "text",
    }).then((resp) => {
      if (resp === "yes") {
        //API call to acknowledge this alert
      }
    });
  }

  async recommendation(data: any) {
    const result = await this.acknowledgeModal({
      modalTitle: "Recommendation",
      modalContent: data.recommendation,
      modalType: "message",
      modalContentType: "text",
      okButtonLabel: "Close",
    });
  }

  occurrencesHandler(selectedRow: any) {
    this.$router.push({
      name: "alert-details",
      params: { alertId: selectedRow.alert_uuid },
    });
  }
}
</script>
