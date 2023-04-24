<template>
    <div>
      <h2>Reminder History</h2>
      <!-- Reminder history list will go here -->
      <ul>
        <li v-for="entry in reminderHistory" :key="entry.id">
          {{ entry.reminder.name }} - Completed at: {{ entry.date_completed }}
        </li>
      </ul>
    </div>
  </template>
  
  <script>
import { ref, reactive } from 'vue';
  import axios from "axios";
  
  export default {
    name: "ReminderHistory",
    setup() {
      const reminderHistory = ref([]);
  
      async function fetchReminderHistory() {
        try {
          const response = await axios.get("http://localhost:8000/users/1/reminder-history");
          reminderHistory.value = response.data;
        } catch (error) {
          console.error("Failed to fetch reminder history:", error);
        }
      }
  
      onMounted(() => {
        fetchReminderHistory();
      });
  
      return {
        reminderHistory,
      };
    },
  };
  </script>
  