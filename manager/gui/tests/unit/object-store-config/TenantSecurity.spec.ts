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
    const pageTitle = wrapper.findAll(".page-title").at(0);
    expect(pageTitle.text()).toMatch("Security");
  });

  test(`Title should be "Encryption"`, () => {
    const pageTitle = wrapper.findAll(".page-title").at(1);
    expect(pageTitle.text()).toMatch("Encryption");
  });

  test(`Presence of Enable TLS Toggle`, () => {
    const enableTLSToggle = wrapper.find(
      `[data-test="enable-tls-toggle"]`
    );
    expect(enableTLSToggle.exists()).toBe(true);
  });

  test(`Presence of Enable AutoCert Toggle`, () => {
    const enableAutoCert = wrapper.find(`[data-test="enable-auto-cert-toggle"]`);
    expect(enableAutoCert.exists()).toBe(true);
  });

  test(`Presence of Custom Certificate Toggle`, () => {
    const customCertToggle = wrapper.find(`[data-test="custom-certificates-toggle"]`);
    expect(customCertToggle.exists()).toBe(true);
  });

  test(`Presence of Enable Server Side Encryption Toggle`, () => {
    const enableSSEncryToggle = wrapper.find(`[data-test="server-side-exception-toggle"]`);
    expect(enableSSEncryToggle.exists()).toBe(true);
  });

  test(`Check Enable TLS Toggle is working`, async () => {
    const enableTLSToggle = wrapper.find(
      `[data-test="enable-tls-toggle"]`
    );
    console.log("before ", wrapper.vm.toggleStates.enableTls);
    await enableTLSToggle.trigger("click");
    await Vue.nextTick();
    console.log("after ", wrapper.emitted());
    
    expect(wrapper.vm.toggleStates.enableTls).toBe(false);
  });
  
});
