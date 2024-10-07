<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h2 class="text-xl">Trend: #{{ $route.params.id }}</h2>
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

<script setup>
import axios from "axios";
import PeopleYouMayKnow from "../components/PeopleYouMayKnow.vue";
import Trends from "../components/Trends.vue";
import FeedItem from "../components/FeedItem.vue";
import { onMounted, ref, watch } from "vue";
import postServices from "@/services/postServices";
import { useRoute } from "vue-router";

const posts = ref([]);
const route = useRoute();

const getFeed = () => {
  postServices
    .getTrend(route.params.id)
    .then((response) => {
      console.log("data", response.data);

      posts.value = response.data;
    })
    .catch((error) => {
      console.log("error", error);
    });
};

onMounted(() => getFeed());

watch(
  () => route.params.id,
  () => getFeed()
);
</script>
