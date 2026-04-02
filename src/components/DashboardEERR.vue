<template>
  <div class="min-h-screen bg-slate-50 p-6 md:p-8 font-sans text-slate-800">
    <header
      class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4"
    >
      <div>
        <h1 class="text-2xl font-bold text-slate-900">
          Estado de Resultados EERR
        </h1>
        <p class="text-sm text-slate-500 mt-1">
          Consolidado dinámico desde Softland - {{ props.empresa }}
        </p>
      </div>

      <div
        class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm flex items-center gap-3"
      >
        <label class="text-xs font-semibold uppercase text-slate-500"
          >Año Operativo:</label
        >
        <select
          v-model.number="filtroAnio"
          class="border border-slate-300 rounded-md px-3 py-1.5 text-sm bg-white font-medium focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
        >
          <option v-for="a in aniosDisponibles" :key="a" :value="a">
            {{ a }}
          </option>
        </select>
      </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div
        class="bg-white rounded-xl shadow-sm p-5 border-l-4 border-emerald-500"
      >
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">
          Ingresos Acumulados
        </p>
        <p class="text-2xl font-bold text-slate-900 mt-1">
          {{ formatCLP(kpis.ingresos) }}
        </p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border-l-4 border-rose-500">
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">
          Gastos Acumulados
        </p>
        <p class="text-2xl font-bold text-slate-900 mt-1">
          {{ formatCLP(kpis.gastos) }}
        </p>
      </div>
      <div
        class="bg-white rounded-xl shadow-sm p-5 border-l-4"
        :class="kpis.ebitda >= 0 ? 'border-purple-500' : 'border-orange-500'"
      >
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">
          EBITDA
        </p>
        <p
          class="text-2xl font-bold mt-1"
          :class="kpis.ebitda >= 0 ? 'text-purple-700' : 'text-orange-600'"
        >
          {{ formatCLP(kpis.ebitda) }}
        </p>
      </div>
      <div
        class="bg-slate-800 rounded-xl shadow-sm p-5 border-l-4"
        :class="kpis.resultado >= 0 ? 'border-emerald-400' : 'border-rose-400'"
      >
        <p class="text-xs uppercase text-slate-400 font-bold tracking-wider">
          Resultado del Ejercicio
        </p>
        <p
          class="text-2xl font-bold mt-1"
          :class="kpis.resultado >= 0 ? 'text-emerald-400' : 'text-rose-400'"
        >
          {{ formatCLP(kpis.resultado) }}
        </p>
      </div>
    </div>

    <div
      class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mb-6"
    >
      <div
        class="px-5 py-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center"
      >
        <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
          Matriz Financiera {{ filtroAnio }}
        </h2>
        <span
          class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded font-semibold"
          >Haz clic en un subítem para ver Centros de Costo</span
        >
      </div>

      <div class="overflow-x-auto max-h-[65vh]">
        <table class="min-w-[1200px] w-full text-xs">
          <thead class="sticky top-0 z-20 bg-slate-100 shadow-sm">
            <tr class="border-b border-slate-300 text-slate-700">
              <th class="px-4 py-3 text-left font-bold min-w-[20rem]">
                Categoría / Subítem
              </th>
              <th
                v-for="m in 12"
                :key="m"
                class="px-2 py-3 text-right font-bold min-w-[6.5rem]"
              >
                {{ mesNombre(m) }}
              </th>
              <th
                class="px-4 py-3 text-right font-bold min-w-[8rem] bg-slate-200/50"
              >
                TOTAL
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-for="grupo in matrizContable" :key="grupo.key">
              <tr
                :class="`border-y ${grupo.config.colorHeader} sticky top-[41px] z-10`"
              >
                <td class="px-4 py-2 font-bold text-slate-900 text-[13px]">
                  {{ grupo.config.label }}
                </td>
                <td
                  v-for="m in 12"
                  :key="'g-' + m"
                  class="px-2 py-2 text-right font-mono font-semibold"
                  :class="
                    grupo.mensual[m] < 0 ? 'text-rose-700' : 'text-slate-800'
                  "
                >
                  {{ formatCLPContable(grupo.mensual[m]) }}
                </td>
                <td
                  class="px-4 py-2 text-right font-mono font-bold bg-white/30"
                  :class="grupo.total < 0 ? 'text-rose-700' : 'text-slate-900'"
                >
                  {{ formatCLPContable(grupo.total) }}
                </td>
              </tr>

              <template v-for="subitem in grupo.subitems" :key="subitem.key">
                <tr
                  class="border-b border-slate-100 cursor-pointer hover:bg-indigo-50/50 transition-colors"
                  @click="toggleFila(subitem.key)"
                >
                  <td
                    class="px-4 py-2 pl-8 font-medium text-slate-700 flex items-center gap-2"
                  >
                    <span class="text-slate-400 text-lg leading-none w-4">{{
                      filasAbiertas[subitem.key] ? "▾" : "▸"
                    }}</span>
                    <span class="capitalize">{{
                      formatearNombre(subitem.key)
                    }}</span>
                  </td>
                  <td
                    v-for="m in 12"
                    :key="'s-' + m"
                    class="px-2 py-2 text-right font-mono text-slate-600"
                    :class="subitem.mensual[m] < 0 ? 'text-rose-600' : ''"
                  >
                    {{ formatCLPContable(subitem.mensual[m]) }}
                  </td>
                  <td
                    class="px-4 py-2 text-right font-mono font-semibold bg-slate-50/50"
                    :class="
                      subitem.total < 0 ? 'text-rose-700' : 'text-slate-800'
                    "
                  >
                    {{ formatCLPContable(subitem.total) }}
                  </td>
                </tr>

                <tr
                  v-if="filasAbiertas[subitem.key]"
                  class="bg-slate-50/80 border-b border-slate-200 shadow-inner"
                >
                  <td colspan="14" class="px-0 py-0">
                    <div
                      class="pl-12 pr-4 py-3 bg-indigo-50/20 border-l-4 border-indigo-300"
                    >
                      <table class="w-full text-[11px]">
                        <thead>
                          <tr class="text-slate-500 border-b border-indigo-100">
                            <th class="py-1 text-left font-semibold w-64">
                              Centro de Costo
                            </th>
                            <th
                              v-for="m in 12"
                              :key="'cch-' + m"
                              class="py-1 text-right font-semibold w-24"
                            >
                              {{ mesNombreAbrev(m) }}
                            </th>
                            <th class="py-1 text-right font-bold w-28">
                              Total CC
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="cc in subitem.centros"
                            :key="cc.key"
                            class="border-b border-indigo-50/50 hover:bg-white transition-colors"
                          >
                            <td class="py-1.5 text-slate-700">
                              {{
                                cc.key === "000"
                                  ? "Sin Centro de Costo"
                                  : cc.nombre
                              }}
                              <span class="text-slate-400 font-mono ml-1"
                                >({{ cc.key }})</span
                              >
                            </td>
                            <td
                              v-for="m in 12"
                              :key="'ccm-' + m"
                              class="py-1.5 text-right font-mono text-slate-500"
                              :class="cc.mensual[m] < 0 ? 'text-rose-500' : ''"
                            >
                              {{ formatCLPContable(cc.mensual[m]) }}
                            </td>
                            <td
                              class="py-1.5 text-right font-mono font-semibold"
                              :class="
                                cc.total < 0
                                  ? 'text-rose-600'
                                  : 'text-slate-700'
                              "
                            >
                              {{ formatCLPContable(cc.total) }}
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </td>
                </tr>
              </template>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div
        class="lg:col-span-2 bg-white rounded-xl shadow-sm p-5 border border-slate-200"
      >
        <h2 class="font-bold text-slate-800 mb-4">
          Evolución Ingresos vs Gastos
        </h2>
        <apexchart
          type="bar"
          height="300"
          :options="chartOptionsBarras"
          :series="chartSeriesBarras"
        ></apexchart>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border border-slate-200">
        <h2 class="font-bold text-slate-800 mb-4">Distribución del Gasto</h2>
        <apexchart
          type="donut"
          height="300"
          :options="chartOptionsDonut"
          :series="chartSeriesDonut"
        ></apexchart>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import eerrDataRaw from "../assets/datos_vue.json";
import mapeoCuentas from "../assets/config/mapeo_cuentas.json"; // <-- RUTA A TU MAPEO REAL

const props = defineProps({
  empresa: { type: String, required: true },
});

// 1. Estado
const filtroAnio = ref(new Date().getFullYear());
const filasAbiertas = ref({});

const toggleFila = (key) => {
  filasAbiertas.value[key] = !filasAbiertas.value[key];
};

// 2. Definición de Bloques (Estrictamente los 4 de tu mapeo.json)
const BLOQUES_FINANCIEROS = [
  {
    key: "ingreso_explotacion",
    label: "Ingresos de Explotación",
    colorHeader: "bg-emerald-200 border-emerald-400",
  },
  {
    key: "ingreso_financiero",
    label: "Ingresos Financieros",
    colorHeader: "bg-cyan-200 border-cyan-400",
  },
  {
    key: "gasto_adm_ventas",
    label: "Gastos de Administración y Ventas",
    colorHeader: "bg-amber-200 border-amber-400",
  },
  {
    key: "otros_resultados",
    label: "Otros Resultados",
    colorHeader: "bg-violet-200 border-violet-400",
  },
];

// 3. Extracción del "Orden" desde tu mapeo.json
// Esto busca el número de "orden" más bajo para cada subítem y lo guarda en un diccionario
const ordenSubitems = computed(() => {
  const dict = {};
  const configEmpresa = mapeoCuentas?.empresas?.[props.empresa] || {};
  const cuentas = configEmpresa.cuentas || {};

  Object.values(cuentas).forEach((c) => {
    const sub = c.subitem || "sin_subitem";
    const ord = Number(c.orden ?? 9999);
    if (!(sub in dict) || ord < dict[sub]) {
      dict[sub] = ord;
    }
  });
  return dict;
});

// 4. Computed base
const datosEmpresa = computed(() =>
  eerrDataRaw.filter((d) => d.Empresa === props.empresa)
);

const aniosDisponibles = computed(() => {
  const set = new Set(datosEmpresa.value.map((d) => d.Anio));
  const arr = Array.from(set).sort((a, b) => b - a);
  return arr.length ? arr : [new Date().getFullYear()];
});

watch(
  () => props.empresa,
  () => {
    filtroAnio.value = aniosDisponibles.value[0];
    filasAbiertas.value = {};
  }
);
onMounted(() => {
  if (aniosDisponibles.value.length)
    filtroAnio.value = aniosDisponibles.value[0];
});

const datosAnio = computed(() =>
  datosEmpresa.value.filter((d) => d.Anio === filtroAnio.value)
);

// 5. EL MOTOR DE LA MATRIZ (Ahora respeta tu orden)
const matrizContable = computed(() => {
  const mapaCategorias = new Map();

  BLOQUES_FINANCIEROS.forEach((bloque) => {
    mapaCategorias.set(bloque.key, {
      key: bloque.key,
      config: bloque,
      mensual: {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0,
      },
      total: 0,
      subitemsMap: new Map(),
    });
  });

  datosAnio.value.forEach((d) => {
    const catKey = mapaCategorias.has(d.Categoria)
      ? d.Categoria
      : "otros_resultados";
    const categoria = mapaCategorias.get(catKey);

    const subKey = d.Subitem || "sin_subitem";
    if (!categoria.subitemsMap.has(subKey)) {
      categoria.subitemsMap.set(subKey, {
        key: `${catKey}-${subKey}`,
        nombreOriginal: subKey, // Guardamos el nombre original para buscar su orden
        mensual: {
          1: 0,
          2: 0,
          3: 0,
          4: 0,
          5: 0,
          6: 0,
          7: 0,
          8: 0,
          9: 0,
          10: 0,
          11: 0,
          12: 0,
        },
        total: 0,
        centrosMap: new Map(),
      });
    }
    const subitem = categoria.subitemsMap.get(subKey);

    const ccKey = d.CodigoCentroCosto || "000";
    if (!subitem.centrosMap.has(ccKey)) {
      subitem.centrosMap.set(ccKey, {
        key: ccKey,
        nombre: d.CentroCosto,
        mensual: {
          1: 0,
          2: 0,
          3: 0,
          4: 0,
          5: 0,
          6: 0,
          7: 0,
          8: 0,
          9: 0,
          10: 0,
          11: 0,
          12: 0,
        },
        total: 0,
      });
    }
    const centro = subitem.centrosMap.get(ccKey);

    const monto = d.SaldoNeto || 0;
    const mes = d.Mes;

    categoria.mensual[mes] += monto;
    categoria.total += monto;
    subitem.mensual[mes] += monto;
    subitem.total += monto;
    centro.mensual[mes] += monto;
    centro.total += monto;
  });

  return Array.from(mapaCategorias.values())
    .filter(
      (cat) =>
        cat.total !== 0 || Object.values(cat.mensual).some((v) => v !== 0)
    )
    .map((cat) => ({
      ...cat,
      // AQUÍ OCURRE LA MAGIA: Ordenamos por el 'orden' de tu JSON
      subitems: Array.from(cat.subitemsMap.values())
        .sort((a, b) => {
          const ordA = ordenSubitems.value[a.nombreOriginal] ?? 9999;
          const ordB = ordenSubitems.value[b.nombreOriginal] ?? 9999;
          if (ordA !== ordB) return ordA - ordB; // Ordena por el número de tu JSON
          return a.nombreOriginal.localeCompare(b.nombreOriginal); // Empate -> Alfabético
        })
        .map((sub) => ({
          ...sub,
          // Ordenamos los Centros de Costo por código numérico para mayor prolijidad
          centros: Array.from(sub.centrosMap.values()).sort((a, b) =>
            a.key.localeCompare(b.key, "es", { numeric: true })
          ),
        })),
    }));
});

// 6. KPIs Financieros (Adaptados a tus 4 categorías)
const kpis = computed(() => {
  let ingresos = 0,
    gastos = 0,
    resultado = 0;

  datosAnio.value.forEach((d) => {
    resultado += d.SaldoNeto;
    if (
      d.Categoria === "ingreso_explotacion" ||
      d.Categoria === "ingreso_financiero"
    ) {
      ingresos += d.SaldoNeto;
    } else {
      gastos += Math.abs(d.SaldoNeto);
    }
  });

  return { ingresos, gastos, ebitda: resultado, resultado }; // El EBITDA lo igualamos al resultado si no defines cuentas de depreciación separadas
});

// 7. Gráficos
const chartSeriesBarras = computed(() => {
  const ingresos = Array(12).fill(0);
  const gastos = Array(12).fill(0);

  datosAnio.value.forEach((d) => {
    const idx = d.Mes - 1;
    if (
      d.Categoria === "ingreso_explotacion" ||
      d.Categoria === "ingreso_financiero"
    )
      ingresos[idx] += d.SaldoNeto;
    else gastos[idx] += Math.abs(d.SaldoNeto);
  });

  return [
    { name: "Ingresos Totales", data: ingresos },
    { name: "Gastos Totales", data: gastos },
  ];
});

const chartOptionsBarras = computed(() => ({
  chart: { type: "bar", toolbar: { show: false }, fontFamily: "inherit" },
  colors: ["#10B981", "#EF4444"],
  plotOptions: { bar: { columnWidth: "50%", borderRadius: 2 } },
  dataLabels: { enabled: false },
  stroke: { show: true, width: 2, colors: ["transparent"] },
  xaxis: {
    categories: [
      "Ene",
      "Feb",
      "Mar",
      "Abr",
      "May",
      "Jun",
      "Jul",
      "Ago",
      "Sep",
      "Oct",
      "Nov",
      "Dic",
    ],
  },
  yaxis: {
    labels: { formatter: (val) => "$" + (val / 1000000).toFixed(1) + "M" },
  },
  tooltip: { y: { formatter: (val) => formatCLP(val) } },
}));

const chartSeriesDonut = computed(() => {
  const mapGastos = {};
  datosAnio.value
    .filter((d) => d.Categoria === "gasto_adm_ventas")
    .forEach((d) => {
      mapGastos[d.Subitem] =
        (mapGastos[d.Subitem] || 0) + Math.abs(d.SaldoNeto);
    });
  return Object.values(mapGastos);
});

const chartOptionsDonut = computed(() => {
  const mapGastos = {};
  datosAnio.value
    .filter((d) => d.Categoria === "gasto_adm_ventas")
    .forEach((d) => {
      mapGastos[d.Subitem] =
        (mapGastos[d.Subitem] || 0) + Math.abs(d.SaldoNeto);
    });
  return {
    chart: { type: "donut", fontFamily: "inherit" },
    labels: Object.keys(mapGastos).map(formatearNombre),
    colors: ["#EF4444", "#F97316", "#F59E0B", "#8B5CF6", "#EC4899", "#06B6D4"],
    dataLabels: { enabled: false },
    stroke: { width: 0 },
    legend: { position: "bottom" },
    tooltip: { y: { formatter: (val) => formatCLP(val) } },
  };
});

// 8. Helpers de Formato
const formatCLP = (v) =>
  new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    maximumFractionDigits: 0,
  }).format(Math.round(Number(v || 0)));
const formatCLPContable = (v) => {
  if (!v || v === 0) return "-";
  const n = Math.round(Number(v));
  const abs = new Intl.NumberFormat("es-CL", {
    maximumFractionDigits: 0,
  }).format(Math.abs(n));
  return n < 0 ? `(${abs})` : abs;
};
const formatearNombre = (t) => String(t || "").replace(/_/g, " ");
const mesNombre = (m) =>
  [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
  ][m - 1];
const mesNombreAbrev = (m) =>
  [
    "Ene",
    "Feb",
    "Mar",
    "Abr",
    "May",
    "Jun",
    "Jul",
    "Ago",
    "Sep",
    "Oct",
    "Nov",
    "Dic",
  ][m - 1];
</script>