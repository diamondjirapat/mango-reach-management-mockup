<script setup>
import { computed } from 'vue'

const props = defineProps({
  stats: {
    type: Object,
    required: true,
    default: () => ({
      total_projects: 0,
      total_clicks: 0,
      total_cost: 0,
      average_score: 0
    })
  }
})

const formattedCost = computed(() => {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(props.stats?.total_cost || 0)
})

const formattedScore = computed(() => {
  return (props.stats?.average_score || 0).toFixed(2)
})
</script>

<template>
  <div class="dashboard-grid">
    <div class="card">
      <h3>Total Projects</h3>
      <p class="value">{{ stats?.total_projects || 0 }}</p>
    </div>
    <div class="card">
      <h3>Total Clicks</h3>
      <p class="value">{{ stats?.total_clicks || 0 }}</p>
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
</template>

<style scoped>
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
}

.card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s;
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
</style>
