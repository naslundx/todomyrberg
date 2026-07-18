import { ref, watch } from "vue";
import { defineStore } from "pinia";

export const useUserStore = defineStore("user", () => {
  const savedId = localStorage.getItem("user_id");
  const savedUsername = localStorage.getItem("username");

  const id = ref<number | null>(savedId ? Number(savedId) : null);
  const username = ref<string>(savedUsername || "");

  function login(userId: number, name: string) {
    id.value = userId;
    username.value = name;
  }

  function logout() {
    id.value = null;
    username.value = "";
  }

  watch(id, (newId) => {
    if (newId !== null) {
      localStorage.setItem("user_id", String(newId));
    } else {
      localStorage.removeItem("user_id");
    }
  });

  watch(username, (newUsername) => {
    if (newUsername) {
      localStorage.setItem("username", newUsername);
    } else {
      localStorage.removeItem("username");
    }
  });

  return { id, username, login, logout };
});
