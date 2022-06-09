import { createLocalVue, mount } from '@vue/test-utils';
import LrSupport from "@/components/configuration/LrSupport.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'

Vue.use(Vuetify)
describe('Configuration-LrSupport.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrSupport, {
            localVue,
            vuetify,
        })
    })

    it('Check if two pannels exist', async () => {
        const expansionPanels = wrapper.findAll(".v-expansion-panel");
        expect(expansionPanels.length).toBe(2);
    })
    it('Check if first pannel is open and second is closed', async () => {
        const uploadExpansionPanel = wrapper.get("[data-test='upload-config-panel']");
        const supportExpansionPanel = wrapper.get("[data-test='support-action-panel']");
        expect(uploadExpansionPanel.classes()).toContain('v-expansion-panel--active');
        expect(supportExpansionPanel.classes()).not.toContain('v-expansion-panel--active');

    })

    //tests for panel one contents

    it('Check if protocol dropdown exist', async () => {
        const serverName = wrapper.get(".v-select__selections > [data-test='protocol']");
        expect(serverName.exists()).toBe(true);
    })

    it('Check server-name field exist', async () => {
        const serverName = wrapper.get("[data-test='server-name']");
        expect(serverName.exists()).toBe(true);
    })

    it('Check if user-name field exist', async () => {
        const userName = wrapper.get("[data-test='user-name']");
        expect(userName.exists()).toBe(true);
    })

    it('Check if password field exist', async () => {
        const password = wrapper.get("[data-test='password']");
        expect(password.exists()).toBe(true);
    })

    it('Check if location field exist', async () => {
        const location = wrapper.get("[data-test='location']");
        expect(location.exists()).toBe(true);
    })

    it('Check for required validation on protocol', async () => {
        const serverName = wrapper.get(".v-select__selections > [data-test='protocol']");
        await serverName.setValue(null)
        await Vue.nextTick();
        expect(wrapper.text()).toMatch('This field is required')
    })
    it('Check for required validation on server name', async () => {
        const serverName = wrapper.get("[data-test='server-name']");
        await serverName.setValue(null)
        await Vue.nextTick();
        expect(wrapper.text()).toMatch('This field is required')
    })
    it('Check for required validation on user name', async () => {
        const serverName = wrapper.get("[data-test='user-name']");
        await serverName.setValue(null)
        await Vue.nextTick();
        expect(wrapper.text()).toMatch('This field is required')
    })
    it('Check for required validation on password', async () => {
        const serverName = wrapper.get("[data-test='password']");
        await serverName.setValue(null)
        await Vue.nextTick();
        expect(wrapper.text()).toMatch('This field is required')
    })
    it('Check for required validation on location', async () => {
        const serverName = wrapper.get("[data-test='location']");
        await serverName.setValue(null)
        await Vue.nextTick();
        expect(wrapper.text()).toMatch('This field is required')
    })

    it('checks whether Apply button gets enable when form is valid', async () => {
        await wrapper.setData({
            supportConfig: {
                protocol: "FTP",
                userName: "Cortxadmin",
                serverName: "test server",
                password: "Seagate@1",
                location: "India"
            }
        });
        await Vue.nextTick();
        const applyBtn = wrapper.get("[data-test='apply-btn']");
        expect(applyBtn.attributes("disabled")).toBeUndefined();
    })

    it('checks whether Apply button is disabled when form is invalid', async () => {
        await wrapper.setData({
            supportConfig: {
                protocol: "FTP",
                userName: "Cortxadmin",
                serverName: "test server",
                password: "",
                location: "India"
            }
        });
        await Vue.nextTick();
        const applyBtn = wrapper.get("[data-test='apply-btn']");
        expect(applyBtn.attributes("disabled")).toBe("disabled");
    })

    it('checks form reset on reset button click', async () => {
        const resetFun = jest.spyOn(wrapper.vm, 'resetConfirmation');
        await wrapper.setData({
            supportConfig: {
                protocol: "FTP",
                userName: "Cortxadmin",
                serverName: "test server",
                password: "",
                location: "India"
            }
        });
        const resetBtn = wrapper.get("[data-test='reset-btn']");
        resetBtn.trigger('click');
        await Vue.nextTick();
        expect(resetFun).toHaveBeenCalled();
        resetFun.mockRestore();
    })

    // tests for panel 2 content

    it('Checks if support action status radio exist', async () => {
        await wrapper.setData({ panel: 1 });
        await Vue.nextTick();
        const supportRadio = wrapper.get("[data-test='support-action-status']");
        expect(supportRadio.exists()).toBe(true)
    })

    it('checks wheater the modal dialog is triggered when radio value is changed', async () => {
        const toggleRadio: any = jest.spyOn(wrapper.vm, 'toggleRadio');
        await wrapper.setData({ panel: 1 });
        await Vue.nextTick();
        await wrapper.setData({ supportAccountStatus: 'enable' });
        await Vue.nextTick();
        expect(toggleRadio).toHaveBeenCalled()
        toggleRadio.mockRestore();
    })
})