<script setup>
defineProps({
  ads: {
    type: Array,
    required: true
  }
})

const getScoreClass = (score) => {
  if (score >= 8) return 'score-high'
  if (score >= 5) return 'score-medium'
  return 'score-low'
}
</script>

<template>
  <div class="table-container">
    <h2>Campaign Performance</h2>
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Project Name</th>
            <th>Source</th>
            <th>Clicks</th>
            <th>Cost</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ad in ads" :key="ad.id">
            <td>{{ ad.project_id }}</td>
            <td>
              <div class="project-info">
                <span class="name">{{ ad.project_name }}</span>
                <a v-if="ad.source_url" :href="ad.source_url" target="_blank" class="link">Link</a>
              </div>
            </td>
            <td><span class="badge">{{ ad.source }}</span></td>
            <td>{{ ad.click_count }}</td>
            <td>${{ ad.cost.toFixed(2) }}</td>
            <td>
              <span :class="['score-badge', getScoreClass(ad.score)]">
                {{ ad.score.toFixed(1) }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.table-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  font-size: 1.25rem;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 1rem;
  background-color: #f8f9fa;
  color: #7f8c8d;
  font-weight: 600;
  border-bottom: 2px solid #e9ecef;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
  color: #2c3e50;
}

tr:hover td {
  background-color: #f8f9fa;
}

.project-info {
  display: flex;
  flex-direction: column;
}

.link {
  font-size: 0.8rem;
  color: #3498db;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.badge {
  background-color: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #495057;
}

.score-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-weight: 700;
  font-size: 0.9rem;
}

.score-high {
  background-color: #d4edda;
  color: #155724;
}

.score-medium {
  background-color: #fff3cd;
  color: #856404;
}

.score-low {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
