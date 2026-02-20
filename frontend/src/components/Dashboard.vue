<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  ads: {
    type: Array,
    required: true,
    default: () => []
  }
})

const emit = defineEmits(['filter-change'])

const searchQuery = ref('')
const sourceFilter = ref('')
const typeFilter = ref('')
const scoreFilter = ref('')

const sources = ['Facebook', 'X', 'Instagram', 'Google', 'TikTok', 'Flyers', 'Billboard']

const matchesScore = (ad, bucket) => {
  const score = ad.score || 0
  if (bucket === 'high') return score >= 8
  if (bucket === 'medium') return score >= 5 && score < 8
  if (bucket === 'low') return score < 5
  return true
}

const filteredAds = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  return (props.ads || []).filter((ad) => {
    const matchSearch = !q || (ad.project_name || '').toLowerCase().includes(q) || (ad.project_id || '').toLowerCase().includes(q)
    const matchSource = !sourceFilter.value || ad.source === sourceFilter.value
    const matchType = !typeFilter.value || ad.type === typeFilter.value
    const matchScr = !scoreFilter.value || matchesScore(ad, scoreFilter.value)
    return matchSearch && matchSource && matchType && matchScr
  })
})

const totalProjects = computed(() => filteredAds.value.length)
const totalClicks = computed(() => filteredAds.value.reduce((sum, ad) => sum + (ad.click_count || 0), 0))
const totalCost = computed(() => filteredAds.value.reduce((sum, ad) => sum + (ad.cost || 0), 0))
const averageScore = computed(() => {
  if (!filteredAds.value.length) return 0
  return filteredAds.value.reduce((sum, ad) => sum + (ad.score || 0), 0) / filteredAds.value.length
})

const formattedCost = computed(() => {
  return new Intl.NumberFormat('th-TH', { style: 'currency', currency: 'THB' }).format(totalCost.value)
})

const formattedScore = computed(() => averageScore.value.toFixed(2))

const hasActiveFilter = computed(() => !!(searchQuery.value || sourceFilter.value || typeFilter.value || scoreFilter.value))

const clearFilters = () => {
  searchQuery.value = ''
  sourceFilter.value = ''
  typeFilter.value = ''
  scoreFilter.value = ''
}

import { watch } from 'vue'
watch(filteredAds, (ads) => {
  emit('filter-change', ads)
}, { immediate: true })
</script>

<template>
  <div class="dashboard-section">
    <!-- Filter Bar -->
    <div class="filter-bar">
      <div class="filter-group search-group">
        <label for="filter-search">Search</label>
        <input id="filter-search" v-model="searchQuery" type="text" placeholder="Project name or ID..." />
      </div>
      <div class="filter-group">
        <label for="filter-source">Source</label>
        <select id="filter-source" v-model="sourceFilter">
          <option value="">All Sources</option>
          <option v-for="s in sources" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label for="filter-type">Type</label>
        <select id="filter-type" v-model="typeFilter">
          <option value="">All Types</option>
          <option value="online">Online</option>
          <option value="offline">Offline</option>
        </select>
      </div>
      <div class="filter-group">
        <label for="filter-score">Score</label>
        <select id="filter-score" v-model="scoreFilter">
          <option value="">All Scores</option>
          <option value="high">High (≥8)</option>
          <option value="medium">Medium (5-7.9)</option>
          <option value="low">Low (&lt;5)</option>
        </select>
      </div>
      <button v-if="hasActiveFilter" class="clear-btn" @click="clearFilters">✕ Clear</button>
    </div>

    <!-- Stats Cards -->
    <div class="dashboard-grid">
      <div class="card">
        <h3>Total Projects</h3>
        <p class="value">{{ totalProjects }}</p>
      </div>
      <div class="card">
        <h3>Total Clicks</h3>
        <p class="value">{{ totalClicks }}</p>
      </div>
      <div class="card">
        <h3>Total Cost</h3>
        <p class="value">{{ formattedCost }}</p>
      </div>
      <div class="card highlight">
        <h3>Average Score</h3>
        <p class="value">{{ formattedScore }}</p>
      </div>
    </div>

    <p v-if="hasActiveFilter" class="filter-summary">
      Showing {{ totalProjects }} of {{ ads.length }} projects
    </p>
  </div>
</template>

<style scoped>
.dashboard-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-bar {
  display: flex;
  align-items: flex-end;
  gap: 0.8rem;
  flex-wrap: wrap;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1rem 1.25rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.filter-group label {
  font-size: 0.75rem;
  font-weight: 600;
  color: #7f8c8d;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.filter-group select {
  padding: 0.45rem 0.7rem;
  border: 1px solid #dce1e6;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #2c3e50;
  background: #fafbfc;
  cursor: pointer;
  transition: border-color 0.2s;
  min-width: 130px;
}

.filter-group select:focus {
  outline: none;
  border-color: #42b983;
}

.search-group {
  flex: 1;
  min-width: 160px;
}

.search-group input {
  padding: 0.45rem 0.7rem;
  border: 1px solid #dce1e6;
  border-radius: 6px;
  font-size: 0.85rem;
  color: #2c3e50;
  background: #fafbfc;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.search-group input:focus {
  outline: none;
  border-color: #42b983;
}

.clear-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 0.45rem 0.8rem;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  align-self: flex-end;
}

.clear-btn:hover {
  background: #c0392b;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  .filter-bar {
    flex-direction: column;
    align-items: stretch;
  }
  .filter-group select {
    min-width: auto;
  }
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.card:hover {
  transform: translateY(-5px);
}

.card h3 {
  margin: 0 0 0.5rem 0;
  color: #7f8c8d;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card .value {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.card.highlight .value {
  color: #42b983;
}

.filter-summary {
  margin: 0;
  text-align: center;
  color: #95a5a6;
  font-size: 0.85rem;
  font-weight: 500;
}
</style>
