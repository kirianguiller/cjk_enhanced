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
const showOptions = ref(false)

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
      <div class="toggles-group" :class="{ open: showOptions }">
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
      </div>
      <div class="flags-group">
        <button @click="showChinese = !showChinese" :class="{ active: showChinese }" title="Toggle Chinese">🇨🇳</button>
        <button @click="showJapanese = !showJapanese" :class="{ active: showJapanese }" title="Toggle Japanese">🇯🇵</button>
        <button @click="showKorean = !showKorean" :class="{ active: showKorean }" title="Toggle Korean">🇰🇷</button>
        <button class="options-toggle" @click="showOptions = !showOptions" :class="{ active: showOptions }" title="Toggle Options">⚙️</button>
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
  gap: 20px;
}

.logo {
  font-weight: bold;
  font-size: 1.2em;
  color: #e91e63; /* Pink logo text */
  white-space: nowrap;
}

.search-bar {
  flex: 1;
  max-width: 600px;
}

.search-bar input {
  width: 100%;
  padding: 8px 12px;
  border-radius: 4px;
  border: none;
  font-size: 1em;
}

.toggles-group {
  display: flex;
  gap: 10px;
}

.flags-group {
  display: flex;
  gap: 10px;
}

.toggles-group label {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
}

.flags-group button {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.flags-group button.active,
.flags-group button:hover {
  opacity: 1;
}

.options-toggle {
  display: none; /* Hidden on desktop */
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
}

.options-toggle.active,
.options-toggle:hover {
  opacity: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

@media (max-width: 768px) {
  .app-header {
    display: grid;
    grid-template-columns: 1fr auto;
    grid-template-rows: auto auto auto;
    grid-template-areas:
      "logo flags"
      "search search"
      "toggles toggles";
    gap: 10px;
    padding: 10px;
  }

  .logo {
    grid-area: logo;
    margin-bottom: 0;
    align-self: center;
  }

  .flags-group {
    grid-area: flags;
    justify-self: end;
    align-self: center;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .options-toggle {
    display: block; /* Visible on mobile */
  }

  .search-bar {
    grid-area: search;
    width: 100%;
    margin: 0;
    max-width: none;
  }

  .toggles-group {
    grid-area: toggles;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px 12px;
    display: none; /* Hidden by default on mobile */
    font-size: 0.85em; /* Smaller font size */
  }

  .toggles-group.open {
    display: flex; /* Visible when open */
  }
}
</style>
