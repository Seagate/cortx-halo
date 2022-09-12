import { createLocalVue, mount } from "@vue/test-utils";
import LrAlertComments from "@/components/alerts/LrAlertComments.vue";
import Vuetify from "vuetify";
import Vue from "vue";

Vue.use(Vuetify);

function addElemWithDataAppToBody() {
  // This is needed to render the v-dialog
  // We need wrap it with data-app
  const app = document.createElement('div');
  app.setAttribute('data-app', 'true');
  document.body.append(app);
};

describe("All alert - LrAlertComments.vue", () => {
  
  const localVue = createLocalVue();
  let vuetify: any;
  let wrapper: any;

  addElemWithDataAppToBody();
  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(LrAlertComments, {
      localVue,
      vuetify,
      propsData: {
        id: "naytvce2892pqtnoi",
        showAlertCommentsDialog: true,
      },
    });
  });

  it("Checks that the replies are not visible by default", async () => {
    const commentRepliesContainer = wrapper.find(".comment-replies-container");
    expect(commentRepliesContainer.exists()).toBe(false);
  });

  it("Checks that the replies are visible after clicking on 'Show replies'", async () => {
    const showRepliesToggle = wrapper.find(".expand-collapse");
    await showRepliesToggle.trigger("click");
    const commentRepliesContainer = wrapper.find(".comment-replies-container");
    expect(commentRepliesContainer.exists()).toBe(true);
  });

  it("Checks whether the corresponding method is called when 'Comment' button is clicked.", async () => {
    const addCommentFunc = jest.spyOn(wrapper.vm, "addComment");
    const addCommentButton = wrapper.find("[data-test='comment-btn']");
    await addCommentButton.trigger("click");
    expect(addCommentFunc).toHaveBeenCalled();
    addCommentFunc.mockRestore();
  });
});
