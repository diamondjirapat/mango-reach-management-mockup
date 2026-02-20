<script setup>
import { ref, onMounted, watch } from 'vue'
import Dashboard from './components/Dashboard.vue'
import DataTable from './components/DataTable.vue'
import Visualization from './components/Visualization.vue'
import api from './services/api'

const stats = ref(null)
const ads = ref([])
const loading = ref(true)
const activeView = ref(localStorage.getItem('activeView') || 'dashboard')

const fetchData = async () => {
  loading.value = true
  try {
    const [statsResponse, adsResponse] = await Promise.all([
      api.getDashboardStats(),
      api.getAds()
    ])
    stats.value = statsResponse.data
    ads.value = adsResponse.data
  } catch (error) {
    console.error('Error fetching data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})

watch(activeView, (view) => {
  localStorage.setItem('activeView', view)
})
</script>

<template>
  <div class="app-container">
    <header>
      <h1>Ads Reach Engagement Analyzer</h1>
      <div class="actions">
        <button @click="fetchData" class="refresh-btn">Refresh Data</button>
        <button
          v-if="activeView === 'dashboard'"
          @click="activeView = 'visualization'"
          class="viz-btn"
        >
          Visualization
        </button>
        <button
          v-else
          @click="activeView = 'dashboard'"
          class="viz-btn"
        >
          Dashboard
        </button>
      </div>
    </header>

    <main v-if="!loading && activeView === 'dashboard'">
      <Dashboard :stats="stats" />
      <div class="divider"></div>
      <DataTable :ads="ads" />
    </main>
    <main v-else-if="!loading">
      <Visualization :stats="stats" :ads="ads" />
    </main>
    <div v-else class="loading">
      Loading...
    </div>
  </div>
</template>

<style scoped>
.app-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.refresh-btn {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.refresh-btn:hover {
  background-color: #3aa876;
}

.viz-btn {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
  flex-shrink: 0;
}

.viz-btn:hover {
  background-color: #3f566d;
}

.divider {
  height: 2rem;
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin-top: 3rem;
}
</style>
