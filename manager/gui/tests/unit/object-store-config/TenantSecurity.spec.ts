import { mount, createLocalVue } from "@vue/test-utils";
import TenantSecurity from "@/components/object-store-config/TenantSecurity.vue";
import Vuetify from "vuetify";
import { Vue } from "vue-property-decorator";

Vue.use(Vuetify)

describe("TenantSecurity", () => {
  let wrapper: any;
  const localVue = createLocalVue();
  let vuetify: Vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(TenantSecurity, { localVue, vuetify });
  });

  test(`Title should be "Security"`, () => {
    const pageTitle = wrapper.get(".page-title");
    expect(pageTitle.text()).toMatch("Security");
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
  test(`Validation of protocol dropdown field - required`, async () => {
    const serverInput = wrapper.get(`.v-select__selections > [data-test="protocol-dropdown-input"]`);
    await serverInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  })

  test(`Validation of server input field - required`, async () => {
    const serverInput = wrapper.get(`[data-test="server-input"]`);
    await serverInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  })

  test(`Validation of server input field - regex`, async () => {
    const serverInput = wrapper.get(`[data-test="server-input"]`);
    await serverInput.setValue("test value");
    await Vue.nextTick();
    expect(wrapper.text()).toContain("Invalid value");
  });

  test(`Validation of port input field - required`, async () => {
    const portInput = wrapper.get(`[data-test="port-input"]`);
    await portInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  });

  test(`Validation of port input field - regex`, async () => {
    const portInput = wrapper.get(`[data-test="port-input"]`);
    await portInput.setValue("98745");
    await Vue.nextTick();
    expect(wrapper.text()).toContain("Invalid value");
  });

  test(`Validation of email input field - required`, async () => {
    const emailInput = wrapper.get(`[data-test="email-input"]`);
    await emailInput.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  });

  test(`Validation of email input field - regex`, async () => {
    const emailInput = wrapper.get(`[data-test="email-input"]`);
    await emailInput.setValue("test value");
    await Vue.nextTick();
    expect(wrapper.text()).toContain("Invalid value");
  });

  test(`Validation of password input field - required`, async () => {
    const password = wrapper.get(`[data-test="password-input"]`);
    await password.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  });

  test(`Validation of confirm password input field - required`, async () => {
    const password = wrapper.get(`[data-test="confirm-password-input"]`);
    await password.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is required");
  });

  test(`Validation of confirm password input field - password match`, async () => {
    const password = wrapper.get(`[data-test="password-input"]`);
    await password.setValue("Seagate@1");
    await Vue.nextTick();
    const confirmPasswordInput = wrapper.get(
      `[data-test="confirm-password-input"]`
    );
    await confirmPasswordInput.setValue("Seagate@2");
    await Vue.nextTick();
    expect(wrapper.text()).toContain("Passwords don't match");
  });

  test(`Validation of receiver emails input field - required`, async () => {
    const receiverEmails = wrapper.get(`[data-test="receiver-emails-input"]`);
    await receiverEmails.setValue(null);
    await Vue.nextTick();
    expect(wrapper.text()).toContain("This field is require");
  });

  test(`Validation of receiver emails input field - regex`, async () => {
    const receiverEmails = wrapper.get(`[data-test="receiver-emails-input"]`);
    await receiverEmails.setValue("random value");
    await Vue.nextTick();
    expect(wrapper.text()).toContain("Invalid value");
  });

  test(`Whether the 'test' button is disabled initially`, async () => {
    const testButton = wrapper.get(`[data-test="test-btn"]`);
    expect(testButton.attributes("disabled")).toBe("disabled");
  });

  test(`Whether the 'test' button is enabled after providing correct inputs`, async () => {
    await wrapper.setData({
      notificationSettings: {
        server: "10.25.14.36",
        port: "9225",
        protocol: "SMTP",
        senderEmail: "admin@seagate.com",
        senderPassword: "Seagate@1",
        confirmPassword: "Seagate@1",
        receiverEmails: "user1@seagate.com, user2@seagate.com",
      },
    });
    await Vue.nextTick();
    const testButton = wrapper.get(`[data-test="test-btn"]`);
    expect(testButton.attributes("disabled")).toBe(undefined);
  });

  test(`Whether the 'apply' button is disabled initially`, async () => {
    const applyButton = wrapper.get(`[data-test="apply-btn"]`);
    expect(applyButton.attributes("disabled")).toBe("disabled");
  });

  test(`Whether the 'apply' button is enabled if the inputs are valid and also verify checkbox is selected`, async () => {
    await wrapper.setData({
      notificationSettings: {
        server: "10.25.14.36",
        port: "9225",
        protocol: "SMTP",
        senderEmail: "admin@seagate.com",
        senderPassword: "Seagate@1",
        confirmPassword: "Seagate@1",
        receiverEmails: "user1@seagate.com, user2@seagate.com",
      },
      isVerified: true,
    });
    await Vue.nextTick();
    const applyButton = wrapper.get(`[data-test="apply-btn"]`);
    expect(applyButton.attributes("disabled")).toBe(undefined);
  });
});
