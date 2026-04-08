<template>
  <div class="min-h-screen bg-gray-100">
    <nav
      class="sticky top-0 z-10 border-b border-gray-200 bg-white/95 backdrop-blur px-4 py-3 flex flex-wrap gap-2 items-center shadow-sm"
    >
      <span class="text-sm font-semibold text-gray-500 mr-2">Vista:</span>
      <button
        type="button"
        :class="tab === 'dash' ? tabActive : tabIdle"
        @click="tab = 'dash'"
      >
        Dashboard ejecutivo
      </button>
      <button
        type="button"
        :class="tab === 'eeff' ? tabActive : tabIdle"
        @click="tab = 'eeff'"
      >
        EEFF — acercamiento
      </button>
      <button
        type="button"
        :class="tab === 'eeff_excel' ? tabActive : tabIdle"
        @click="tab = 'eeff_excel'"
      >
        EEFF Excel + proyección
      </button>
      <button
        type="button"
        :class="tab === 'cmf' ? tabActive : tabIdle"
        @click="tab = 'cmf'"
      >
        CMF — proyección
      </button>

      <button
        type="button"
        :class="tab === 'eeff_eerr' ? tabActive : tabIdle"
        @click="tab = 'eeff_eerr'"
      >
        EERR — consolidado
      </button>

      <button
        type="button"
        :class="tab === 'balance_trib' ? tabActive : tabIdle"
        @click="tab = 'balance_trib'"
      >
        Balance Tributario
      </button>
      
      <button
        type="button"
        :class="tab === 'balance_ifrs' ? tabActive : tabIdle"
        @click="tab = 'balance_ifrs'"
      >
        Balance IFRS
      </button>

      <div
        class="w-px h-6 bg-gray-200 hidden sm:block mx-1"
        aria-hidden="true"
      />

      <label class="flex items-center gap-2 text-sm text-gray-600">
        <span class="font-medium text-gray-500">Empresa</span>
        <select
          v-model="empresa"
          class="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-800 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
        >
          <option v-for="e in empresasDisponibles" :key="e" :value="e">
            {{ e }}
          </option>
        </select>
      </label>
    </nav>

    <DashboardFidelmira v-if="tab === 'dash'" :empresa="empresa" />
    <VistaEeffAcercamiento v-else-if="tab === 'eeff'" :empresa="empresa" />
    <VistaEeffExcelProyeccion v-else-if="tab === 'eeff_excel'" :empresa="empresa" />
    <VistaCmfProyeccion v-else-if="tab === 'cmf'" :empresa="empresa" />
    <VistaEerr v-else-if="tab === 'eeff_eerr'" :empresa="empresa" />
    <VistaBalance v-else-if="tab === 'balance_trib'" :empresa="empresa" norma="Trib" />
    <VistaBalance v-else-if="tab === 'balance_ifrs'" :empresa="empresa" norma="IFRS" />

    <button 
      v-if="!isChatOpen" 
      @click="isChatOpen = true"
      class="fixed bottom-6 right-6 w-14 h-14 bg-indigo-600 text-white rounded-full shadow-2xl hover:bg-indigo-700 transition-transform hover:scale-105 flex items-center justify-center z-50 focus:outline-none"
      title="Abrir Asistente IA"
    >
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-7 h-7">
        <path fill-rule="evenodd" d="M4.804 21.644A6.707 6.707 0 006 21.75a6.721 6.721 0 003.583-1.029c.774.182 1.584.279 2.417.279 5.322 0 9.75-3.97 9.75-9 0-5.03-4.428-9-9.75-9s-9.75 3.97-9.75 9c0 2.409 1.025 4.587 2.674 6.192.232.226.277.428.254.543a3.73 3.73 0 01-.814 1.686.75.75 0 00.44 1.223zM8.25 10.875a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25zM10.875 12a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0zm4.875-1.125a1.125 1.125 0 100 2.25 1.125 1.125 0 000-2.25z" clip-rule="evenodd" />
      </svg>
    </button>

    <ChatFinanciero v-if="isChatOpen" @close="isChatOpen = false" :empresa="empresa" />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import DashboardFidelmira from "./components/DashboardFidelmira.vue";
import VistaEeffAcercamiento from "./components/VistaEeffAcercamiento.vue";
import VistaEeffExcelProyeccion from "./components/VistaEeffExcelProyeccion.vue";
import VistaCmfProyeccion from "./components/VistaCmfProyeccion.vue";
import VistaEerr from "./components/DashboardEERR.vue";

import ChatFinanciero from "./components/ChatFinanciero.vue";
import VistaBalance from "./components/BalanceTributario.vue"; 
import { EMPRESAS } from "./utils/empresas.js";

const tab = ref("dash");
const isChatOpen = ref(false); // NUEVO ESTADO PARA EL CHAT

const contabilidadGlob = import.meta.glob("./assets/data/*/contabilidad.json", {
  eager: true,
});
const empresasDisponibles = computed(() => {
  const set = new Set();
  for (const path of Object.keys(contabilidadGlob)) {
    const normalized = path.replace(/\\/g, "/");
    const idx = normalized.indexOf("/data/");
    if (idx === -1) continue;
    const rest = normalized.slice(idx + "/data/".length);
    const seg = rest.split("/")[0];
    if (seg) set.add(seg);
  }
  const list = EMPRESAS.filter((e) => set.has(e));
  return list.length ? list : [...set].sort();
});

const empresa = ref("FIDELMIRA");

onMounted(() => {
  if (!empresasDisponibles.value.includes(empresa.value)) {
    empresa.value = empresasDisponibles.value[0] || "FIDELMIRA";
  }
});

const tabActive =
  "rounded-lg px-4 py-2 text-sm font-medium bg-indigo-600 text-white shadow";
const tabIdle =
  "rounded-lg px-4 py-2 text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200";
</script>

<style>
/* Tailwind en style.css principal */
</style>