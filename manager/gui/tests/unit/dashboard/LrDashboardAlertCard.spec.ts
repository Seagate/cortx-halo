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

    it('Check if title exist and is Alerts', async () => {
        expect(wrapper.text()).toContain("Alerts");

    })


})