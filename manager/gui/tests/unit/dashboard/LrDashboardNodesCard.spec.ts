import { createLocalVue, mount, Wrapper } from '@vue/test-utils';
import LrDashboardNodesCard from "@/components/dashboard/LrDashboardNodesCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { Api } from "@/services/api";
import { hexToRGB } from "@/utils/CommonUtilFunctions"
Vue.use(Vuetify)
describe('Dashboard-LrDashboardNodesCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    const mockGetData = jest.spyOn(Api, 'getData')
        .mockResolvedValue({
            "cluster": {
                "name": "mycluster",
                "status": "degraded"
            },
            "nodes": {
                "online": 5,
                "offline": 7,
                "failed": 0,
                "degraded": 9
            }
        });
    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardNodesCard, {
            localVue,
            vuetify,
            mocks: {
                $t: () => "Online Offline Degraded Failed"
            }
        })
    })

    it('Check if title exist and total count is visible', async () => {
        await wrapper.vm.getHealthData();
        await Vue.nextTick()
        expect(mockGetData).toHaveBeenCalled()
        expect(wrapper.text()).toContain("21 nodes");
    })

    it('checks if 4 statues are visible on card', async () => {
        const infoCard = wrapper.findAll("[data-test='info-card']");
        expect(infoCard.length).toBe(4)
    })

    it('checks if first status is online and count is 5', async () => {
        const color = hexToRGB("#E2F2DB")
        const infoCard = wrapper.findAll("[data-test='info-card']");
        const info = infoCard.at(0).get(".info-card-container");
        expect(info.text()).toContain("Online");
        expect(info.text()).toContain("5");
        expect(info.element.style.backgroundColor).toBe(color)
    })

    it('checks if second status is offline and count is 7', async () => {
        const color = hexToRGB("#EEEEEE")
        const infoCard = wrapper.findAll("[data-test='info-card']");
        const info = infoCard.at(1).get(".info-card-container");
        expect(info.text()).toContain("Offline");
        expect(info.text()).toContain("7");
        expect(info.element.style.backgroundColor).toBe(color)
    })

    it('checks if third status is failed and count is 0', async () => {
        const color = hexToRGB("#FBE9EA")
        const infoCard = wrapper.findAll("[data-test='info-card']");
        const info = infoCard.at(2).get(".info-card-container");
        expect(info.text()).toContain("Failed");
        expect(info.text()).toContain("0");
        expect(info.element.style.backgroundColor).toBe(color)
    })

    it('checks if forth status is degraded and count is 9', async () => {
        const color = hexToRGB("#FDEDD4")
        const infoCard = wrapper.findAll("[data-test='info-card']");
        const info = infoCard.at(3).get(".info-card-container");
        expect(info.text()).toContain("Degraded");
        expect(info.text()).toContain("9");
        expect(info.element.style.backgroundColor).toBe(color)
    })

})