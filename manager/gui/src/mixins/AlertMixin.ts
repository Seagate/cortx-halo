/*
 * CORTX-CSM: CORTX Management web and CLI interface.
 * Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
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
 * please email opensource@seagate.com or cortx-questions@seagate.com.
 */
import { Component, Vue } from "vue-property-decorator";
import SgtDialog from "@/lib/components/SgtDialog/SgtDialog.vue";
import { SgtDialogModel } from "@/lib/components/SgtDialog/SgtDialog.model";
import { create } from "vue-modal-dialogs";

@Component
export default class AlertMixin extends Vue {
  selectedRecord: any = null;
  showAlertDetailsDialog = false;
  showAlertCommentsDialog = false;
  public acknowledgeModal = create<SgtDialogModel>(SgtDialog);

  async recommendation(data: any) {
    const result = await this.acknowledgeModal({
      modalTitle: "Recommendation",
      modalContent: data.recommendation,
      modalType: "message",
      modalContentType: "text",
      okButtonLabel: "Close",
    });
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

  comment(selectedRow: any) {
    this.selectedRecord = null;
    this.selectedRecord = JSON.parse(JSON.stringify(selectedRow));
    this.showAlertCommentsDialog = true;
  }

  openDetails(selectedRow: any) {
    this.selectedRecord = null;
    this.selectedRecord = JSON.parse(JSON.stringify(selectedRow));
    this.selectedRecord.extended_info = JSON.parse(
      this.selectedRecord.extended_info
    );
    this.showAlertDetailsDialog = true;
  }
}
