import { createLocalVue, mount } from '@vue/test-utils';
import SgtToggle from "@/lib/components/SgtToggle/SgtToggle.vue";
import Vuetify from 'vuetify';
import Vue from 'vue'

Vue.use(Vuetify)
describe('lib-SgtToggle.vue', () => {
    const localVue = createLocalVue();
    let vuetify: any;
    let wrapper: any;
    let toggleState: boolean = false;

    beforeEach(() => {
        vuetify = new Vuetify()
        wrapper = mount(SgtToggle, {
            localVue,
            vuetify,
            propsData: {
                labelPre: 'Test Pre Label',
                labelPost: 'Test Post Label',
                areToggleLabel: true,
                tooltip: toggleState ? 'Test On' : 'Test Off',
                value: toggleState,
              }
        })
    })


    it('Check if both labels exist and rendered correctly', async () => {
        const preLabel = wrapper.findAll("[data-test='toggle-pre-label']");
        const postLabel = wrapper.findAll("[data-test='toggle-post-label']");
        expect(preLabel.length).toBe(1);
        expect(postLabel.length).toBe(1);
        expect(preLabel.at(0).text()).toBe("Test Pre Label");
        expect(postLabel.at(0).text()).toBe("Test Post Label");
    })

    it('Check if toggle button exists', async () => {
        const toggleContainer = wrapper.find(".toggle-container");
        expect(toggleContainer.exists()).toBe(true);
    })

    it('Check if toggle button exists', async () => {
        const toggleContainer = wrapper.find(".toggle-container");
        expect(toggleContainer.exists()).toBe(true);
    })

    it('Check if toggle is off by default', async () => {
        expect(wrapper.vm.value).toBe(false);
    })

    it('Check if toggle is working on click', async () => {
        const toggleContainer = wrapper.find(".toggle-container");
        await toggleContainer.trigger('click');
        console.log(toggleContainer.classes());
        expect(wrapper.emitted().change.length).toBe(1);
        expect(wrapper.emitted().change[0][0]).toBe(true);
    })
})