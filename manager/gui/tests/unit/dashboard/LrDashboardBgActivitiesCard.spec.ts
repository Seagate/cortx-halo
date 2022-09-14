import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardBgActivitiesCard from "@/components/dashboard/LrDashboardBgActivitiesCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/Api";

Vue.use(Vuetify)
describe('Dashboard-LrDashboardBgActivitiesCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "tasks": 7
        });

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardBgActivitiesCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Background Activities"
            }
        })
    })

    it('Check if title exist and is Background Activities', async () => {
        expect(wrapper.text()).toContain("Background Activities");

    })

    it('Check if card details are present and total task is visible', async () => {
        expect(wrapper.text()).toContain("7 tasks");
    })

})