<script setup>
import { ref } from 'vue'
import VocabList from './components/VocabList.vue'

const searchQuery = ref('')
const showChinese = ref(true)
const showJapanese = ref(true)
const showKorean = ref(true)
const showPinyin = ref(true)
const showFurigana = ref(true)
const showKoreanRomanization = ref(true) // Renamed for clarity if needed, but keeping prop name consistent
const showDepTree = ref(false)

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
        <label class="toggle">
          <input type="checkbox" v-model="showPinyin"> Pinyin
        </label>
        <label class="toggle">
          <input type="checkbox" v-model="showFurigana"> Furigana
        </label>
        <label class="toggle">
          <input type="checkbox" v-model="showKoreanRomanization"> Korean Rom.
        </label>
        <label class="toggle">
          <input type="checkbox" v-model="showDepTree"> DepTree
        </label>
        <!-- Global Language Toggles (Flags or Buttons) -->
        <button @click="showChinese = !showChinese" :class="{ active: showChinese }" title="Toggle Chinese">🇨🇳</button>
        <button @click="showJapanese = !showJapanese" :class="{ active: showJapanese }" title="Toggle Japanese">🇯🇵</button>
        <button @click="showKorean = !showKorean" :class="{ active: showKorean }" title="Toggle Korean">🇰🇷</button>
      </div>
    </header>

    <main>
      <div class="container">
        <VocabList 
          :search-query="searchQuery" 
          :show-chinese="showChinese"
          :show-japanese="showJapanese"
          :show-korean="showKorean"
          :show-pinyin="showPinyin"
          :show-furigana="showFurigana"
          :show-korean-romanization="showKoreanRomanization"
          :show-dep-tree="showDepTree"
        />
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

.header-controls {
  display: flex;
  align-items: center;
}

.toggles {
  display: flex;
  gap: 10px;
  margin-right: 20px;
  font-size: 0.9em;
}

.toggles label {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
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

@media (max-width: 768px) {
  .app-header {
    flex-direction: column;
    gap: 10px;
    padding: 10px;
  }

  .logo {
    margin-bottom: 5px;
  }

  .search-bar {
    width: 100%;
    margin: 0;
    max-width: none;
  }

  .header-controls {
    width: 100%;
    flex-wrap: wrap;
    justify-content: center;
    gap: 10px;
  }

  .toggles {
    margin-right: 0;
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
