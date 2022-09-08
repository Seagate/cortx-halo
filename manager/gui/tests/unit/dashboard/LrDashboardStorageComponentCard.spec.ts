import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardStorageComponentsCard from "@/components/dashboard/LrDashboardStorageComponentsCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/Api";

Vue.use(Vuetify)
describe('Dashboard-LrDashboardStorageComponentsCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "data": {
                "buckets": 7,
                "objects": 20,
                "underReplicated": 10,
                "S3Account": 25,
                "IAMUser": 30,
                "dummyText": 4
            }
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardStorageComponentsCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Storage Components Buckets Objects Under Replicated S3Account IAMUser dummyText"
            }
        })
    })

    it('Check if title exist', async () => {
        expect(mockGetData).toHaveBeenCalled()
        expect(wrapper.text()).toContain("Storage Components");
    })

    it('checks if 6 components are visible on card', async () => {
        const infoCard = wrapper.findAll("[data-test='info-card']");
        expect(infoCard.length).toBe(6)
    })

    it('checks if 6 components have the expected data', async () => {
        expect(wrapper.text()).toContain("Buckets");
        expect(wrapper.text()).toContain("Objects");
        expect(wrapper.text()).toContain("Under Replicated");
        expect(wrapper.text()).toContain("S3Account");
        expect(wrapper.text()).toContain("IAMUser");
        expect(wrapper.text()).toContain("dummyText");

        expect(wrapper.text()).toContain("7");
        expect(wrapper.text()).toContain("20");
        expect(wrapper.text()).toContain("25");
        expect(wrapper.text()).toContain("30");
        expect(wrapper.text()).toContain("10");
        expect(wrapper.text()).toContain("4");

    })

})