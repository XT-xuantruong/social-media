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

const getFeed = () => {
  postServices
    .getProfileFeed(route.params.id)
    .then((response) => {
      posts.value = response.data.posts;
      user.value = response.data.user;
    })
    .catch((error) => {
      console.log("error", error);
    });
};
const submitForm = () => {
  console.log("show ra", body.value);

  postServices
    .create({ body: body.value })
    .then((response) => {
      console.log("data", response.data);

      posts.value.unshift(response.data);
      body.value = "";
    })
    .catch((error) => {
      console.log("error", error);
    });
};

const sendFriendshipRequest = () => {
  oauthServices
    .sendFriendshipRequest(route.params.id)
    .then((response) => {
      console.log("data", response.data);

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
      console.log(response.data);
      router.push("/messages");
    })
    .catch((error) => {
      console.log("error", error);
    });
};

onMounted(() => getFeed());

  watch(
    () => route.params.id,
    () => getFeed()
  )
</script>
<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full" />

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
            v-if="userStore.user.id !== user.id"
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
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <a
              href="#"
              class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg"
              >Attach image</a
            >

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
        <FeedItem v-bind:post="post" />
      </div>
    </div>

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />

      <Trends />
    </div>
  </div>
</template>
