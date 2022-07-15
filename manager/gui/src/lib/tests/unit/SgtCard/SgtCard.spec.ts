import { createLocalVue, shallowMount } from '@vue/test-utils';
import SgtCard from "@/lib/components/SgtCard/SgtCard.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'

Vue.use(Vuetify)
describe('lib-SgtCard.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = shallowMount(SgtCard, {
            localVue,
            vuetify,
            propsData: {
                title: 'Hello world',
                showZoomIcon: true
              }
        })
    })

    it('Check if title exist', async () => {
        expect(wrapper.text()).toContain('Hello world')
    })

    it('Check if zoomIcon button exist', async () => {
        const zoomIcon = wrapper.get("sgtsvgicon-stub")
        expect(zoomIcon.exists()).toBe(true);
    })
})