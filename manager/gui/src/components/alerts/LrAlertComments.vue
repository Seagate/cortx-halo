<!--
* CORTX-Halo: Halo Management GUI.
* Copyright (c) 2022 Seagate Technology LLC and/or its Affiliates
* This program is free software: you can redistribute it and/or modify
* it under the terms of the GNU Affero General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
* GNU Affero General Public License for more details.
* You should have received a copy of the GNU Affero General Public License
* along with this program. If not, see <https://www.gnu.org/licenses/>.
* For any questions about this software or licensing,
* please email opensource@seagate.com.
-->
<template>
  <v-dialog v-model="dialog" scrollable max-width="600px">
    <v-card>
      <v-card-title>
        <div class="title-container">
          Comments
          <img
            :src="require(`@/assets/icons/close-green.svg`)"
            @click="dialog = false"
            class="close-btn"
            alt="logo"
          />
        </div>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="card-content-container">
        <div class="no-comment-label" v-if="alertComments.length === 0">
          No Comments
        </div>
        <div class="comments-container" v-else>
          <div
            class="lr-comment"
            v-for="comment in alertComments"
            :key="comment.comment_id"
          >
            <div class="comment-wrapper">
              <div class="created-by">
                {{ comment.created_by }}
              </div>
              <div class="comment-timestamp">
                {{ formatCommentTime(new Date(comment.created_time * 1000)) }}
              </div>
              <div class="comment-text mt-1">
                {{ comment.comment_text }}
              </div>
            </div>

            <LrAlertCommentReplies
              :comment_id="comment.comment_id"
              :replies="comment.replies"
            />
          </div>
        </div>
        <div class="comment-input">
          <v-textarea
            outlined
            name="comment"
            label="Add Comment"
            rows="3"
            row-height="30"
            v-model.trim="commentText"
            :no-resize="true"
            hide-details="auto"
          ></v-textarea>
          <span class="error-txt sub-txt">{{ errorMsg }}</span>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions class="action-button-container">
        <v-btn
          color="primary"
          @click="addComment()"
          data-test="comment-btn"
          class="mr-2"
          dark
          >Comment</v-btn
        >
        <v-btn color="csmdisabled" @click="dialog = false" dark>Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script lang="ts">
import { Component, Vue, Prop, PropSync } from "vue-property-decorator";
import { Api } from "../../services/Api";
import { AlertCommentModel } from "./LrAlertComment.model";
import { formatCommentTime } from "@/utils/CommonUtilFunctions";
import LrAlertCommentReplies from "./LrAlertCommentReplies.vue";
@Component({
  name: "LrAlertComments",
  components: {
    LrAlertCommentReplies,
  },
})
export default class LrAlertComments extends Vue {
  @Prop({ required: true }) private id: any;
  private alertComments: AlertCommentModel[] = [];
  @PropSync("showAlertCommentsDialog", { required: false, default: false })
  private dialog: boolean;
  private commentText = "";
  private errorMsg = "";

  async mounted() {
    //Id in the below api path should be alert id (this.id)
    const res: any = await Api.getData(
      "alerts/comment/1638276506e3b3954d1c03463b8ca4ecaa84a6b92f",
      { isDummy: true }
    );
    this.alertComments = res.data;
  }

  formatCommentTime(time: number) {
    return formatCommentTime(time);
  }

  addComment() {
    if (!this.commentText) this.errorMsg = "Comment Required";
    else if (this.commentText.length > 250)
      this.errorMsg = "Comment Cannot Be More Than 250 Char";
    else {
      this.errorMsg = "";
      // code to post the comment
    }
  }

  replyToComment(comment_id: string, event: any) {
    //Make the API call to reply to the comment.
  }
}
</script>
<style lang="scss" scoped>
.title-container {
  width: 100%;
  font-weight: bold;
  .close-btn {
    cursor: pointer;
    float: right;
  }
}
.sub-txt {
  font-size: 0.8rem;
}
.error-txt {
  color: red;
}
.comment-input {
  margin-top: 1rem;

  .v-text-field__details {
    display: none;
  }
}
.no-comment-label {
  display: block;
  margin-top: 1rem;
}
.card-content-container {
  padding: 0 1.5rem 0.5rem 1.5rem !important;

  .comments-container {
    max-height: 47vh;
    overflow-y: auto;
    padding-right: 10px;
    margin: 1em 0;

    .lr-comment {
      border: 1px solid #eceeef;
      border-radius: 8px;
      background-color: #fcfcfd;

      &:not(:last-child) {
        margin-bottom: 1em;
      }

      .comment-wrapper {
        padding: 1rem 1.2rem 0.5em;
      }

      .created-by {
        font-weight: bold;
      }

      .comment-timestamp {
        color: #c4c4c4;
      }
    }
  }
}
</style>
