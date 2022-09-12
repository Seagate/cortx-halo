import { createLocalVue, mount } from '@vue/test-utils';
import Tenant from "@/components/object-store-config/Tenant.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/Api";

Vue.use(Vuetify)
describe('Object-Store-Config-Tenant.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "data": {
                "fatal": "10",
                "critical": "5",
                "error": "0",
                "warning": "20",
                "informational": "17"
            }
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardAlertCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Alerts Fatal Critical Warning Error Informational"
            }
        })
    })

    it('Check if title exist and total count is visible', async () => {
        expect(mockGetData).toHaveBeenCalled()
        expect(wrapper.text()).toContain("Alerts");
        expect(wrapper.text()).toContain("55");
    })

    it('Check if the alert and their counts are visible', async () => {
        expect(wrapper.text()).toContain("Fatal 10");
        expect(wrapper.text()).toContain("Critical 5");
        expect(wrapper.text()).toContain("Error 3");
        expect(wrapper.text()).toContain("Warning 20");
        expect(wrapper.text()).toContain("Informational 17");
    })


})