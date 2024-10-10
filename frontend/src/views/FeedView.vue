<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <FeedForm v-bind:user="userStore" v-bind:posts="posts" />

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

<script setup>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/FeedItem.vue";
import { onMounted, ref } from "vue";
import postServices from "@/services/postServices";
import FeedForm from "@/components/FeedForm.vue";

const posts = ref([]);
const body = ref("");
const url = ref(null);
const file = ref(null);
const getFeed = () => {
  postServices
    .gets()
    .then((response) => {
      posts.value = response.data;
    })
    .catch((error) => {
      console.log("error", error);
    });
};

onMounted(() => getFeed());

const deletePost = (id) => {
  posts.value = posts.value.filter((post) => post.id !== id);
};
</script>

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
