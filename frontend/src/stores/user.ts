import { ref } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => {
  const id = ref<number | null>(null);
  const username = ref<string>("");

  function login(userId: number, name: string) {
    id.value = userId;
    username.value = name;
  }

  function logout() {
    id.value = null;
    username.value = "";
  }

  return { id, username, login, logout };
});
