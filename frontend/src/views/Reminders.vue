
<template>
    <div>
      <h2>Reminders</h2>
      <ul>
        <li v-for="reminder in reminders" :key="reminder.id">
          {{ reminder.name }} - Schedule: {{ reminder.schedule.recurrence }}
          <button @click="completeReminder(reminder.id)">Complete</button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
import { ref, reactive, onMounted} from 'vue';
  import axios from "axios";
  
  export default {
    name: "Reminders",
    setup() {
      const reminders = ref([]);
  
      async function completeReminder(reminderId) {
        try {
          await axios.post(
            `http://localhost:8000/users/1/reminders/${reminderId}/complete`
          );
          fetchReminders();
        } catch (error) {
          console.error("Failed to complete reminder:", error);
        }
      }
  
      async function fetchReminders() {
        try {
          const response = await axios.get("http://localhost:8000/users/1/reminders");
          reminders.value = response.data;
        } catch (error) {
          console.error("Failed to fetch reminders:", error);
        }
      }
  
      onMounted(() => {
        fetchReminders();
      });
  
      return {
        reminders,
        completeReminder,
      };
    },
  };
  </script>
  