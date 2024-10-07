<template>
  <div class="mb-6 flex items-center justify-between">
    <div class="flex items-center space-x-6">
      <img
        :src="props.comment.created_by.avatar"
        class="w-[40px] h-[40px] rounded-full"
      />

      <p>
        <strong>
          <RouterLink
            :to="{
              name: 'profile',
              params: { id: props.comment.created_by.id },
            }"
            >{{ props.comment.created_by.name }}</RouterLink
          >
        </strong>
      </p>
    </div>
    <p class="text-gray-600">{{ props.comment.created_at_formatted }} ago</p>
  </div>
  <p>{{ props.comment.body }}</p>
</template>
<script setup>
import { defineProps } from "vue";
const props = defineProps({
  comment: Object,
});
</script>
