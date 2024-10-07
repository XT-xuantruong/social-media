<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Edit profile</h1>
        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit
          mate. Lorem ipsum dolor sit mate.
        </p>
      </div>
    </div>
    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Name</label><br />
            <input
              type="text"
              v-model="form.name"
              placeholder="Your full name"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label>E-mail</label><br />
            <input
              type="email"
              v-model="form.email"
              placeholder="Your e-mail address"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>
          <div>
            <label>Avatar</label><br />
            <input type="file" ref="file" />
          </div>
          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>
          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
              Save changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";
import { ref } from "vue";
import oauthServices from "@/services/oauthServices";
import { useRouter } from "vue-router";

const router = useRouter();
const toastStore = useToastStore();
const userStore = useUserStore();
const form = ref({
  email: userStore.user.email,
  name: userStore.user.name,
});
const errors = ref([]);
const file = ref(null);

const submitForm = () => {
  errors.value = [];
  if (form.value.email === "") {
    errors.value.push("Your e-mail is missing");
  }
  if (form.value.name === "") {
    errors.value.push("Your name is missing");
  }
  if (errors.value.length === 0) {
    let formData = new FormData();
    formData.append("avatar", file.value.files[0]);
    formData.append("name", form.value.name);
    formData.append("email", form.value.email);
    oauthServices
      .updateProfile(formData)
      .then((response) => {
        if (response.data.message === "information updated") {
          // toastStore.showToast(
          //   5000,
          //   "The information was saved",
          //   "bg-emerald-500"
          // );
          userStore.setUserInfo({
            id: userStore.user.id,
            name: form.value.name,
            email: form.value.email,
            avatar: response.data.data,
          });
          router.back();
        } else {
          // toastStore.showToast(
          //   5000,
          //   `${response.data.message}. Please try again`,
          //   "bg-red-300"
          // );
        }
      })
      .catch((error) => {
        console.log("error", error);
      });
  }
};
</script>
