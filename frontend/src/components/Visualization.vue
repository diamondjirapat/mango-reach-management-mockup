<script setup>
import { computed, ref } from 'vue'

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
  },
  ads: {
    type: Array,
    required: true,
    default: () => []
  }
})

const selectedSource = ref(null)
const selectedScoreBucket = ref(null)
const selectedChannel = ref(null)

const channelGroups = {
  offline: ['Billboard', 'Flyers', 'Unknown'],
  online: ['TikTok', 'Facebook', 'X', 'Instagram', 'Google']
}

const channelLabels = {
  online: 'Online',
  offline: 'Offline'
}

const toPercent = (value, total) => {
  if (!total) return 0
  return (value / total) * 100
}

const formatPercent = (value) => `${value.toFixed(1)}%`

const matchesScoreBucket = (ad, bucket) => {
  const score = ad.score || 0
  if (bucket === 'high') return score >= 8
  if (bucket === 'medium') return score >= 5 && score < 8
  if (bucket === 'low') return score < 5
  return true
}

const filteredAds = computed(() => {
  return (props.ads || []).filter((ad) => {
    const matchesSource = !selectedSource.value || ad.source === selectedSource.value
    const matchesScore = !selectedScoreBucket.value || matchesScoreBucket(ad, selectedScoreBucket.value)
    const source = ad.source || 'Unknown'
    const matchesChannel = !selectedChannel.value || channelGroups[selectedChannel.value].includes(source)
    return matchesSource && matchesScore && matchesChannel
  })
})

const topSources = computed(() => {
  const bySource = {}
  for (const ad of filteredAds.value) {
    const source = ad.source || 'Unknown'
    bySource[source] = (bySource[source] || 0) + (ad.click_count || 0)
  }

  const rows = Object.entries(bySource)
    .map(([source, clicks]) => ({ source, clicks }))
    .sort((a, b) => b.clicks - a.clicks)

  const totalClicks = rows.reduce((sum, row) => sum + row.clicks, 0)
  return rows.map((row) => ({
    ...row,
    percentage: toPercent(row.clicks, totalClicks),
    width: toPercent(row.clicks, totalClicks)
  }))
})

const scoreBreakdown = computed(() => {
  const result = { high: 0, medium: 0, low: 0 }
  for (const ad of filteredAds.value) {
    const score = ad.score || 0
    if (score >= 8) result.high += 1
    else if (score >= 5) result.medium += 1
    else result.low += 1
  }
  const total = filteredAds.value.length
  return {
    high: toPercent(result.high, total),
    medium: toPercent(result.medium, total),
    low: toPercent(result.low, total)
  }
})

const channelBreakdown = computed(() => {
  const totals = { offline: 0, online: 0 }
  const baseAds = (props.ads || []).filter((ad) => {
    const matchesSource = !selectedSource.value || ad.source === selectedSource.value
    const matchesScore = !selectedScoreBucket.value || matchesScoreBucket(ad, selectedScoreBucket.value)
    return matchesSource && matchesScore
  })

  for (const ad of baseAds) {
    const source = ad.source || 'Unknown'
    const clicks = ad.click_count || 0

    if (channelGroups.offline.includes(source)) {
      totals.offline += clicks
      continue
    }

    if (channelGroups.online.includes(source)) {
      totals.online += clicks
    }
  }

  const totalClicks = totals.offline + totals.online
  return [
    {
      key: 'online',
      channel: 'Online',
      clicks: totals.online,
      percentage: toPercent(totals.online, totalClicks),
      width: toPercent(totals.online, totalClicks)
    },
    {
      key: 'offline',
      channel: 'Offline',
      clicks: totals.offline,
      percentage: toPercent(totals.offline, totalClicks),
      width: toPercent(totals.offline, totalClicks)
    }
  ]
})

const filteredClicks = computed(() => {
  return filteredAds.value.reduce((sum, ad) => sum + (ad.click_count || 0), 0)
})

const totalProjectsShare = computed(() => {
  return toPercent(filteredAds.value.length, (props.ads || []).length)
})

const totalClicksShare = computed(() => {
  const allClicks = (props.ads || []).reduce((sum, ad) => sum + (ad.click_count || 0), 0)
  return toPercent(filteredClicks.value, allClicks)
})

const toggleSource = (source) => {
  selectedSource.value = selectedSource.value === source ? null : source
}

const toggleScoreBucket = (bucket) => {
  selectedScoreBucket.value = selectedScoreBucket.value === bucket ? null : bucket
}

const toggleChannel = (channel) => {
  selectedChannel.value = selectedChannel.value === channel ? null : channel
  selectedSource.value = null
}

const clearFilters = () => {
  selectedSource.value = null
  selectedScoreBucket.value = null
  selectedChannel.value = null
}
</script>

<template>
  <section class="viz-page">
    <div class="panel">
      <h2>Click Distribution By Source</h2>
      <div class="toolbar">
        <button class="clear-btn" @click="clearFilters">Clear Filters</button>
      </div>
      <div v-if="topSources.length === 0" class="empty">No data available.</div>
      <div v-else class="bars">
        <button
          v-for="item in topSources"
          :key="item.source"
          class="bar-row"
          :class="{ active: selectedSource === item.source }"
          @click="toggleSource(item.source)"
        >
          <div class="label">{{ item.source }}</div>
          <div class="track">
            <div class="fill" :style="{ width: `${item.width}%` }"></div>
            <span class="bar-number">{{ item.clicks }}</span>
          </div>
          <div class="value">{{ formatPercent(item.percentage) }}</div>
        </button>
      </div>
    </div>

    <div class="panel">
      <h2>Online vs Offline</h2>
      <div class="bars">
        <button
          v-for="item in channelBreakdown"
          :key="item.channel"
          class="bar-row channel-row"
          :class="{ active: selectedChannel === item.key }"
          @click="toggleChannel(item.key)"
        >
          <div class="label">{{ item.channel }}</div>
          <div class="track">
            <div class="fill channel-fill" :style="{ width: `${item.width}%` }"></div>
            <span class="bar-number">{{ item.clicks }}</span>
          </div>
          <div class="value">{{ formatPercent(item.percentage) }}</div>
        </button>
      </div>
      <p v-if="selectedChannel" class="summary">Active channel filter: {{ channelLabels[selectedChannel] }}</p>
      <p class="summary">Offline: Billboard, Flyers, Unknown | Online: TikTok, Facebook, X, Instagram, Google</p>
    </div>

    <div class="panel">
      <h2>Score Breakdown</h2>
      <div class="score-grid">
        <button
          class="score-card high"
          :class="{ active: selectedScoreBucket === 'high' }"
          @click="toggleScoreBucket('high')"
        >
          <p class="title">High (8-10)</p>
          <p class="num">{{ formatPercent(scoreBreakdown.high) }}</p>
        </button>
        <button
          class="score-card medium"
          :class="{ active: selectedScoreBucket === 'medium' }"
          @click="toggleScoreBucket('medium')"
        >
          <p class="title">Medium (5-7.9)</p>
          <p class="num">{{ formatPercent(scoreBreakdown.medium) }}</p>
        </button>
        <button
          class="score-card low"
          :class="{ active: selectedScoreBucket === 'low' }"
          @click="toggleScoreBucket('low')"
        >
          <p class="title">Low (&lt;5)</p>
          <p class="num">{{ formatPercent(scoreBreakdown.low) }}</p>
        </button>
      </div>
      <p class="summary">
        Total Projects: {{ formatPercent(totalProjectsShare) }} | Total Clicks:
        {{ formatPercent(totalClicksShare) }}
      </p>
    </div>
  </section>
</template>

<style scoped>
.viz-page {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

.panel {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 1.25rem;
}

h2 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 0.75rem;
}

.clear-btn {
  background: #4e5d6c;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 0.35rem 0.7rem;
  cursor: pointer;
  font-weight: 600;
}

.empty {
  color: #6c757d;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.bar-row {
  display: grid;
  grid-template-columns: 140px 1fr 70px;
  align-items: center;
  gap: 0.6rem;
  border: 1px solid transparent;
  background: #fff;
  border-radius: 8px;
  padding: 0.4rem;
  cursor: pointer;
  text-align: left;
}

.bar-row.active {
  border-color: #2c3e50;
  background: #f5f7fa;
}

.bar-row.channel-row {
  cursor: pointer;
}

.label {
  color: #34495e;
  font-weight: 600;
}

.track {
  position: relative;
  height: 22px;
  border-radius: 999px;
  background: #e9ecef;
  overflow: hidden;
}

.fill {
  height: 100%;
  background: #42b983;
}

.channel-fill {
  background: #42b983;
}

.bar-number {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  font-size: 0.75rem;
  font-weight: 700;
  color: #1f2d3a;
  pointer-events: none;
  z-index: 1;
}

.value {
  text-align: right;
  color: #2c3e50;
  font-weight: 700;
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.8rem;
}

.score-card {
  border-radius: 8px;
  padding: 0.9rem;
  border: 2px solid transparent;
  text-align: left;
  cursor: pointer;
}

.score-card.active {
  border-color: #2c3e50;
}

.title {
  margin: 0;
  font-size: 0.85rem;
  color: #4d5b67;
}

.num {
  margin: 0.45rem 0 0 0;
  font-size: 1.6rem;
  font-weight: 700;
}

.high {
  background: #8fb59a;
  color: #12301d;
}

.medium {
  background: #cdbb7a;
  color: #3f2e00;
}

.low {
  background: #bf8d93;
  color: #3f141a;
}

.summary {
  margin: 1rem 0 0 0;
  color: #2c3e50;
  font-weight: 600;
}

@media (max-width: 768px) {
  .bar-row {
    grid-template-columns: 100px 1fr 60px;
  }

  .score-grid {
    grid-template-columns: 1fr;
  }
}
</style>
