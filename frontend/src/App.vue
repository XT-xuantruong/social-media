<script setup>
import { useUserStore } from "@/stores/user";
import axios from "axios";
import Toast from "@/components/Toast.vue";
import { RouterView } from "vue-router";
import Navbar from "@/components/Navbar.vue";

const userStore = useUserStore();

userStore.initStore();

const token = userStore.user.access;

if (token) {
  axios.defaults.headers.common["Authorization"] = "Bearer " + token;
} else {
  axios.defaults.headers.common["Authorization"] = "";
}
</script>

<template>
  <Navbar />
  <main class="px-8 py-6 bg-gray-100">
    <RouterView />
  </main>
</template>
