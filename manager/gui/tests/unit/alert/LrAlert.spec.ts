import { createLocalVue, mount } from "@vue/test-utils";
import LrAlert from "@/components/alerts/LrAlert.vue";
import SgtDataTable from "@/lib/components/SgtDataTable/SgtDataTable.vue";
import Vuetify from "vuetify";
import Vue from "vue";

Vue.use(Vuetify);
describe("All alert - LrAlert.vue", () => {
  const localVue = createLocalVue();
  let vuetify: any;
  let wrapper: any;

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(LrAlert, {
      localVue,
      vuetify,
    });
  });

  it("Checks whether the data table exists", async () => {
    const alertDataTable = wrapper.findAll(".sgt-data-table");
    expect(alertDataTable.exists()).toBe(true);
  });

  it("Checks whether recommendation handler is called", async () => {
    const recommendationHandler = jest.spyOn(wrapper.vm, "recommendation");
    const alertTable = wrapper.findComponent(SgtDataTable);
    alertTable.vm.$emit("recommend");
    await wrapper.vm.$nextTick();
    expect(recommendationHandler).toHaveBeenCalled();
    recommendationHandler.mockRestore();
  });

  it("Checks whether comment handler is called", async () => {
    const commentHandler = jest.spyOn(wrapper.vm, "comment");
    const alertTable = wrapper.findComponent(SgtDataTable);
    alertTable.vm.$emit("comment");
    await wrapper.vm.$nextTick();
    expect(commentHandler).toHaveBeenCalled();
    commentHandler.mockRestore();
  });

  it("Checks whether singleAcknowledge handler is called", async () => {
    const singleAcknowledgeHandler = jest.spyOn(
      wrapper.vm,
      "singleAcknowledge"
    );
    const alertTable = wrapper.findComponent(SgtDataTable);
    alertTable.vm.$emit("singleAcknowledge");
    await wrapper.vm.$nextTick();
    expect(singleAcknowledgeHandler).toHaveBeenCalled();
    singleAcknowledgeHandler.mockRestore();
  });

  it("Checks whether occurrences handler is called", async () => {
    const occurrencesHandler = jest.spyOn(wrapper.vm, "occurrencesHandler");
    const alertTable = wrapper.findComponent(SgtDataTable);
    alertTable.vm.$emit("occurrences");
    await wrapper.vm.$nextTick();
    expect(occurrencesHandler).toHaveBeenCalled();
    occurrencesHandler.mockRestore();
  });

  it("Checks whether zoom handler is called", async () => {
    const openDetails = jest.spyOn(wrapper.vm, "openDetails");
    const alertTable = wrapper.findComponent(SgtDataTable);
    alertTable.vm.$emit("zoom");
    await wrapper.vm.$nextTick();
    expect(openDetails).toHaveBeenCalled();
    openDetails.mockRestore();
  });
});
