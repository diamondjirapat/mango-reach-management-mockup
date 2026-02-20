<script setup>
import { ref, reactive } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'ad-created'])

const submitting = ref(false)
const errorMsg = ref('')

const form = reactive({
  project_name: '',
  project_id: '',
  source: 'Facebook',
  source_url: '',
  type: 'online',
  click_count: 0,
  cost: 0
})

const sources = ['Facebook', 'X', 'Instagram', 'Google', 'TikTok', 'Flyers', 'Billboard']

const handleSubmit = async () => {
  if (!form.project_name.trim() || !form.project_id.trim()) {
    errorMsg.value = 'Project Name and Project ID are required.'
    return
  }
  submitting.value = true
  errorMsg.value = ''
  try {
    await api.createAd({
      project_name: form.project_name.trim(),
      project_id: form.project_id.trim(),
      source: form.source,
      source_url: form.source_url.trim() || null,
      type: form.type,
      click_count: Number(form.click_count),
      cost: Number(form.cost)
    })
    emit('ad-created')
    emit('close')
  } catch (e) {
    errorMsg.value = 'Failed to create ad. Please try again.'
    console.error(e)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="modal-header">
        <h2>Add New Ad</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-row">
          <div class="form-group">
            <label for="project_name">Project Name *</label>
            <input id="project_name" v-model="form.project_name" type="text" placeholder="e.g. New Condo" required />
          </div>
          <div class="form-group">
            <label for="project_id">Project ID *</label>
            <input id="project_id" v-model="form.project_id" type="text" placeholder="e.g. PRJ-001" required />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="source">Source</label>
            <select id="source" v-model="form.source">
              <option v-for="s in sources" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="type">Type</label>
            <select id="type" v-model="form.type">
              <option value="online">Online</option>
              <option value="offline">Offline</option>
            </select>
          </div>
        </div>

        <div class="form-group full-width">
          <label for="source_url">Source URL <span class="optional">(optional)</span></label>
          <input id="source_url" v-model="form.source_url" type="url" placeholder="https://..." />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="click_count">Click Count</label>
            <input id="click_count" v-model.number="form.click_count" type="number" min="0" />
          </div>
          <div class="form-group">
            <label for="cost">Cost ($)</label>
            <input id="cost" v-model.number="form.cost" type="number" min="0" step="0.01" />
          </div>
        </div>

        <p class="score-note">
          <span class="note-icon">ℹ️</span>
          Score will be calculated automatically based on clicks, cost, and source.
        </p>

        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <div class="modal-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')">Cancel</button>
          <button type="submit" class="submit-btn" :disabled="submitting">
            {{ submitting ? 'Saving...' : 'Save Ad' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.25s ease;
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.6rem;
  color: #7f8c8d;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #2c3e50;
}

.modal-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #4d5b67;
}

.optional {
  font-weight: 400;
  color: #95a5a6;
}

input, select {
  padding: 0.55rem 0.75rem;
  border: 1px solid #dce1e6;
  border-radius: 6px;
  font-size: 0.9rem;
  color: #2c3e50;
  background: #fafbfc;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus, select:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 3px rgba(66, 185, 131, 0.15);
}

.score-note {
  background: #eef9f3;
  border: 1px solid #c3e6d5;
  border-radius: 6px;
  padding: 0.6rem 0.85rem;
  font-size: 0.82rem;
  color: #2c6e49;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.note-icon {
  font-size: 0.95rem;
}

.error-msg {
  color: #e74c3c;
  font-size: 0.85rem;
  margin: 0;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
  padding-top: 0.5rem;
  border-top: 1px solid #e9ecef;
}

.cancel-btn {
  background: #e9ecef;
  color: #495057;
  border: none;
  padding: 0.55rem 1.1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.cancel-btn:hover {
  background: #dee2e6;
}

.submit-btn {
  background: #42b983;
  color: white;
  border: none;
  padding: 0.55rem 1.3rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #3aa876;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 540px) {
  .modal-card {
    margin: 1rem;
  }
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>
