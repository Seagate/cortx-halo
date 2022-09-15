import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardPerformanceCard from "@/components/dashboard/LrDashboardPerformanceCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/Api";

Vue.use(Vuetify)
describe('Dashboard-LrDashboardPerformanceCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "data": {
                "readThroughput": 5,
                "writeThroughput": 22,
                "unit": "Gbps"
            }
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardPerformanceCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Performance Read Throughput Write Throughput"
            }
        })
    })

    it('Check if title exist and is Performance', async () => {
        expect(mockGetData).toHaveBeenCalled()
        expect(wrapper.text()).toContain("Performance")

    })

    it('Check if the card displays proper data', async () => {
        expect(wrapper.text()).toContain("Read Throughput");
        expect(wrapper.text()).toContain("5 Gbps");
        expect(wrapper.text()).toContain("Write Throughput");
        expect(wrapper.text()).toContain("22 Gbps");
    })


})