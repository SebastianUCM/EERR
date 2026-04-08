<template>
  <div class="min-h-screen bg-slate-50 p-6 md:p-8 font-sans text-slate-800">
    <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
      <div>
        <h1 class="text-2xl font-bold text-slate-900">
          Estado de Resultados EERR
        </h1>
        <p class="text-sm text-slate-500 mt-1">
          Montos desde <code class="text-xs bg-slate-100 px-1 rounded">datos_vue.json</code>,
          categorías desde <code class="text-xs bg-slate-100 px-1 rounded">mapeo_cuentas.json</code>
          — {{ props.empresa }}
        </p>
      </div>

      <div class="rounded-xl border border-slate-200 bg-white p-3 shadow-sm flex items-center gap-3">
        <label class="text-xs font-semibold uppercase text-slate-500">Año Operativo:</label>
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
      <div class="bg-white rounded-xl shadow-sm p-5 border-l-4 border-emerald-500">
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">Ingresos Acumulados</p>
        <p class="text-2xl font-bold text-slate-900 mt-1">{{ formatCLP(kpis.ingresos) }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border-l-4 border-rose-500">
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">Gastos Acumulados</p>
        <p class="text-2xl font-bold text-slate-900 mt-1">{{ formatCLP(kpis.gastos) }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border-l-4" :class="kpis.ebitda >= 0 ? 'border-purple-500' : 'border-orange-500'">
        <p class="text-xs uppercase text-slate-500 font-bold tracking-wider">EBITDA</p>
        <p class="text-2xl font-bold mt-1" :class="kpis.ebitda >= 0 ? 'text-purple-700' : 'text-orange-600'">
          {{ formatCLP(kpis.ebitda) }}
        </p>
      </div>
      <div class="bg-slate-800 rounded-xl shadow-sm p-5 border-l-4" :class="kpis.resultado >= 0 ? 'border-emerald-400' : 'border-rose-400'">
        <p class="text-xs uppercase text-slate-400 font-bold tracking-wider">Resultado del Ejercicio</p>
        <p class="text-2xl font-bold mt-1" :class="kpis.resultado >= 0 ? 'text-emerald-400' : 'text-rose-400'">
          {{ formatCLP(kpis.resultado) }}
        </p>
      </div>
    </div>

    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden mb-6">
      <div class="px-5 py-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
        <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wide">
          Matriz Financiera {{ filtroAnio }}
        </h2>
        <span class="text-xs bg-indigo-100 text-indigo-700 px-2 py-1 rounded font-semibold">
          Niveles: Categoría ▾ Subítem ▾ Cuenta ▾ Centro Costo
        </span>
      </div>

      <div class="overflow-x-auto max-h-[65vh]">
        <table class="min-w-[1400px] w-full text-xs border-collapse">
          <thead class="sticky top-0 z-20 bg-slate-100 shadow-sm">
            <tr class="border-b border-slate-300 text-slate-700">
              <th class="px-4 py-3 text-left font-bold min-w-[24rem]">Estructura de Cuentas</th>
              <th v-for="m in 12" :key="m" class="px-2 py-3 text-right font-bold min-w-[6.5rem]">{{ mesNombre(m) }}</th>
              <th class="px-4 py-3 text-right font-bold min-w-[8rem] bg-slate-200/50">TOTAL</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="grupo in matrizContable" :key="grupo.key">
              
              <tr :class="`border-y ${grupo.config.colorHeader} sticky top-[41px] z-10 shadow-sm`">
                <td class="px-4 py-2.5 font-bold text-slate-900 text-[13px] uppercase tracking-wide">{{ grupo.config.label }}</td>
                <td v-for="m in 12" :key="'g-' + m" class="px-2 py-2.5 text-right font-mono font-bold" :class="grupo.mensual[m] < 0 ? 'text-rose-700' : 'text-slate-800'">
                  {{ formatCLPContable(grupo.mensual[m]) }}
                </td>
                <td class="px-4 py-2.5 text-right font-mono font-bold bg-white/30" :class="grupo.total < 0 ? 'text-rose-700' : 'text-slate-900'">
                  {{ formatCLPContable(grupo.total) }}
                </td>
              </tr>

              <template v-for="subitem in grupo.subitems" :key="subitem.key">
                <tr class="border-b border-slate-200 cursor-pointer hover:bg-slate-50 transition-colors bg-white" @click="toggleFila(subitem.key)">
                  <td class="px-4 py-2 pl-8 font-semibold text-slate-800 flex items-center gap-2">
                    <span class="text-indigo-500 text-lg leading-none w-4">{{ filasAbiertas[subitem.key] ? "▾" : "▸" }}</span>
                    <span class="capitalize">{{ formatearNombre(subitem.nombreOriginal) }}</span>
                  </td>
                  <td v-for="m in 12" :key="'s-' + m" class="px-2 py-2 text-right font-mono text-slate-700 font-medium" :class="subitem.mensual[m] < 0 ? 'text-rose-600' : ''">
                    {{ formatCLPContable(subitem.mensual[m]) }}
                  </td>
                  <td class="px-4 py-2 text-right font-mono font-bold bg-slate-50/50" :class="subitem.total < 0 ? 'text-rose-700' : 'text-slate-800'">
                    {{ formatCLPContable(subitem.total) }}
                  </td>
                </tr>

                <template v-if="filasAbiertas[subitem.key]">
                  <template v-for="cuenta in subitem.cuentas" :key="cuenta.key">
                    
                    <tr class="border-b border-slate-100 cursor-pointer hover:bg-indigo-50/30 transition-colors bg-slate-50/50" @click="toggleFila(subitem.key + '-' + cuenta.key)">
                      <td class="px-4 py-1.5 pl-14 font-medium text-slate-700 flex items-center gap-2">
                        <span class="text-slate-400 text-lg leading-none w-4">{{ filasAbiertas[subitem.key + '-' + cuenta.key] ? "▾" : "▸" }}</span>
                        <span class="text-indigo-600 font-mono">{{ cuenta.codigo }}</span>
                        <span class="truncate max-w-[15rem]">{{ cuenta.nombre }}</span>
                      </td>
                      <td v-for="m in 12" :key="'c-' + m" class="px-2 py-1.5 text-right font-mono text-slate-600 text-[11px]" :class="cuenta.mensual[m] < 0 ? 'text-rose-500' : ''">
                        {{ formatCLPContable(cuenta.mensual[m]) }}
                      </td>
                      <td class="px-4 py-1.5 text-right font-mono font-semibold bg-slate-100/50 text-[11px]" :class="cuenta.total < 0 ? 'text-rose-600' : 'text-slate-700'">
                        {{ formatCLPContable(cuenta.total) }}
                      </td>
                    </tr>

                    <template v-if="filasAbiertas[subitem.key + '-' + cuenta.key]">
                      <tr v-for="cc in cuenta.centros" :key="cc.key" class="border-b border-slate-50 hover:bg-slate-100 transition-colors bg-white">
                        <td class="px-4 py-1 pl-[5.5rem] text-slate-500 text-[11px] flex items-center gap-1.5">
                          <span class="w-1 h-1 rounded-full bg-slate-300"></span>
                          <span class="font-mono text-slate-400">{{ cc.codigo === '000' ? '' : cc.codigo }}</span>
                          <span class="truncate max-w-[14rem]">{{ cc.codigo === '000' ? 'Sin Centro de Costo' : cc.nombre }}</span>
                        </td>
                        <td v-for="m in 12" :key="'cc-' + m" class="px-2 py-1 text-right font-mono text-slate-400 text-[11px]" :class="cc.mensual[m] < 0 ? 'text-rose-400' : ''">
                          {{ formatCLPContable(cc.mensual[m]) }}
                        </td>
                        <td class="px-4 py-1 text-right font-mono font-medium text-slate-500 bg-white text-[11px]" :class="cc.total < 0 ? 'text-rose-500' : ''">
                          {{ formatCLPContable(cc.total) }}
                        </td>
                      </tr>
                    </template>
                    
                  </template>
                </template>
                
              </template>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm p-5 border border-slate-200">
        <h2 class="font-bold text-slate-800 mb-4">Evolución Ingresos vs Gastos</h2>
        <apexchart type="bar" height="300" :options="chartOptionsBarras" :series="chartSeriesBarras"></apexchart>
      </div>
      <div class="bg-white rounded-xl shadow-sm p-5 border border-slate-200">
        <h2 class="font-bold text-slate-800 mb-4">Distribución del Gasto</h2>
        <apexchart type="donut" height="300" :options="chartOptionsDonut" :series="chartSeriesDonut"></apexchart>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
import eerrDataRaw from "../assets/datos_vue.json";
import mapeoCuentas from "../assets/config/mapeo_cuentas.json";

const props = defineProps({
  empresa: { type: String, required: true },
});

const filtroAnio = ref(new Date().getFullYear());
const filasAbiertas = ref({});

const toggleFila = (key) => {
  filasAbiertas.value[key] = !filasAbiertas.value[key];
};

const BLOQUES_FINANCIEROS = [
  { key: "ingreso_explotacion", label: "Ingresos de Explotación", colorHeader: "bg-emerald-200 border-emerald-400" },
  { key: "ingreso_financiero", label: "Ingresos Financieros", colorHeader: "bg-cyan-200 border-cyan-400" },
  { key: "gasto_adm_ventas", label: "Gastos de Administración y Ventas", colorHeader: "bg-amber-200 border-amber-400" },
  { key: "otros_resultados", label: "Otros Resultados", colorHeader: "bg-violet-200 border-violet-400" },
];

const ordenSubitems = computed(() => {
  const dict = {};
  const configEmpresa = mapeoCuentas?.empresas?.[props.empresa] || {};
  const cuentas = configEmpresa.cuentas || {};

  Object.values(cuentas).forEach((c) => {
    const sub = c.subitem || "sin_subitem";
    const ord = Number(c.orden ?? 9999);
    if (!(sub in dict) || ord < dict[sub]) dict[sub] = ord;
  });
  return dict;
});

function normAnio(v) { return Number(v); }
function normMes(v) {
  const n = Number(v);
  if (n >= 1 && n <= 12) return n;
  const x = parseInt(String(v || "").trim().replace(/^0+/, "") || "0", 10);
  return x >= 1 && x <= 12 ? x : 1;
}

const datosEmpresa = computed(() =>
  eerrDataRaw.filter((d) => String(d.Empresa).trim() === String(props.empresa).trim())
);

const aniosDisponibles = computed(() => {
  const set = new Set(datosEmpresa.value.map((d) => normAnio(d.Anio)));
  const arr = Array.from(set).sort((a, b) => b - a);
  return arr.length ? arr : [new Date().getFullYear()];
});

watch(() => props.empresa, () => {
  filtroAnio.value = aniosDisponibles.value[0];
  filasAbiertas.value = {};
});

onMounted(() => {
  if (aniosDisponibles.value.length) filtroAnio.value = aniosDisponibles.value[0];
});

const datosAnio = computed(() =>
  datosEmpresa.value.filter((d) => normAnio(d.Anio) === Number(filtroAnio.value))
);

// Mapeo Inteligente
const datosAnioMapeados = computed(() => {
  const configEmpresa = mapeoCuentas?.empresas?.[props.empresa];
  if (!configEmpresa) return []; 

  const mapCuentas = configEmpresa.cuentas || {};
  const reglasSubitem = configEmpresa.reglas_subitem || [];
  const fallbacks = configEmpresa.fallback || {};
  const prefijos = fallbacks.categoria_por_prefijo || [];

  const rows = [];
  for (const d of datosAnio.value) {
    const cod = String(d.CodigoCuenta ?? "").trim();
    const nombreCta = String(d.NombreCuenta || d.Cuenta || "").toUpperCase(); 
    if (!cod) continue;

    let categoria = null;
    let subitem = null;

    if (mapCuentas[cod]) {
      categoria = mapCuentas[cod].categoria;
      subitem = mapCuentas[cod].subitem;
    } else {
      for (const pref of prefijos) {
        if (cod.startsWith(pref.prefijo)) {
          categoria = pref.categoria;
          break;
        }
      }
      if (!categoria) categoria = fallbacks.categoria_default || "otros_resultados";

      for (const regla of reglasSubitem) {
        if (regla.match_nombre.some(keyword => nombreCta.includes(keyword))) {
          subitem = regla.subitem;
          break;
        }
      }
      if (!subitem) subitem = fallbacks.subitem_default || "sin_subitem";
    }

    const mes = normMes(d.Mes);
    rows.push({
      ...d,
      Categoria: categoria,
      Subitem: subitem,
      Mes: mes,
      SaldoNeto: Number(d.SaldoNeto ?? 0),
    });
  }
  return rows;
});

// MOTOR MATRIZ EN CASCADA
const matrizContable = computed(() => {
  const mapaCategorias = new Map();

  BLOQUES_FINANCIEROS.forEach((bloque) => {
    mapaCategorias.set(bloque.key, {
      key: bloque.key,
      config: bloque,
      mensual: { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0 },
      total: 0,
      subitemsMap: new Map(),
    });
  });

  datosAnioMapeados.value.forEach((d) => {
    const catKey = mapaCategorias.has(d.Categoria) ? d.Categoria : "otros_resultados";
    const categoria = mapaCategorias.get(catKey);

    // NIVEL 2: SUBITEM
    const subKey = d.Subitem || "sin_subitem";
    if (!categoria.subitemsMap.has(subKey)) {
      categoria.subitemsMap.set(subKey, {
        key: `${catKey}-${subKey}`,
        nombreOriginal: subKey,
        mensual: { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0 },
        total: 0,
        cuentasMap: new Map(),
      });
    }
    const subitem = categoria.subitemsMap.get(subKey);

    // NIVEL 3: CUENTA CONTABLE
    const ctaKey = d.CodigoCuenta;
    if (!subitem.cuentasMap.has(ctaKey)) {
      subitem.cuentasMap.set(ctaKey, {
        key: ctaKey,
        codigo: ctaKey,
        nombre: d.NombreCuenta || d.Cuenta || "Sin Nombre",
        mensual: { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0 },
        total: 0,
        centrosMap: new Map()
      });
    }
    const cuenta = subitem.cuentasMap.get(ctaKey);

    // NIVEL 4: CENTRO DE COSTO
    const ccKey = d.CodigoCentroCosto || "000";
    if (!cuenta.centrosMap.has(ccKey)) {
      cuenta.centrosMap.set(ccKey, {
        key: ccKey,
        codigo: ccKey,
        nombre: d.CentroCosto || "Sin Centro de Costo",
        mensual: { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0 },
        total: 0,
      });
    }
    const centro = cuenta.centrosMap.get(ccKey);

    // SUMATORIAS
    const monto = d.SaldoNeto || 0;
    const mes = d.Mes;

    categoria.mensual[mes] += monto;  categoria.total += monto;
    subitem.mensual[mes] += monto;    subitem.total += monto;
    cuenta.mensual[mes] += monto;     cuenta.total += monto;
    centro.mensual[mes] += monto;     centro.total += monto;
  });

  return Array.from(mapaCategorias.values())
    .filter((cat) => cat.total !== 0 || Object.values(cat.mensual).some((v) => v !== 0))
    .map((cat) => ({
      ...cat,
      subitems: Array.from(cat.subitemsMap.values())
        .sort((a, b) => {
          const ordA = ordenSubitems.value[a.nombreOriginal] ?? 9999;
          const ordB = ordenSubitems.value[b.nombreOriginal] ?? 9999;
          if (ordA !== ordB) return ordA - ordB;
          return a.nombreOriginal.localeCompare(b.nombreOriginal);
        })
        .map((sub) => ({
          ...sub,
          cuentas: Array.from(sub.cuentasMap.values())
            .sort((a, b) => a.codigo.localeCompare(b.codigo, "es", { numeric: true }))
            .map((cta) => ({
              ...cta,
              centros: Array.from(cta.centrosMap.values())
                .sort((a, b) => a.codigo.localeCompare(b.codigo, "es", { numeric: true }))
            }))
        })),
    }));
});

const kpis = computed(() => {
  let ingresos = 0, gastos = 0, resultado = 0;

  datosAnioMapeados.value.forEach((d) => {
    resultado += d.SaldoNeto;
    if (d.Categoria === "ingreso_explotacion" || d.Categoria === "ingreso_financiero") {
      ingresos += d.SaldoNeto;
    } else {
      gastos += Math.abs(d.SaldoNeto);
    }
  });

  return { ingresos, gastos, ebitda: resultado, resultado }; 
});

const chartSeriesBarras = computed(() => {
  const ingresos = Array(12).fill(0);
  const gastos = Array(12).fill(0);

  datosAnioMapeados.value.forEach((d) => {
    const idx = d.Mes - 1;
    if (d.Categoria === "ingreso_explotacion" || d.Categoria === "ingreso_financiero") {
      ingresos[idx] += d.SaldoNeto;
    } else {
      gastos[idx] += Math.abs(d.SaldoNeto);
    }
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
  xaxis: { categories: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"] },
  yaxis: { labels: { formatter: (val) => "$" + (val / 1000000).toFixed(1) + "M" } },
  tooltip: { y: { formatter: (val) => formatCLP(val) } },
}));

const chartSeriesDonut = computed(() => {
  const mapGastos = {};
  datosAnioMapeados.value
    .filter((d) => d.Categoria === "gasto_adm_ventas")
    .forEach((d) => {
      mapGastos[d.Subitem] = (mapGastos[d.Subitem] || 0) + Math.abs(d.SaldoNeto);
    });
  return Object.values(mapGastos);
});

const chartOptionsDonut = computed(() => {
  const mapGastos = {};
  datosAnioMapeados.value
    .filter((d) => d.Categoria === "gasto_adm_ventas")
    .forEach((d) => {
      mapGastos[d.Subitem] = (mapGastos[d.Subitem] || 0) + Math.abs(d.SaldoNeto);
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

const formatCLP = (v) => new Intl.NumberFormat("es-CL", { style: "currency", currency: "CLP", maximumFractionDigits: 0 }).format(Math.round(Number(v || 0)));
const formatCLPContable = (v) => {
  if (!v || v === 0) return "-";
  const n = Math.round(Number(v));
  const abs = new Intl.NumberFormat("es-CL", { maximumFractionDigits: 0 }).format(Math.abs(n));
  return n < 0 ? `(${abs})` : abs;
};
const formatearNombre = (t) => String(t || "").replace(/_/g, " ");
const mesNombre = (m) => ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"][m - 1];
const mesNombreAbrev = (m) => ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"][m - 1];
</script>