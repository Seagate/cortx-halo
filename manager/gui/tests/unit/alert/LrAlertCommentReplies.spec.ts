import { createLocalVue, mount } from "@vue/test-utils";
import LrAlertCommentReplies from "@/components/alerts/LrAlertCommentReplies.vue";
import Vuetify from "vuetify";
import Vue from "vue";

Vue.use(Vuetify);
describe("All alert - LrAlertCommentReplies.vue", () => {
  const localVue = createLocalVue();
  let vuetify: any;
  let wrapper: any;

  beforeEach(() => {
    vuetify = new Vuetify();
    wrapper = mount(LrAlertCommentReplies, {
      localVue,
      vuetify,
      propsData: {
        comment_id: "naytvce2892pqtnoi",
        replies: [
          {
            comment_id: "naytvce2892ncpownw",
            created_by: "admin2",
            comment_text: "This is a sample reply comment one.",
            created_time: 1655882765,
          },
          {
            comment_id: "naytvce2025utwnzbe",
            created_by: "admin2",
            comment_text: "This is a sample reply comment two.",
            created_time: 1655882765,
          },
        ],
      },
    });
  });

  it("Checks whether the corresponding method is called when 'Reply' button is clicked.", async () => {
    const replyHandler = jest.spyOn(wrapper.vm, "replyToComment");
    const showRepliesToggle = wrapper.find(".expand-collapse");
    await showRepliesToggle.trigger("click");
    const commentReplyBtn = wrapper.find("button");
    await commentReplyBtn.trigger("click");
    expect(replyHandler).toHaveBeenCalled();
    replyHandler.mockRestore();
  });
});
