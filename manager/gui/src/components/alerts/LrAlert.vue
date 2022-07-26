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
import {
  Component,
  Vue,
  Prop,
  Watch,
  PropSync,
  Mixins,
} from "vue-property-decorator";
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
import AlertMixin from "@/mixins/AlertMixin";

@Component({
  name: "LrAlert",
  components: { SgtDataTable, LrAlertDialog, LrAlertComments },
})
export default class LrAlert extends Mixins(AlertMixin) {
  @Prop({ required: false }) private alertId: string;
  @Prop({ required: false }) private severity: string;
  @Prop({ required: false }) private resourceInfo: string;
  alertConst: any = JSON.parse(JSON.stringify(lrAlertConst));
  alerts: any = [];
  showDataTable = false;
  chips: SgtFilterObject[] = [];

  mounted() {
    if (this.severity) {
      this.setFilter("severity", this.severity);
    } else if (this.resourceInfo) {
      this.setFilter("resourceInfo", this.resourceInfo);
    } else {
      this.getAlertsList();
    }

    if (this.alertId) {
      this.alertConst.alertTable.isMultiSelect = false;
      //   getMethod for selected alert
      this.showDataTable = true;
    } else {
      this.showDataTable = true;
    }
  }

  async getAlertsList(queryFilters?: string, chipsData?: any[]) {
    const filter = queryFilters ? `?${queryFilters}` : "";
    const endpoint = `alerts/list${filter}`;
    const res: any = await Api.getData(endpoint, { isDummy: true });
    this.alerts = res["data"];
    if (chipsData) {
      this.chips = chipsData;
    }
  }

  setFilter(filterName: string, filterValue: string) {
    const advanceForm = [...this.alertConst.searchConfig.advanceForm];
    const formElementIndex = advanceForm.findIndex(
      (element) => element.name === filterName
    );
    const formElement =
      this.alertConst.searchConfig.advanceForm[formElementIndex];
    formElement.value = filterValue;
    formElement.editable = false;
  }

  getColor(item: any) {
    return this.alertConst.severityList[item.severity];
  }

  updateRecord(tableDataConfig: SgtDataTableFilterSortPag) {
    let queryFilters = ``;
    tableDataConfig.filterList.forEach((filter) => {
      queryFilters += `${filter.name}=${filter.value}`;
    });
    this.getAlertsList(queryFilters, tableDataConfig.filterList);
  }

  multiAcknowledge(data: any) {
    //multi select action
  }

  occurrencesHandler(selectedRow: any) {
    this.$router.push({
      name: "alert-details",
      params: { alertId: selectedRow.alert_uuid },
    });
  }
}
</script>
