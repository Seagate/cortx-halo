import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardCapacityCard from "@/components/dashboard/LrDashboardCapacityCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/api";

Vue.use(Vuetify)
describe('Dashboard-LrDashboardCapacityCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "data": {
                "size": 77309411328,
                "available": 67309411328,
                "used": 10000000000,
                "usagePercentage": 15
            }
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardCapacityCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Capacity"
            }
        })
    })

    it('Check if title exist and usage percent is visible', async () => {
        expect(mockGetData).toHaveBeenCalled()
        expect(wrapper.text()).toContain("Capacity");
        expect(wrapper.text()).toContain("15%");
    })

    it('Check if the total is visible', async () => {
        expect(wrapper.text()).toContain("72.00 GB");
    })
    it('Check if the used capacity is visible', async () => {
        expect(wrapper.text()).toContain("9.31 GB");
    })
    it('Check if the available capacity is visible', async () => {
        expect(wrapper.text()).toContain("62.69 GB");
    })

})