<script setup>
import { computed } from 'vue'

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
  }
})

// Helper to get the definition object for the current language preference
// The data structure has definitions inside each language object.
// We need to decide which "definition" to show.
// The requirement says "see the definition in the language that is clicked on top".
// This implies we show the definition text FROM the selected language's entry.
// E.g. if 'Chinese' is selected, we show `item.chinese.definitions[0].text`.

// However, the screenshot shows 3 columns for examples, but a single definition row?
// Actually, the screenshot shows:
// 1. Header: Time [shijian] | Time [jikan] | Time [sigan]
// 2. Definition: "有起点和终点的一段时间。" (Chinese definition)
//    And on the right, toggles [C] [J] [K].
//    So the definition row displays ONE definition at a time, toggleable.
// 3. Examples: 3 columns (Chinese, Japanese, Korean).

const currentDefinition = computed(() => {
  // Default to Chinese if not specified or fallback
  // The definitionLanguage prop controls this.
  // 'C' -> item.chinese
  // 'J' -> item.japanese
  // 'K' -> item.korean
  
  // Note: The data has an array of definitions. We'll assume we show the first one for now,
  // or we need to handle multiple definitions.
  // The screenshot shows "1. ...", "2. ...".
  // So the component might be rendering a SINGLE definition entry (one meaning), not the whole word entry?
  // Wait, the screenshot shows "1. ..." and "2. ...". These look like separate cards or separate sections within a card.
  // Let's assume the `item` prop passed here represents ONE meaning (one definition group).
  // BUT the JSON structure is hierarchical: Word -> Definitions.
  // If we want to match the screenshot, we might need to flatten the data or iterate over definitions.
  // Let's assume the parent component iterates over definitions and passes a "Merged Definition Object" 
  // OR this component handles the whole word and iterates definitions itself.
  // Screenshot shows "1. ..." then "2. ...". This suggests the Card is the WORD, and it lists definitions.
  
  return props.item
})

// We need a local state for the definition language if we want to toggle it per row?
// Or is it global? "language that is clicked on top" might mean global.
// But the screenshot has [C][J][K] buttons on the definition row.
// Let's make it controllable via prop but also emit events or have local override.
// For now, let's use a local state initialized from prop, or just use the prop if it's global.
// The user said "language that is clicked on top", maybe referring to the header?
// But the screenshot shows buttons on the definition line.
// Let's implement local toggle for the definition line.

import { ref, watch } from 'vue'
const localDefLang = ref(props.definitionLanguage || 'C')

watch(() => props.definitionLanguage, (newVal) => {
  localDefLang.value = newVal
})

const setLang = (lang) => {
  localDefLang.value = lang
}

const getDefinitionText = (defIndex) => {
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
    return defs[defIndex].text
  }
  return ''
}

const getExamples = (langCode, defIndex) => {
    const langKey = {
    'C': 'chinese',
    'J': 'japanese',
    'K': 'korean'
  }[langCode]
  
  const defs = props.item[langKey]?.definitions
  if (defs && defs[defIndex]) {
    return defs[defIndex].examples || []
  }
  return []
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
      <div class="definition-row">
        <div class="def-text">
          <span class="index">{{ index + 1 }}.</span>
          <span v-html="highlight(getDefinitionText(index))"></span>
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
          <div v-for="(ex, i) in getExamples('C', index)" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="highlight(ex)"></span>
          </div>
        </div>
        <div class="ex-col japanese">
          <div v-for="(ex, i) in getExamples('J', index)" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="highlight(ex)"></span>
          </div>
        </div>
        <div class="ex-col korean">
          <div v-for="(ex, i) in getExamples('K', index)" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="highlight(ex)"></span>
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
  background-color: var(--bg-chinese-light); /* Default to pinkish light? Or dynamic? */
  /* Screenshot shows pink background for definition row */
}

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
