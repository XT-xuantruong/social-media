<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <div class="space-y-4">
          <div
            class="flex items-center justify-between"
            v-for="conversation in conversations"
            v-bind:key="conversation.id"
            v-on:click="setActiveConversation(conversation.id)"
          >
            <div class="flex items-center space-x-2">
              <template v-for="user in conversation.users" v-bind:key="user.id">
                <template v-if="user.id !== userStore.user.id">
                  <img
                    :src="user.avatar"
                    class="w-[40px] h-[40px] rounded-full"
                  />

                  <p class="text-xs font-bold">
                    {{ user.name }}
                  </p>
                </template>
              </template>
            </div>

            <span class="text-xs text-gray-500"
              >{{ conversation.modified_at_formatted }} ago</span
            >
          </div>
        </div>
      </div>
    </div>

    <div class="main-center col-span-3 space-y-4">
      <div class="bg-white border border-gray-200 rounded-lg">
        <div class="flex flex-col flex-grow p-4">
          <template
            v-for="message in activeConversation.messages"
            v-bind:key="message.id"
          >
            <div
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div>
                <div
                  class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg"
                >
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formatted }} ago</span
                >
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.avatar"
                  class="w-[40px] h-[40px] rounded-full"
                />
              </div>
            </div>

            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.avatar"
                  class="w-[40px] h-[40px] rounded-full"
                />
              </div>
              <div>
                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                  <p class="text-sm">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-500 leading-none"
                  >{{ message.created_at_formatted }} ago</span
                >
              </div>
            </div>
          </template>
        </div>
      </div>

      <div class="bg-white border border-gray-200 rounded-lg">
        <form v-on:submit.prevent="submitForm">
          <div class="p-4">
            <textarea
              v-model="body"
              class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What do you want to say?"
            ></textarea>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            <button
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useUserStore } from "@/stores/user";
import { onMounted, ref } from "vue";
import chatServices from "@/services/chatServices";

const userStore = useUserStore();

const conversations = ref([]);
const activeConversation = ref({});
const body = ref("");

const getConversations = () => {
  chatServices
    .gets()
    .then((response) => {
      // console.log(response.data);

      conversations.value = response.data;

      if (conversations.value.length) {
        activeConversation.value = conversations.value[0].id;
      }

      getMessages();
    })
    .catch((error) => {
      console.log(error);
    });
};

const setActiveConversation = (id) => {
  console.log("setActiveConversation", id);

  activeConversation.value = id;
  getMessages();
};

const getMessages = () => {
  chatServices
    .get(activeConversation.value)
    .then((response) => {
      console.log("long", response.data);

      activeConversation.value = response.data;
    })
    .catch((error) => {
      console.log(error);
    });
};

const submitForm = () => {
  console.log("submitForm", body);

  chatServices
    .sendMessages(activeConversation.value.id, body.value)
    .then((response) => {
      // console.log(response.data);

      activeConversation.value.messages.push(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
};

onMounted(() => getConversations());
</script>
