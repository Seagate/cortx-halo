import { createLocalVue, mount } from "@vue/test-utils";
import LrAlertDetails from "@/components/alerts/LrAlertDetails.vue";
import SgtSvgIcon from "@/lib/components/SgtSvgIcon/SgtSvgIcon.vue";
import Vuetify from "vuetify";
import Vue from "vue";
import { Api } from "@/services/Api";

Vue.use(Vuetify);
describe("All alert - LrAlertDetails.vue", () => {
  const localVue = createLocalVue();
  let vuetify: any;
  let wrapper: any;

  const mockGetData = jest.spyOn(Api, "getData").mockResolvedValue({
    data: [
      {
        alert_uuid: "1638276506e3b3954d1c03463b8ca4ecaa84a6b92f",
        recommendation: "This is a sample recommendation text for the alert.",
        module_name: "node:os:memory_usage",
        description:
          "Host memory usage has increased to 94.2%,beyond the configured threshold of 80% for more than 30 seconds.",
        health: "",
        health_recommendation: "",
        resolved: false,
        acknowledged: false,
        severity: "warning",
        state: "Fault",
        category: "Memory",
        alert_type: "New",
        extended_info:
          '{"specific_info": {"localtime": "1638276442", "bootTime": "1638276443", "upTime": 1637655730, "uname": {"sysname": "Linux", "nodename": "ssc-vm-g3-rhev4-2588.colo.seagate.com", "version": "3.10.0-1160.el7.x86_64", "release": "#1 SMP Mon Oct 19 16:18:59 UTC 2020", "machine": "x86_64"}, "totalMemory": {"total": 8191512576, "available": 333766656, "percent": 95.9, "used": 7477370880, "free": 133812224, "active": 5865058304, "inactive": 1301692416, "buffers": 2981888, "cached": 577347584, "shared": 62230528, "slab": 456572928}, "loggedInUsers": [{"name": "935423", "terminal": "pts/0", "host": "10.4.148.186", "started": 1638271872.0, "pid": 20703}, {"name": "root", "terminal": "pts/1", "host": "10.4.148.186", "started": 1638272000.0, "pid": 20788}, {"name": "root", "terminal": "pts/2", "host": "ssc-vm-rhev4-1049.colo.seagate.com", "started": 1638276480.0, "pid": 61335}], "processCount": 238, "runningProcessCount": 0}, "info": {"resource_type": "node:os:memory_usage", "resource_id": "0", "event_time": "1638276506", "description": "Host memory usage has increased to 95.9%,beyond the configured threshold of 80% for more than 30 seconds.", "site_id": "1", "node_id": "1", "rack_id": "1", "cluster_id": "30f1ab70-2468-4fa2-b90a-dca41691019c", "fru": "false"}}',
        module_type: "memory_usage",
        updated_time: 1643300240,
        created_time: 1638276506,
        sensor_info:
          "1_1_1_30f1ab70-2468-4fa2-b90a-dca41691019c_0_node:os:memory_usage",
        host_id: "srvnode-1.mgmt.public",
        node_id: "1",
        support_message: "",
        resource_id: "0",
        hostname: "srvnode-1.mgmt.public",
      },
      {
        alert_uuid: "16382764691ff81c418c254fb2957e68a8019d8066",
        recommendation: "This is a sample recommendation text for the alert.",
        module_name: "node:sw:cortx_sw_services:sspl",
        description:
          "IEMSensor is stopped and unrecoverable. IEMSensor, Failed in monitoring IEM, (2, 'No such file or directory') /var/log/cortx/iem/iem_messages",
        health: "",
        health_recommendation: "",
        resolved: false,
        acknowledged: false,
        severity: "critical",
        state: "Fault",
        category: "Sensor",
        alert_type: "New",
        extended_info:
          '{"specific_info": {"log_file_path": "/var/log/cortx/iem/iem_messages", "threaded": true, "timestamp_file_path": "/var/cortx/sspl/data/iem/last_processed_msg_time"}, "info": {"event_time": "1638276469", "resource_id": "IEMSensor", "resource_type": "node:sw:cortx_sw_services:sspl", "description": "IEMSensor is stopped and unrecoverable. IEMSensor, Failed in monitoring IEM, (2, \'No such file or directory\') /var/log/cortx/iem/iem_messages", "impact": "CORTX Software Events(IEMs) can not be processed and highlighted.", "recommendation": "Restart SSPL service", "site_id": "1", "node_id": "1", "rack_id": "1", "cluster_id": "30f1ab70-2468-4fa2-b90a-dca41691019c", "fru": "false"}}',
        module_type: "sspl",
        updated_time: 1638276469,
        created_time: 1638276469,
        sensor_info:
          "1_1_1_30f1ab70-2468-4fa2-b90a-dca41691019c_IEMSensor_node:sw:cortx_sw_services:sspl",
        host_id: "srvnode-1.mgmt.public",
        node_id: "1",
        support_message:
          "Please contact Seagate Support via https://www.seagate.com/direct-partners/",
        resource_id: "IEMSensor",
        hostname: "srvnode-1.mgmt.public",
      },
      {
        alert_uuid: "1640554971f7870d69dd9a4eef87938804521c8fe6",
        recommendation: "This is a sample recommendation text for the alert.",
        module_name: "node:sw:os:service",
        description: "kafka.service in active state from last 30 seconds.",
        health: "",
        health_recommendation: "",
        resolved: true,
        acknowledged: false,
        severity: "informational",
        state: "Fault_resolved",
        category: "Server",
        alert_type: "Active",
        extended_info:
          '{"specific_info": {"service_name": "kafka.service", "previous_state": "failed", "state": "active", "previous_substate": "NA", "substate": "running", "previous_pid": "NA", "pid": "1719"}, "info": {"resource_type": "node:sw:os:service", "resource_id": "kafka.service", "event_time": "1643300199", "description": "kafka.service in active state from last 30 seconds.", "impact": "kafka.service service is available now.", "recommendation": "No action required", "site_id": "1", "node_id": "1", "rack_id": "1", "cluster_id": "30f1ab70-2468-4fa2-b90a-dca41691019c", "fru": "false"}}',
        module_type: "service",
        updated_time: 1643300219,
        created_time: 1643300199,
        sensor_info:
          "1_1_1_30f1ab70-2468-4fa2-b90a-dca41691019c_kafka.service_node:sw:os:service",
        host_id: "srvnode-1.mgmt.public",
        node_id: "1",
        support_message: "",
        resource_id: "kafka.service",
        hostname: "srvnode-1.mgmt.public",
      },
    ],
  });

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(LrAlertDetails, {
      localVue,
      vuetify,
      propsData: { alertId: "1638276506e3b3954d1c03463b8ca4ecaa84a6b92f" },
    });
  });

  it("Check if titles exist and is 'Alert' and 'Occurrences'", async () => {
    expect(mockGetData).toHaveBeenCalled();

    const alertTitle = wrapper.find(".top-section .section-title");
    expect(alertTitle.html()).toContain("Alert");
    const occurrencesTitle = wrapper.find(".alert-title-container");
    expect(occurrencesTitle.html()).toContain("Occurrences");
  });

  it("Checks whether the alert details section contains all the titles.", async () => {
    const alertDetailsContainer = wrapper.find(".alert-details-container");
    expect(alertDetailsContainer.html()).toContain("Resource name");
    expect(alertDetailsContainer.html()).toContain("Alert Type");
    expect(alertDetailsContainer.html()).toContain("Severity");
    expect(alertDetailsContainer.html()).toContain("State");
    expect(alertDetailsContainer.html()).toContain("Created Time");
    expect(alertDetailsContainer.html()).toContain("Reason");
    expect(alertDetailsContainer.html()).toContain("Category");
    expect(alertDetailsContainer.html()).toContain("Site");
    expect(alertDetailsContainer.html()).toContain("Rack");
    expect(alertDetailsContainer.html()).toContain("Node");
    expect(alertDetailsContainer.html()).toContain("Cluster");
  });

  it("Checks whether the action icons are present", async () => {
    const actionIconContainer = wrapper.find(".action-icons");
    const actionIcons = actionIconContainer.findAll(".sgt-icon-container");
    expect(actionIcons.length).toBe(4);
  });

  it("Checks whether the handlers for action icons are called properly", async () => {
    const actionIconsContainer = wrapper.find(".action-icons");
    const actionIcons = actionIconsContainer.findAllComponents(SgtSvgIcon);

    const recommendationHandler = jest.spyOn(wrapper.vm, "recommendation");
    const recommendationIcon = actionIcons.at(0);
    recommendationIcon.vm.$emit("click");
    expect(recommendationHandler).toHaveBeenCalled();

    const acknowledgeHandler = jest.spyOn(wrapper.vm, "singleAcknowledge");
    const acknowledgeIcon = actionIcons.at(1);
    await acknowledgeIcon.vm.$emit("click");
    expect(acknowledgeHandler).toHaveBeenCalled();

    const commentHandler = jest.spyOn(wrapper.vm, "comment");
    const commentIcon = actionIcons.at(2);
    await commentIcon.vm.$emit("click");
    expect(commentHandler).toHaveBeenCalled();

    const openDetailsHandler = jest.spyOn(wrapper.vm, "openDetails");
    const magnifyIcon = actionIcons.at(3);
    await magnifyIcon.vm.$emit("click");
    expect(openDetailsHandler).toHaveBeenCalled();
  });

  it("Checks whether the data table exists for occurences.", async () => {
    const alertDataTable = wrapper.find(".sgt-data-table");
    expect(alertDataTable.exists()).toBe(true);
  });

  it("Checks whether the resource info filter is applied for occurences table.", async () => {
    const filterChip = wrapper.find(".sgt-data-table .v-chip__content");
    expect(filterChip.html()).toContain("Resource Info :");
  });
});
