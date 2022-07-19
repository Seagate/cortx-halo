import { createLocalVue, mount } from "@vue/test-utils";
import LrAlert from "@/components/alerts/LrAlert.vue";
import SgtDataTable from "@/lib/components/SgtDataTable/SgtDataTable.vue";
import Vuetify from "vuetify";
import Vue from "vue";
import { Api } from "@/services/Api";

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

  it("Checks whether the data table and proper header exists", async () => {
    const alertDataTable = wrapper.findAll(".sgt-data-table");
    expect(wrapper.html()).toContain("Alert Time");
    expect(wrapper.html()).toContain("Category");
    expect(wrapper.html()).toContain("Severity");
    expect(wrapper.html()).toContain("State");
    expect(wrapper.html()).toContain("Description");
    expect(wrapper.html()).toContain("Alert Type");
    expect(alertDataTable.exists()).toBe(true);
  });

  it("Checks whether the advance search toggle and filter items exists", async () => {
    const advanceSearchToggle = wrapper.find(
      "[data-test='advance-search-toggle']"
    );

    const advanceSearchContainer = wrapper.find(".advance-search-container");
    expect(advanceSearchContainer.attributes("style")).toContain(
      "display: none"
    );

    expect(advanceSearchToggle.exists()).toBe(true);
    await advanceSearchToggle.trigger("click");
    expect(wrapper.html()).toContain("Update Date");
    expect(wrapper.html()).toContain("Resource Info");
    expect(wrapper.html()).toContain("Description");
    expect(wrapper.html()).toContain("Status");
    expect(wrapper.html()).toContain("Severity");
    expect(wrapper.html()).toContain("Category");
  });

  it("Checks whether the search button triggers the handler", async () => {
    const updateRecordHandler = jest.spyOn(wrapper.vm, "updateRecord");
    const searchButton = wrapper.find(".search-btn");
    searchButton.trigger("click");
    expect(updateRecordHandler).toHaveBeenCalled();
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
