<template>
  <form v-on:submit.prevent="submitForm" method="post">
    <div class="p-4">
      <textarea
        v-model="body"
        class="p-4 w-full bg-gray-100 rounded-lg"
        placeholder="What are you thinking about?"
      ></textarea>
      <label> <input type="checkbox" v-model="is_private" /> Private </label>
      <div id="preview" v-if="url">
        <img :src="url" class="w-[100px] mt-3 rounded-xl" />
      </div>
    </div>

    <div class="p-4 border-t border-gray-100 flex justify-between">
      <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
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
</template>

<script setup>
import postServices from "@/services/postServices";
import { ref, toRef } from "vue";
const props = defineProps({
  user: Object,
  posts: Array,
});

const posts = toRef(props, 'posts');

const body = ref("");
const url = ref(null);
const file = ref(null);
const is_private = ref(false);

const submitForm = () => {
  let formData = new FormData();
  if (file.value && file.value.files.length > 0) {
    formData.append("attachments", file.value.files[0]);
  }
  formData.append("body", body.value);
  formData.append('is_private', is_private.value)
  console.log("hay", is_private.value);
  
  postServices
    .create(formData)
    .then((response) => {
      posts.value.unshift(response.data.data);
      body.value = "";
      file.value = null;
      url.value = null;
      is_private.value = false

      if (props.user) {
        props.user.posts_count += 1;
      }
    })
    .catch((error) => {
      console.log("error", error);
    });
};

const onFileChange = (e) => {
  const file = e.target.files[0];
  url.value = URL.createObjectURL(file);
};
</script>
