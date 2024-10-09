<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
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
import { onMounted, ref } from "vue";
import postServices from "@/services/postServices";

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
      console.log("11111111", posts);

      body.value = "";
      file.value = null;
      url.value = null;
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
