<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { apiFetch } from "../api";

const router = useRouter();
const route = useRoute();

const isEdit = route.name === "edit";
const taskId = route.params.id;

const users = ref<any[]>([]);
const isLoading = ref(true);

const form = ref({
  title: "",
  details: "",
  emoji: "📝",
  user_id: "",
  due_date: new Date().toISOString().split("T")[0],
  is_recurring: false,
  interval_value: 1,
  interval_type: "days",
  specific_day: null as number | null,
});

const emojis = [
  "🧹",
  "🧼",
  "🧽",
  "🗑️",
  "🚽",
  "🍽️",
  "🍳",
  "🛒",
  "📄",
  "🚗",
  "🪴",
  "🐶",
  "👕",
  "💰",
  "📅",
  "📝",
];

onMounted(async () => {
  try {
    users.value = await apiFetch("/users");

    if (isEdit) {
      const allTasks = await apiFetch("/tasks");
      const task = allTasks.find((t: any) => t.id === Number(taskId));
      if (task) {
        form.value = {
          title: task.title,
          details: task.details || "",
          emoji: task.emoji || "📝",
          user_id: task.user_id,
          due_date: task.due_date.split("T")[0],
          is_recurring: task.is_recurring,
          interval_value: task.interval_value || 1,
          interval_type: task.interval_type || "days",
          specific_day: task.specific_day,
        };
      }
    } else {
      if (users.value.length > 0) {
        form.value.user_id = users.value[0].id;
      }
    }
  } catch (err) {
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});

async function saveTask() {
  const payload = {
    ...form.value,
    user_id: Number(form.value.user_id),
    specific_day:
      form.value.specific_day !== null &&
      form.value.specific_day !== ("" as any)
        ? Number(form.value.specific_day)
        : null,
  };

  try {
    if (isEdit) {
      await apiFetch(`/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify(payload),
      });
    } else {
      await apiFetch("/tasks", {
        method: "POST",
        body: JSON.stringify(payload),
      });
    }
    router.back();
  } catch (err) {
    console.error(err);
    alert("Kunde inte spara uppgiften");
  }
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header
      class="bg-blue-600 text-white p-4 flex items-center shadow-md sticky top-0 z-10"
    >
      <button
        class="p-2 mr-4 hover:bg-blue-700 rounded-full"
        @click="router.back()"
      >
        <font-awesome-icon icon="arrow-left" />
      </button>
      <h1 class="text-xl font-bold flex-1">
        {{ isEdit ? "Redigera Uppgift" : "Ny Uppgift" }}
      </h1>
    </header>

    <main class="p-4 max-w-lg mx-auto">
      <div v-if="isLoading" class="text-center py-10">Laddar...</div>
      <form
        v-else
        class="bg-white rounded-xl shadow p-6 space-y-4"
        @submit.prevent="saveTask"
      >
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Emoji</label
          >
          <div class="flex flex-wrap gap-2">
            <button
              v-for="e in emojis"
              :key="e"
              type="button"
              :class="{ 'bg-blue-100 ring-2 ring-blue-500': form.emoji === e }"
              class="text-2xl p-2 rounded hover:bg-gray-100 transition"
              @click="form.emoji = e"
            >
              {{ e }}
            </button>
            <input
              v-model="form.emoji"
              type="text"
              class="w-14 text-center text-xl border rounded focus:ring-2 focus:ring-blue-500 ml-2"
              maxlength="2"
              title="Egen emoji"
              placeholder="📝"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Titel</label
          >
          <input
            v-model="form.title"
            type="text"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="Ex: Städa badrum"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Detaljer (Frivilligt)</label
          >
          <textarea
            v-model="form.details"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"
            rows="3"
            placeholder="Anteckningar eller specifika instruktioner..."
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Tilldelad Användare</label
          >
          <select
            v-model="form.user_id"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option v-for="u in users" :key="u.id" :value="u.id">
              {{ u.username }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1"
            >Datum / Nästa tillfälle</label
          >
          <input
            v-model="form.due_date"
            type="date"
            required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div class="border-t pt-4">
          <label class="flex items-center gap-2 cursor-pointer">
            <input
              v-model="form.is_recurring"
              type="checkbox"
              class="w-5 h-5 text-blue-600 rounded focus:ring-blue-500"
            />
            <span class="font-medium text-gray-800">Återkommande uppgift</span>
          </label>
        </div>

        <div
          v-if="form.is_recurring"
          class="space-y-4 bg-gray-50 p-4 rounded-lg"
        >
          <div class="flex gap-4">
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Intervall</label
              >
              <input
                v-model.number="form.interval_value"
                type="number"
                min="1"
                required
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="flex-2">
              <label class="block text-sm font-medium text-gray-700 mb-1"
                >Typ</label
              >
              <select
                v-model="form.interval_type"
                class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="days">Dagar</option>
                <option value="weeks">Veckor</option>
                <option value="months">Månader</option>
                <option value="years">År</option>
              </select>
            </div>
          </div>

          <div v-if="form.interval_type === 'weeks'">
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Specifik veckodag (frivilligt)</label
            >
            <select
              v-model="form.specific_day"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option :value="null">Ingen specifik dag</option>
              <option :value="0">Måndag</option>
              <option :value="1">Tisdag</option>
              <option :value="2">Onsdag</option>
              <option :value="3">Torsdag</option>
              <option :value="4">Fredag</option>
              <option :value="5">Lördag</option>
              <option :value="6">Söndag</option>
            </select>
          </div>

          <div v-if="form.interval_type === 'months'">
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Specifik dag i månaden (1-31, frivilligt)</label
            >
            <input
              v-model.number="form.specific_day"
              type="number"
              min="1"
              max="31"
              class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder="Lämna tomt för ingen specifik"
            />
          </div>
        </div>

        <div class="pt-4">
          <button
            type="submit"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg transition"
          >
            {{ isEdit ? "Spara Ändringar" : "Lägg Till Uppgift" }}
          </button>
        </div>
      </form>
    </main>
  </div>
</template>
