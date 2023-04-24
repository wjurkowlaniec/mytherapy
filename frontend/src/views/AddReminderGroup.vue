<template>
    <div>
      <h2>Add Reminder Group</h2>
      <!-- Add reminder group form will go here -->
      <form @submit.prevent="addReminderGroup">
        <label for="name">Group Name:</label>
        <input type="text" id="name" v-model="name" required>
        <button type="submit">Add Reminder Group</button>
      </form>
    </div>
  </template>
  
  <script>
import { ref, reactive } from 'vue';
  import axios from "axios";
  
  export default {
    name: "AddReminderGroup",
    setup() {
      const name = ref("");
  
      async function addReminderGroup() {
        try {
          await axios.post("http://localhost:8000/users/1/reminder-groups", {
            name: name.value,
          });
          name.value = "";
        } catch (error) {
          console.error("Failed to add reminder group:", error);
        }
      }
  
      return {
        name,
        addReminderGroup,
      };
    },
  };
  </script>
  