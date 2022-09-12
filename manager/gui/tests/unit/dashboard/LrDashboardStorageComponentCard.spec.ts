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
                "buckets": 5,
                "objects": 22,
                "underReplicated": 12,
                "S3 Account": 37,
                "IAM User": 20,
                "Tenants": 7
            }
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardStorageComponentsCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Storage Components Buckets Objects Under Replicated S3 Account IAM User Tenants"
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
        expect(wrapper.text()).toContain("S3 Account");
        expect(wrapper.text()).toContain("IAM User");
        expect(wrapper.text()).toContain("Tenants");

        expect(wrapper.text()).toContain("5");
        expect(wrapper.text()).toContain("22");
        expect(wrapper.text()).toContain("12");
        expect(wrapper.text()).toContain("37");
        expect(wrapper.text()).toContain("20");
        expect(wrapper.text()).toContain("7");

    })

})