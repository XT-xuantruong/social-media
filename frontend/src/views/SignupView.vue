<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Sign up</h1>

        <p class="mb-6 text-gray-500">
          Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum
          dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit
          mate. Lorem ipsum dolor sit mate.
        </p>

        <p class="font-bold">
          Already have an account?
          <RouterLink :to="{ name: 'login' }" class="underline"
            >Click here</RouterLink
          >
          to log in!
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
            <label>Password</label><br />
            <input
              type="password"
              v-model="form.password1"
              placeholder="Your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <div>
            <label>Repeat password</label><br />
            <input
              type="password"
              v-model="form.password2"
              placeholder="Repeat your password"
              class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg"
            />
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>
          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">
              Sign up
            </button>
          </div>
        </form>

        <div
          class="bg-green-300 text-white rounded-lg p-6 mt-2"
          :class="toastStore.classes"
          v-if="toastStore.isVisible"
        >
          {{ toastStore.message }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useToastStore } from "@/stores/toast";
import oauthServices from "@/services/oauthServices";
import { ref } from "vue";
import { useRouter } from "vue-router";

const toastStore = useToastStore();
const form = ref({ email: "", name: "", password1: "", password2: "" });
const errors = ref([]);
const router = useRouter();

const submitForm = () => {
  errors.value = [];
  if (form.value.email === "") {
    errors.value.push("Your e-mail is missing");
  }

  if (form.value.name === "") {
    errors.value.push("Your name is missing");
  }

  if (form.value.password1 === "") {
    errors.value.push("Your password is missing");
  }

  if (form.value.password1 !== form.value.password2) {
    errors.value.push("The password does not match");
  }

  if (errors.value.length === 0) {
    oauthServices
      .signup(form.value)
      .then((response) => {
        if (response.data.message === "success") {
          toastStore.showToast(
            5000,
            "The user is registered. Please activate your account by clicking your email link.",
            "bg-emerald-500"
          );

          form.value.email = "";
          form.value.name = "";
          form.value.password1 = "";
          form.value.password2 = "";
        } else {
          const data = JSON.parse(response.data.message);
          for (const key in data) {
            errors.value.push(data[key][0].message);
          }

          toastStore.showToast(
            5000,
            "Something went wrong. Please try again",
            "bg-red-300"
          );
        }
      })
      .catch((error) => {
        console.log("error", error);
      });
  }
};
</script>
