import { mount, createLocalVue } from "@vue/test-utils";
import TenantSetup from "@/components/object-store-config/TenantSetup.vue";
import Vuetify from "vuetify";
import { Vue } from "vue-property-decorator";

Vue.use(Vuetify)

describe("TenantSetup", () => {
  let wrapper: any;
  const localVue = createLocalVue();
  let vuetify: Vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(TenantSetup, { localVue, vuetify });
  });

  test(`Title should be "Name"`, () => {
    const pageTitle = wrapper.findAll(".page-title").at(0);
    expect(pageTitle.text()).toMatch("Name");
  });

  test(`Title should be "Capacity"`, () => {
    const pageTitle = wrapper.findAll(".page-title").at(1);
    expect(pageTitle.text()).toMatch("Capacity");
  });

  test(`Presence of username input field`, () => {
    const usernameInput = wrapper.find(
      `[data-test="username-input"]`
    );
    expect(usernameInput.exists()).toBe(true);
  });

  test(`Presence of Number of server field`, () => {
    const noOfserverInput = wrapper.find(`[data-test="no-of-server-input"]`);
    expect(noOfserverInput.exists()).toBe(true);
  });

  test(`Presence of Drives per server field`, () => {
    const drivesPerServerInput = wrapper.find(`[data-test="drives-per-server-input"]`);
    expect(drivesPerServerInput.exists()).toBe(true);
  });

  test(`Presence of Total size field`, () => {
    const totalSizeInput = wrapper.find(`[data-test="total-size-input"]`);
    expect(totalSizeInput.exists()).toBe(true);
  });

  test(`Presence of Ensure Code Parity dropdown`, () => {
    const ensureCodeParityInput = wrapper.find(`[data-test="ensure-code-parity-dropdown"]`);
    expect(ensureCodeParityInput.exists()).toBe(true);
  });

  
  test(`Validation of Ensure Code Parity dropdown field - required`, async () => {
    const ensureCodeParityInput = wrapper.get(`.v-select__selections > [data-test="ensure-code-parity-dropdown"]`);
    await ensureCodeParityInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  })

  test(`Validation of Number of server field - required`, async () => {
    const noOfserverInput = wrapper.get(`[data-test="no-of-server-input"]`);
    await noOfserverInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  })

  test(`Validation of Drives per Server field - required`, async () => {
    const drivesPerServerInput = wrapper.get(`[data-test="drives-per-server-input"]`);
    await drivesPerServerInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  });

  test(`Validate if the Total Size is disabled`, async () => {
    const totalSizeInput = wrapper.find(`[data-test="total-size-input"]`);
    expect(totalSizeInput.attributes().disabled).toBe("disabled");
  });

  test(`Validate if the Total Size is calculated properly`, async () => {
    const drivesPerServerInput = wrapper.get(`[data-test="drives-per-server-input"]`);
    await drivesPerServerInput.setValue(3);
    await Vue.nextTick();
    
    const noOfserverInput = wrapper.get(`[data-test="no-of-server-input"]`);
    await noOfserverInput.setValue(2);
    await Vue.nextTick();

    const totalSizeInput = wrapper.find(`[data-test="total-size-input"]`);
    expect(totalSizeInput.element.value).toBe("384");
  });


});
