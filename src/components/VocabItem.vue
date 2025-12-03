<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  definitionLanguage: {
    type: String,
    default: 'CJK' // 'CJK', 'C', 'J', 'K' - determines which definition text to show
  },
  searchQuery: {
    type: String,
    default: ''
  },
  showPinyin: {
    type: Boolean,
    default: true
  },
  showFurigana: {
    type: Boolean,
    default: true
  }
})



// We need a local state for the definition language if we want to toggle it per row?
// Or is it global? "language that is clicked on top" might mean global.
// But the screenshot has [C][J][K] buttons on the definition row.
// Let's make it controllable via prop but also emit events or have local override.
// For now, let's use a local state initialized from prop, or just use the prop if it's global.
// Let's implement local toggle for the definition line.

const localDefLang = ref(props.definitionLanguage || 'C')

watch(() => props.definitionLanguage, (newVal) => {
  localDefLang.value = newVal
})

const setLang = (lang) => {
  localDefLang.value = lang
}

const getDefinitionData = (defIndex) => {
  const langKey = {
    'C': 'chinese',
    'J': 'japanese',
    'K': 'korean'
  }[localDefLang.value]
  
  // We need to find the definition at defIndex for the selected language.
  // The data structure: item.chinese.definitions[defIndex]
  // We assume the definitions are aligned by index across languages?
  // The JSON structure has `definitions` array in each language.
  // They SHOULD be aligned (same meaning).
  // Let's assume they are.
  
  const defs = props.item[langKey]?.definitions
  if (defs && defs[defIndex]) {
    return defs[defIndex]
  }
  return null
}

const getExampleData = (langCode, defIndex, exIndex) => {
    const langKey = {
    'C': 'chinese',
    'J': 'japanese',
    'K': 'korean'
  }[langCode]
  
  const defs = props.item[langKey]?.definitions
  if (defs && defs[defIndex] && defs[defIndex].examples) {
    return defs[defIndex].examples[exIndex]
  }
  return null
}

const highlight = (text) => {
  if (!text) return ''
  if (!props.searchQuery) return text
  
  const query = props.searchQuery.trim()
  if (!query) return text

  // Escape special regex characters in query
  const safeQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  const regex = new RegExp(`(${safeQuery})`, 'gi')
  
  return text.replace(regex, '<span class="highlight">$1</span>')
}

const renderText = (dataObj, lang) => {
  if (!dataObj) return ''
  
  const showPronunciation = (lang === 'C' && props.showPinyin) || (lang === 'J' && props.showFurigana)
  
  if (!showPronunciation || !dataObj.transcription || !dataObj.transcription.segments) {
    return highlight(dataObj.text)
  }
  
  // Render segments with Ruby tags
  return dataObj.transcription.segments.map(seg => {
    const base = highlight(seg.base)
    if (seg.reading) {
      return `<ruby>${base}<rt>${seg.reading}</rt></ruby>`
    }
    return base
  }).join('')
}




</script>

<template>
  <div class="vocab-card">
    <!-- Header Row -->
    <div class="header-row">
      <div class="header-col chinese">
        <span class="word" v-html="highlight(item.chinese.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.chinese.romanization)"></span>】</span>
      </div>
      <div class="header-col japanese">
        <span class="word" v-html="highlight(item.japanese.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.japanese.pronunciation)"></span> <span v-html="highlight(item.japanese.romanization)"></span>】</span>
      </div>
      <div class="header-col korean">
        <span class="word" v-html="highlight(item.korean.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.korean.pronunciation)"></span> <span v-html="highlight(item.korean.romanization)"></span>】</span>
      </div>
    </div>

    <!-- Definitions Loop -->
    <div v-for="(def, index) in item.chinese.definitions" :key="index" class="definition-group">
      <!-- Definition Text Row -->
      <div class="definition-row" :class="['bg-' + localDefLang]">
        <div class="def-text">
          <span class="index">{{ index + 1 }}.</span>
          <span v-html="renderText(getDefinitionData(index), localDefLang)"></span>
        </div>
        <div class="lang-toggles">
          <button @click="setLang('C')" :class="{ active: localDefLang === 'C' }" class="btn-c">C</button>
          <button @click="setLang('J')" :class="{ active: localDefLang === 'J' }" class="btn-j">J</button>
          <button @click="setLang('K')" :class="{ active: localDefLang === 'K' }" class="btn-k">K</button>
        </div>
      </div>

      <!-- Examples Row -->
      <div class="examples-row">
        <div class="ex-col chinese">
          <div v-for="(ex, i) in getDefinitionData(index)?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('C', index, i), 'C')"></span>
          </div>
        </div>
        <div class="ex-col japanese">
          <div v-for="(ex, i) in getDefinitionData(index)?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('J', index, i), 'J')"></span>
          </div>
        </div>
        <div class="ex-col korean">
          <div v-for="(ex, i) in getDefinitionData(index)?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('K', index, i), 'K')"></span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vocab-card {
  background: white;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
}

.header-col {
  padding: 10px 15px;
  color: #333;
  font-weight: bold;
  font-size: 1.1em;
}

.header-col.chinese { background-color: var(--color-chinese); color: white; }
.header-col.japanese { background-color: var(--color-japanese); color: white; }
.header-col.korean { background-color: var(--color-korean); color: var(--color-korean-text); }

.definition-group {
  border-bottom: 1px solid #eee;
}

.definition-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  transition: background-color 0.3s ease;
}

.bg-C { background-color: var(--bg-chinese-light); }
.bg-J { background-color: var(--bg-japanese-light); }
.bg-K { background-color: var(--bg-korean-light); }

.def-text {
  font-size: 1.1em;
}

.lang-toggles button {
  border: none;
  padding: 5px 10px;
  margin-left: 5px;
  cursor: pointer;
  font-weight: bold;
  color: white;
}

.btn-c { background-color: #ccc; }
.btn-c.active { background-color: var(--color-chinese); }
.btn-j { background-color: #ccc; }
.btn-j.active { background-color: var(--color-japanese); }
.btn-k { background-color: #ccc; }
.btn-k.active { background-color: var(--color-korean); color: black; }

.examples-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 10px 0;
}

.ex-col {
  padding: 0 15px;
  border-right: 1px dotted #ccc;
}
.ex-col:last-child { border-right: none; }

.example {
  margin-bottom: 5px;
  font-size: 0.95em;
  color: #555;
}

:deep(.highlight) {
  background-color: #00e676; /* Brighter green */
  color: #000; /* Black text for better contrast */
  font-weight: bold;
  border-radius: 4px;
  padding: 0 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
</style>
