<script setup>
import axios from "axios";
import { useRouter } from "vue-router"; // Sử dụng để điều hướng trong Composition API
import { useUserStore } from "@/stores/user";
import { reactive, ref } from "vue";
import oauthServices from "@/services/oauthServices";

const userStore = useUserStore();
const router = useRouter();

const form = reactive({
  email: "",
  password: "",
});

const errors = ref([]);

const submitForm = async () => {
  errors.value = [];

  if (form.email === "") {
    errors.value.push("Your e-mail is missing");
  }

  if (form.password === "") {
    errors.value.push("Your password is missing");
  }

  if (errors.value.length === 0) {
    try {
      const loginResponse = await oauthServices.login(form);

      // Lưu token
      userStore.setToken(loginResponse.data);

      // Lấy thông tin người dùng sau khi đăng nhập thành công

      const userResponse = await oauthServices.getme(loginResponse.data.access);

      // Lưu thông tin người dùng
      userStore.setUserInfo(userResponse.data);

      // Điều hướng đến trang /feed
      router.push("/feed");
    } catch (error) {
      errors.value.push(
        "The email or password is incorrect! Or the user is not activated!"
      );
    }
  }
};
</script>

<template>
  <div>
    <form @submit.prevent="submitForm">
      <div>
        <label>Email</label>
        <input
          v-model="form.email"
          type="email"
          placeholder="Enter your email"
        />
      </div>
      <div>
        <label>Password</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="Enter your password"
        />
      </div>

      <template v-if="errors.length > 0">
        <div class="bg-red-300 text-white rounded-lg p-6">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>
      </template>

      <button type="submit">Login</button>
    </form>
  </div>
</template>
