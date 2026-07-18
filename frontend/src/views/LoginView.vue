<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import { apiFetch } from "../api";

const username = ref("");
const isLoading = ref(false);
const errorMsg = ref("");

const router = useRouter();
const userStore = useUserStore();

async function login() {
  if (!username.value.trim()) return;
  isLoading.value = true;
  errorMsg.value = "";
  try {
    const user = await apiFetch("/login", {
      method: "POST",
      body: JSON.stringify({ username: username.value }),
    });
    userStore.login(user.id, user.username);
    router.push("/");
  } catch (err: any) {
    errorMsg.value = err.message || "Ett fel uppstod";
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-xl shadow-lg p-8 w-full max-w-sm">
      <h1 class="text-3xl font-bold text-center text-blue-600 mb-6">
        TodoMyrberg
      </h1>
      <form class="space-y-4" @submit.prevent="login">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Användarnamn</label
          >
          <input
            v-model="username"
            type="text"
            placeholder="Skriv ditt namn..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:outline-none"
            required
          />
        </div>
        <p v-if="errorMsg" class="text-red-500 text-sm">
          {{ errorMsg }}
        </p>
        <button
          type="submit"
          :disabled="isLoading || !username.trim()"
          class="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
        >
          {{ isLoading ? "Loggar in..." : "Logga in" }}
        </button>
      </form>
    </div>
  </div>
</template>
