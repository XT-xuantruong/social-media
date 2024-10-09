<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="notification in notifications"
        v-bind:key="notification.id"
        v-if="notifications.length"
      >
        {{ notification.body }}
        <button class="underline" @click="readNotification(notification)">
          Read more
        </button>
      </div>
      <div class="p-4 bg-white border border-gray-200 rounded-lg" v-else>
        You don't have any unread notifications!
      </div>
    </div>
  </div>
</template>
<script setup>
import router from "@/router";
import notificationServices from "@/services/notificationServices";
import { useUserStore } from "@/stores/user";
import axios from "axios";
import { onBeforeMount, onMounted, ref, watch } from "vue";
const notifications = ref([]);
const userStore = useUserStore();

const getNotifications = () => {
  notificationServices
    .gets()
    .then((response) => {
      console.log(response.data);

      notifications.value = response.data;
    })
    .catch((error) => {
      console.log("Error: ", error);
    });
};
onMounted(() => {
  getNotifications();
});
watch(
  () => userStore.user.id,
  () => {
    getNotifications();
  }
);

const readNotification = (notification) => {
  console.log("readNotification", notification.id);
  notificationServices
    .setRead(notification)
    .then((response) => {
      console.log(response.data);
      if (
        notification.type_of_notification == "post_like" ||
        notification.type_of_notification == "post_comment"
      ) {
        router.push({
          name: "postview",
          params: { id: notification.post_id },
        });
      } else {
        router.push({
          name: "friends",
          params: { id: notification.created_for_id },
        });
      }
    })
    .catch((error) => {
      console.log("Error: ", error);
    });
};
</script>
