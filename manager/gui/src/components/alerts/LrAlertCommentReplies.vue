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
  <div>
    <span
      class="expand-collapse"
      v-if="replies && replies.length > 0"
      @click="isRepliesVisible = !isRepliesVisible"
      >{{ isRepliesVisible ? "Hide replies" : "Show replies" }}</span
    >

    <ul
      class="comment-replies-container"
      v-if="isRepliesVisible && replies && replies.length > 0"
    >
      <li
        class="comment-reply"
        v-for="reply in replies"
        :key="reply.comment_id"
      >
        <div class="created-by">
          {{ reply.created_by }}
        </div>
        <div class="comment-timestamp">
          {{ formatCommentTime(reply.created_time) }}
        </div>
        <div class="comment-text mt-1">
          {{ reply.comment_text }}
        </div>
      </li>
    </ul>
    <div class="add-reply">
      <v-text-field
        outlined
        dense
        class="mt-2"
        name="reply"
        placeholder="Reply"
        height="40"
        hide-details="auto"
        append-icon="mdi-send-circle"
        @click:append="replyToComment($event)"
        @keyup.enter="replyToComment($event)"
      ></v-text-field>
    </div>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Prop, PropSync } from "vue-property-decorator";
import { Api } from "../../services/Api";
import { formatCommentTime } from "@/utils/CommonUtilFunctions";
import { IAlertComment } from "./LrAlertComment.model";

@Component({
  name: "LrAlertCommentReplies",
  components: {},
})
export default class LrAlertCommentReplies extends Vue {
  isRepliesVisible = false;
  @Prop({ required: true }) private comment_id: string;
  @Prop({ required: true }) private replies: IAlertComment[];

  formatCommentTime(time: number) {
    return formatCommentTime(time);
  }

  replyToComment(event: any) {
    //Make the API call to reply to the comment.
  }
}
</script>
<style lang="scss" scoped>
.expand-collapse {
  cursor: pointer;
  font-weight: bold;
  font-size: 0.8rem;
  margin-bottom: 20px;
  padding: 0 1.2em;
  color: $primary;
  text-decoration: underline;
}
.created-by {
  font-weight: bold;
}

.comment-timestamp {
  color: #c4c4c4;
}

.comment-replies-container {
  padding: 0 1em 0.5em 3em;

  .comment-reply {
    padding: 0.5em 0;
    &:not(:last-child) {
      border-bottom: 1px solid #eceeef;
    }
  }
}
.add-reply {
  padding: 0.5em 1em 1em;
}
</style>
