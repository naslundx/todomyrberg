<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { apiFetch } from "../api";

const router = useRouter();
const tasks = ref<any[]>([]);
const users = ref<any[]>([]);
const isLoading = ref(true);

onMounted(() => {
  loadData();
});

async function loadData() {
  isLoading.value = true;
  try {
    const [tasksData, usersData] = await Promise.all([
      apiFetch("/tasks"),
      apiFetch("/users"),
    ]);
    tasks.value = tasksData;
    users.value = usersData;
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
}

function getUserName(userId: number) {
  const user = users.value.find((u) => u.id === userId);
  return user ? user.username : "Okänd";
}

function formatDate(isoString: string) {
  return new Date(isoString).toLocaleDateString("sv-SE");
}

function formatInterval(value: number, type: string) {
  if (type === "days") return value === 1 ? "1 dag" : `${value} dagar`;
  if (type === "weeks") return value === 1 ? "1 vecka" : `${value} veckor`;
  if (type === "months") return value === 1 ? "1 månad" : `${value} månader`;
  if (type === "years") return value === 1 ? "1 år" : `${value} år`;
  return `${value} ${type}`;
}

async function markEarlyDone(taskId: number) {
  if (
    !confirm(
      "Är du säker på att du vill markera denna uppgift som tidigt klar?",
    )
  )
    return;
  try {
    await apiFetch(`/tasks/${taskId}/action`, {
      method: "POST",
      body: JSON.stringify({ action: "early_done" }),
    });
    loadData();
  } catch (err) {
    console.error(err);
  }
}

async function deleteTask(taskId: number) {
  if (!confirm("Är du säker på att du vill ta bort denna uppgift?")) return;
  try {
    await apiFetch(`/tasks/${taskId}`, { method: "DELETE" });
    loadData();
  } catch (err) {
    console.error(err);
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header
      class="bg-gray-800 text-white p-4 flex items-center shadow-md sticky top-0 z-10"
    >
      <button
        class="p-2 mr-4 hover:bg-gray-700 rounded-full"
        @click="router.push('/')"
      >
        <font-awesome-icon icon="arrow-left" />
      </button>
      <h1 class="text-xl font-bold flex-1">Admin</h1>
    </header>

    <main class="p-4 max-w-2xl mx-auto">
      <div v-if="isLoading" class="text-center py-10 text-gray-500">
        Laddar...
      </div>
      <div v-else class="space-y-4">
        <div
          v-for="task in tasks"
          :key="task.id"
          class="bg-white rounded-xl shadow p-4 border border-gray-200"
        >
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-lg font-semibold flex items-center gap-2">
              <span v-if="task.emoji">{{ task.emoji }}</span>
              {{ task.title }}
            </h3>
            <span
              :class="
                task.status === 'done'
                  ? 'bg-green-100 text-green-800'
                  : 'bg-yellow-100 text-yellow-800'
              "
              class="text-xs font-medium px-2.5 py-0.5 rounded"
            >
              {{ task.status === "done" ? "Klar" : "Väntar" }}
            </span>
          </div>

          <div
            v-if="task.details"
            class="text-sm text-gray-500 mb-3 p-2 bg-gray-50 rounded italic"
          >
            {{ task.details }}
          </div>

          <div class="text-sm text-gray-600 mb-4 grid grid-cols-2 gap-2">
            <div>
              <strong>Användare:</strong> {{ getUserName(task.user_id) }}
            </div>
            <div>
              <strong>Nästa tillfälle:</strong> {{ formatDate(task.due_date) }}
            </div>
            <div v-if="task.is_recurring" class="col-span-2">
              <strong>Intervall:</strong>
              {{ formatInterval(task.interval_value, task.interval_type) }}
              <span v-if="task.specific_day !== null"
                >(Dag: {{ task.specific_day }})</span
              >
            </div>
            <div v-else class="col-span-2">
              <strong>Engångsuppgift</strong>
            </div>
          </div>

          <div class="flex flex-wrap gap-2 pt-2 border-t border-gray-100">
            <button
              v-if="task.is_recurring"
              class="text-sm bg-blue-50 text-blue-600 hover:bg-blue-100 py-1.5 px-3 rounded-lg flex items-center gap-1"
              @click="markEarlyDone(task.id)"
            >
              <font-awesome-icon icon="check" /> Tidigt klar
            </button>
            <button
              class="text-sm bg-gray-50 text-gray-600 hover:bg-gray-100 py-1.5 px-3 rounded-lg flex items-center gap-1"
              @click="router.push(`/edit/${task.id}`)"
            >
              <font-awesome-icon icon="edit" /> Redigera
            </button>
            <button
              class="text-sm bg-red-50 text-red-600 hover:bg-red-100 py-1.5 px-3 rounded-lg flex items-center gap-1 ml-auto"
              @click="deleteTask(task.id)"
            >
              <font-awesome-icon icon="trash" /> Ta bort
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
