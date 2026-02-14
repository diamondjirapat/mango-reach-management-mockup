<script setup>
import { ref, onMounted } from 'vue'
import Dashboard from './components/Dashboard.vue'
import DataTable from './components/DataTable.vue'
import api from './services/api'

const stats = ref(null)
const ads = ref([])
const loading = ref(true)

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
</script>

<template>
  <div class="app-container">
    <header>
      <h1>Ads Reach Engagement Analyzer</h1>
      <button @click="fetchData" class="refresh-btn">Refresh Data</button>
    </header>

    <main v-if="!loading">
      <Dashboard :stats="stats" />
      <div class="divider"></div>
      <DataTable :ads="ads" />
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
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

h1 {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
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
}

.refresh-btn:hover {
  background-color: #3aa876;
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
