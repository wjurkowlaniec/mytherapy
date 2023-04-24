<template>
    <div>
      <h2>Add Reminder</h2>
      <!-- Add reminder form will go here -->
      <form @submit.prevent="addReminder">
        <label for="name">Reminder Name:</label>
        <input type="text" id="name" v-model="name" required>
        <button type="submit">Add Reminder</button>
      </form>
    </div>
  </template>
  
  <script>
import { ref, reactive } from 'vue';
  import axios from "axios";
  
  export default {
    name: "AddReminder",
    setup() {
      const name = ref("");
  
      async function addReminder() {
        try {
          await axios.post("http://localhost:8000/users/1/reminders", {
            name: name.value,
          });
          name.value = "";
        } catch (error) {
          console.error("Failed to add reminder:", error);
        }
      }
  
      return {
        name,
        addReminder,
      };
    },
  };
  </script>
  