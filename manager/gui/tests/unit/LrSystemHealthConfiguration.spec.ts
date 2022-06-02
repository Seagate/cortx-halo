import { mount, createLocalVue } from "@vue/test-utils";
import LrSystemHealthConfiguration from "@/components/configuration/LrSystemHealthConfiguration.vue";
import Vuetify from "vuetify";

describe("LrSystemHealthConfiguration", () => {
  let wrapper: any;
  const localVue = createLocalVue();
  let vuetify: Vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(LrSystemHealthConfiguration, { localVue, vuetify });
  });

  test(`Title should be "System Health"`, () => {
    const pageTitle = wrapper.get(".page-title");
    expect(pageTitle.text()).toMatch("System Health");
  });

  test(`Presence of protocol dropdown field`, () => {
    const protocolDropdown = wrapper.find(
      `[data-test="protocol-dropdown-input"]`
    );
    expect(protocolDropdown.exists()).toBe(true);
  });

  test(`Presence of server input field`, () => {
    const serverInput = wrapper.find(`[data-test="server-input"]`);
    expect(serverInput.exists()).toBe(true);
  });

  test(`Presence of port input field`, () => {
    const portInput = wrapper.find(`[data-test="port-input"]`);
    expect(portInput.exists()).toBe(true);
  });

  test(`Presence of email input field`, () => {
    const emailInput = wrapper.find(`[data-test="email-input"]`);
    expect(emailInput.exists()).toBe(true);
  });

  test(`Presence of password input field`, () => {
    const passwordInput = wrapper.find(`[data-test="password-input"]`);
    expect(passwordInput.exists()).toBe(true);
  });

  test(`Presence of confirm password input field`, () => {
    const confirmPasswordInput = wrapper.find(
      `[data-test="confirm-password-input"]`
    );
    expect(confirmPasswordInput.exists()).toBe(true);
  });

  test(`Presence of receiver emails input field`, () => {
    const receiverEmailsInput = wrapper.find(
      `[data-test="receiver-emails-input"]`
    );
    expect(receiverEmailsInput.exists()).toBe(true);
  });

  test(`Presence of test cta button.`, () => {
    const testButton = wrapper.find(`[data-test="test-btn"]`);
    expect(testButton.exists()).toBe(true);
  });

  test(`Presence of verified checkbox field`, () => {
    const verifiedCheckbox = wrapper.find(`[data-test="verified-checkbox"]`);
    expect(verifiedCheckbox.exists()).toBe(true);
  });

  test(`Presence of apply button`, () => {
    const applyButton = wrapper.find(`[data-test="apply-btn"]`);
    expect(applyButton.exists()).toBe(true);
  });

  test(`Presence of reset button`, () => {
    const resetButton = wrapper.find(`[data-test="reset-btn"]`);
    expect(resetButton.exists()).toBe(true);
  });

  test(`Validation of server input field`, async () => {
    const serverInput = wrapper
      .findComponent({ name: "v-text-field" })
      .find(`[data-test="server-input"]`);

    await serverInput.setValue("test value");

    const serverInputContainer = wrapper
      .findAllComponents({ name: "v-col" })
      .filter(
        (w: any) => w.attributes()["data-test"] === "server-input-container"
      )
      .at(0);
    console.log("server input container: ", serverInputContainer.html());

    expect(serverInputContainer.find(".v-input.error-text").exists()).toBe(
      true
    );
  });
});
