import { createRouter, createWebHistory } from "vue-router";
import Reminders from "../views/Reminders.vue";
import AddReminder from "../views/AddReminder.vue";
import AddReminderGroup from "../views/AddReminderGroup.vue";
import ReminderHistory from "../views/ReminderHistory.vue";

const routes = [
  {
    path: "/",
    name: "Reminders",
    component: Reminders,
  },
  {
    path: "/add-reminder",
    name: "AddReminder",
    component: AddReminder,
  },
  {
    path: "/add-reminder-group",
    name: "AddReminderGroup",
    component: AddReminderGroup,
  },
  {
    path: "/reminder-history",
    name: "ReminderHistory",
    component: ReminderHistory,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
