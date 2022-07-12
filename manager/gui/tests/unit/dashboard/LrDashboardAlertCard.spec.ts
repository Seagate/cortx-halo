import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardAlertCard from "@/components/dashboard/LrDashboardAlertCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/api";

Vue.use(Vuetify)
describe('Dashboard-LrDashboardAlertCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
                "fatal": "10",
                "critical": "5",
                "error": "3",
                "warning": "20",
                "informational": "17"
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