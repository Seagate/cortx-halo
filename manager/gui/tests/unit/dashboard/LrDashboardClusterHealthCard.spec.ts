import { createLocalVue, mount } from '@vue/test-utils';
import LrDashboardClusterHealthCard from "@/components/dashboard/LrDashboardClusterHealthCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'
import { hexToRGB } from "@/utils/CommonUtilFunctions"

Vue.use(Vuetify)
describe('Dashboard-LrDashboardClusterHealthCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    // const localize = jest.spyOn(VueI18n, 'loadLocaleMessages').mockReturnValue()
    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(LrDashboardClusterHealthCard, {
            localVue,
            vuetify,
            // i18n
            mocks: {
                $t: () => "cluster Health Degraded"
            }
        })
    })

    it('Check if title exist and is cluster Health', async () => {
        expect(wrapper.text()).toContain("cluster Health");
    })

    it('checks if cluster detail data is populated for degraded status', async () => {
        const color = hexToRGB("#FDEDD4")
        wrapper.setData({
            clusterDetails: {
                "name": "mycluster",
                "status": "degraded"
            }
        })
        await Vue.nextTick();
        const infoCard = wrapper.get(".info-card-container");
        expect(wrapper.text()).toContain("mycluster");
        expect(wrapper.text()).toContain("Degraded");
        expect(infoCard.element.style.backgroundColor).toBe(color)
    })

    it('checks if cluster shows the right Icon', async () => {
        expect(wrapper.vm.getClusterHealthImgUrl()).toBe("health-offline-cluster.svg");
        expect(wrapper.vm.getClusterHealthImgUrl("online")).toBe("health-online-cluster.svg");
        expect(wrapper.vm.getClusterHealthImgUrl("offline")).toBe("health-offline-cluster.svg");
        expect(wrapper.vm.getClusterHealthImgUrl("degraded")).toBe("health-degraded-cluster.svg");
        expect(wrapper.vm.getClusterHealthImgUrl("failed")).toBe("health-failed-cluster.svg");
    })

    it('checks if cluster shows the right background color', async () => {
        expect(wrapper.vm.getClusterHealthBackground()).toBe("#FFFFFF");
        expect(wrapper.vm.getClusterHealthBackground("online")).toBe("#E2F2DB");
        expect(wrapper.vm.getClusterHealthBackground("offline")).toBe("#EEEEEE");
        expect(wrapper.vm.getClusterHealthBackground("degraded")).toBe("#FDEDD4");
        expect(wrapper.vm.getClusterHealthBackground("failed")).toBe("#FBE9EA");

    })

})