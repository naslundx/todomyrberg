<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";
import { apiFetch } from "../api";

const router = useRouter();
const userStore = useUserStore();

const tasks = ref<any[]>([]);
const isLoading = ref(true);

onMounted(() => {
  if (!userStore.id) {
    router.push("/login");
    return;
  }
  loadTasks();
});

async function loadTasks() {
  isLoading.value = true;
  try {
    tasks.value = await apiFetch(`/tasks?user_id=${userStore.id}`);
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

async function markAction(task: any, action: "done" | "snooze") {
  try {
    await apiFetch(`/tasks/${task.id}/action`, {
      method: "POST",
      body: JSON.stringify({ action, details: task.details }),
    });
    loadTasks();
  } catch (err) {
    console.error(err);
  }
}

function formatInterval(value: number, type: string) {
  if (type === "days") return value === 1 ? "1 dag" : `${value} dagar`;
  if (type === "weeks") return value === 1 ? "1 vecka" : `${value} veckor`;
  if (type === "months") return value === 1 ? "1 månad" : `${value} månader`;
  if (type === "years") return value === 1 ? "1 år" : `${value} år`;
  return `${value} ${type}`;
}

function logout() {
  userStore.logout();
  router.push("/login");
}
</script>

<template>
  <div class="min-h-screen pb-20">
    <header
      class="bg-blue-600 text-white p-4 flex justify-between items-center shadow-md sticky top-0 z-10"
    >
      <div>
        <h1 class="text-xl font-bold">Hej, {{ userStore.username }}!</h1>
        <p class="text-blue-100 text-sm">Dina uppgifter för idag</p>
      </div>
      <div class="flex gap-4">
        <button
          class="p-2 hover:bg-blue-700 rounded-full"
          title="Admin"
          @click="router.push('/admin')"
        >
          <font-awesome-icon icon="cog" />
        </button>
        <button
          class="p-2 hover:bg-blue-700 rounded-full"
          title="Logga ut"
          @click="logout"
        >
          <font-awesome-icon icon="sign-out-alt" />
        </button>
      </div>
    </header>

    <main class="p-4 max-w-lg mx-auto">
      <div v-if="isLoading" class="text-center py-10 text-gray-500">
        Laddar uppgifter...
      </div>
      <div v-else-if="tasks.length === 0" class="text-center py-10">
        <font-awesome-icon
          icon="check-circle"
          class="text-6xl text-green-400 mb-4"
        />
        <h2 class="text-2xl font-semibold text-gray-700">Allt är klart!</h2>
        <p class="text-gray-500 mt-2">
          Bra jobbat, du har inga fler uppgifter idag.
        </p>
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="bg-white rounded-xl shadow p-4 border border-gray-100 flex flex-col gap-3"
        >
          <div>
            <h3
              class="text-lg font-semibold text-gray-800 flex items-center gap-2"
            >
              <span v-if="task.emoji">{{ task.emoji }}</span>
              {{ task.title }}
            </h3>
            <p v-if="task.is_recurring" class="text-xs text-gray-500 mt-1">
              <font-awesome-icon icon="rotate-right" class="mr-1" />
              Återkommande ({{
                formatInterval(task.interval_value, task.interval_type)
              }})
            </p>
          </div>

          <textarea
            v-model="task.details"
            class="w-full text-sm border border-gray-200 rounded-lg p-2 text-gray-700 bg-gray-50 focus:bg-white focus:ring-2 focus:ring-blue-200 focus:outline-none transition resize-y"
            rows="2"
            placeholder="Lägg till en valfri notering eller detalj..."
          />

          <div class="flex gap-2 mt-1">
            <button
              class="flex-1 bg-green-500 hover:bg-green-600 text-white font-medium py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition"
              @click="markAction(task, 'done')"
            >
              <font-awesome-icon icon="check" /> Klar
            </button>
            <button
              class="flex-1 bg-yellow-500 hover:bg-yellow-600 text-white font-medium py-2 px-4 rounded-lg flex items-center justify-center gap-2 transition"
              @click="markAction(task, 'snooze')"
            >
              <font-awesome-icon icon="clock" /> Snooza
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- Floating Action Button -->
    <button
      class="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-blue-700 transition transform hover:scale-105 z-20"
      @click="router.push('/add')"
    >
      <font-awesome-icon icon="plus" class="text-2xl" />
    </button>
  </div>
</template>
