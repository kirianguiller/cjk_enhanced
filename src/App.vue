<script setup>
import { ref } from 'vue'
import VocabList from './components/VocabList.vue'

const searchQuery = ref('')
const globalDefLang = ref('C') // Default to Chinese definitions

const setGlobalLang = (lang) => {
  globalDefLang.value = lang
}
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <div class="logo">808CJK</div>
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search here..."
        />
      </div>
      <div class="header-controls">
        <!-- Global Language Toggles (Flags or Buttons) -->
        <!-- Screenshot shows flags on the right: China, Japan, Korea -->
        <button @click="setGlobalLang('C')" :class="{ active: globalDefLang === 'C' }" title="Chinese Definitions">🇨🇳</button>
        <button @click="setGlobalLang('J')" :class="{ active: globalDefLang === 'J' }" title="Japanese Definitions">🇯🇵</button>
        <button @click="setGlobalLang('K')" :class="{ active: globalDefLang === 'K' }" title="Korean Definitions">🇰🇷</button>
      </div>
    </header>

    <main>
      <div class="container">
        <VocabList :search-query="searchQuery" :global-def-lang="globalDefLang" />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #333;
  color: white;
  padding: 10px 20px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo {
  font-weight: bold;
  font-size: 1.2em;
  color: #e91e63; /* Pink logo text */
}

.search-bar {
  flex: 1;
  max-width: 600px;
  margin: 0 20px;
}

.search-bar input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 4px;
  border: none;
  font-size: 1em;
}

.header-controls button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
  margin-left: 10px;
}

.header-controls button.active,
.header-controls button:hover {
  opacity: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
</style>
