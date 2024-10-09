<script setup>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/FeedItem.vue";
import { useUserStore } from "@/stores/user";
import { onBeforeMount, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import postServices from "@/services/postServices";
import oauthServices from "@/services/oauthServices";
import chatServices from "@/services/chatServices";

const userStore = useUserStore();
const route = useRoute();
const router = useRouter();

const posts = ref([]);
const user = ref({});
const body = ref("");
const can_send_friendship_request = ref(null);

const url = ref(null);
const file = ref(null);
const getFeed = () => {
  postServices
    .getProfileFeed(route.params.id)
    .then((response) => {
      posts.value = response.data.posts;
      user.value = response.data.user;
      can_send_friendship_request = response.data.can_send_friendship_request;

      console.log("long", user);
    })
    .catch((error) => {
      console.log("error", error);
    });
};
const submitForm = () => {
  let formData = new FormData();
  if (file.value && file.value.files.length > 0) {
    formData.append("attachments", file.value.files[0]);
  }
  formData.append("body", body.value);
  postServices
    .create(formData)
    .then((response) => {
      posts.value.unshift(response.data.data);
      body.value = "";
      file.value = null;
      url.value = null;
    })
    .catch((error) => {
      console.log("error", error);
    });
};

const sendFriendshipRequest = () => {
  oauthServices
    .sendFriendshipRequest(route.params.id)
    .then((response) => {
      can_send_friendship_request = false;
      if (response.data.message == "request already sent") {
        this.toastStore.showToast(
          5000,
          "The request has already been sent!",
          "bg-red-300"
        );
      } else {
        this.toastStore.showToast(
          5000,
          "The request was sent!",
          "bg-emerald-300"
        );
      }
    })
    .catch((error) => {
      console.log("error", error);
    });
};

const sendDirectMessage = () => {
  chatServices
    .getChat(route.params.id)
    .then((response) => {
      router.push("/messages");
    })
    .catch((error) => {
      console.log("error", error);
    });
};
const onFileChange = (e) => {
  const file = e.target.files[0];
  url.value = URL.createObjectURL(file);
};
onMounted(() => getFeed());

watch(
  () => route.params.id,
  () => getFeed()
);

const deletePost = (id) => {
  posts.value = posts.value.filter((post) => post.id !== id);
};
</script>
<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <img :src="user.avatar" class="mb-6 rounded-full" />

        <p>
          <strong>{{ user.name }}</strong>
        </p>

        <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
          <RouterLink
            :to="{ name: 'friends', params: { id: user.id } }"
            class="text-xs text-gray-500"
            >{{ user.friends_count }} friends</RouterLink
          >
          <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
        </div>

        <div class="mt-6">
          <button
            class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendFriendshipRequest"
            v-if="userStore.user.id !== user.id && can_send_friendship_request"
          >
            Send friendship request
          </button>
          <button
            class="inline-block mt-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
            @click="sendDirectMessage"
            v-if="userStore.user.id !== user.id"
          >
            Send direct message
          </button>
          <RouterLink
            class="inline-block mr-2 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg"
            to="/profile/edit"
            v-if="userStore.user.id === user.id"
          >
            Edit profile
          </RouterLink>
        </div>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <div
        class="bg-white border border-gray-200 rounded-lg"
        v-if="userStore.user.id === user.id"
      >
        <form v-on:submit.prevent="submitForm" method="post">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What are you thinking about?"
            ></textarea>

            <div id="preview" v-if="url">
              <img :src="url" class="w-[100px] mt-3 rounded-xl" />
            </div>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <label
              class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"
            >
              <input type="file" ref="file" @change="onFileChange" />
              Attach image
            </label>
            <button
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
            >
              Post
            </button>
          </div>
        </form>
      </div>

      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" v-on:deletePost="deletePost" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />

      <Trends />
    </div>
  </div>
</template>

<style scoped>
input[type="file"] {
  display: none;
}
.custom-file-upload {
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
}
</style>
