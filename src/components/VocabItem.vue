<script setup>
import { ref, computed } from 'vue'
import DepTree from './DepTree.vue'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  showChinese: {
    type: Boolean,
    default: true
  },
  showJapanese: {
    type: Boolean,
    default: true
  },
  showKorean: {
    type: Boolean,
    default: true
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
  },
  showKoreanRomanization: {
    type: Boolean,
    default: true
  },
  showDepTree: {
    type: Boolean,
    default: false
  }
})

const hoveredTree = ref(null)

const gridStyle = computed(() => {
  const count = (props.showChinese ? 1 : 0) + (props.showJapanese ? 1 : 0) + (props.showKorean ? 1 : 0)
  if (count === 0) return { display: 'none' }
  return {
    display: 'grid',
    gridTemplateColumns: `repeat(${count}, 1fr)`
  }
})

const getDefinitionData = (defIndex, langCode) => {
  const langKey = {
    'C': 'chinese',
    'J': 'japanese',
    'K': 'korean'
  }[langCode]
  
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
  
  const showPronunciation = (lang === 'C' && props.showPinyin) || 
                            (lang === 'J' && props.showFurigana) ||
                            (lang === 'K' && props.showKoreanRomanization)
  
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
    <div class="header-row" :style="gridStyle">
      <div v-if="showChinese" class="header-col chinese">
        <span class="word" v-html="highlight(item.chinese.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.chinese.romanization)"></span>】</span>
      </div>
      <div v-if="showJapanese" class="header-col japanese">
        <span class="word" v-html="highlight(item.japanese.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.japanese.pronunciation)"></span> <span v-html="highlight(item.japanese.romanization)"></span>】</span>
      </div>
      <div v-if="showKorean" class="header-col korean">
        <span class="word" v-html="highlight(item.korean.word)"></span>
        <span class="romanization">【<span v-html="highlight(item.korean.pronunciation)"></span> <span v-html="highlight(item.korean.romanization)"></span>】</span>
      </div>
    </div>

    <!-- Definitions Loop -->
    <div v-for="(def, index) in item.chinese.definitions" :key="index" class="definition-group">
      <!-- Definition Text Row -->
      <div class="definition-row" :style="gridStyle">
        <div v-if="showChinese" class="def-col chinese bg-C">
          <span class="index">{{ index + 1 }}.</span>
          <span v-html="renderText(getDefinitionData(index, 'C'), 'C')"></span>
        </div>
        <div v-if="showJapanese" class="def-col japanese bg-J">
           <span class="index">①</span>
           <span v-html="renderText(getDefinitionData(index, 'J'), 'J')"></span>
        </div>
        <div v-if="showKorean" class="def-col korean bg-K">
           <span class="index">①</span>
           <span v-html="renderText(getDefinitionData(index, 'K'), 'K')"></span>
        </div>
      </div>

      <!-- Examples Row -->
      <div class="examples-row" :style="gridStyle">
        <div v-if="showChinese" class="ex-col chinese">
          <div v-for="(ex, i) in getDefinitionData(index, 'C')?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('C', index, i), 'C')"></span>
            
            <!-- Tree Icon & Tooltip -->
            <div v-if="showDepTree && getExampleData('C', index, i)?.conllu" class="tree-trigger"
                 @mouseenter="hoveredTree = `C-${index}-${i}`"
                 @mouseleave="hoveredTree = null">
              <span class="tree-icon">🌳</span>
              <div v-if="hoveredTree === `C-${index}-${i}`" class="tree-tooltip">
                <DepTree :conll="getExampleData('C', index, i).conllu" />
              </div>
            </div>
          </div>
        </div>
        <div v-if="showJapanese" class="ex-col japanese">
          <div v-for="(ex, i) in getDefinitionData(index, 'C')?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('J', index, i), 'J')"></span>
            
            <!-- Tree Icon & Tooltip -->
            <div v-if="showDepTree && getExampleData('J', index, i)?.conllu" class="tree-trigger"
                 @mouseenter="hoveredTree = `J-${index}-${i}`"
                 @mouseleave="hoveredTree = null">
              <span class="tree-icon">🌳</span>
              <div v-if="hoveredTree === `J-${index}-${i}`" class="tree-tooltip">
                <DepTree :conll="getExampleData('J', index, i).conllu" />
              </div>
            </div>
          </div>
        </div>
        <div v-if="showKorean" class="ex-col korean">
          <div v-for="(ex, i) in getDefinitionData(index, 'C')?.examples" :key="i" class="example">
            <span class="ex-index">①</span> <span v-html="renderText(getExampleData('K', index, i), 'K')"></span>
            
            <!-- Tree Icon & Tooltip -->
            <div v-if="showDepTree && getExampleData('K', index, i)?.conllu" class="tree-trigger"
                 @mouseenter="hoveredTree = `K-${index}-${i}`"
                 @mouseleave="hoveredTree = null">
              <span class="tree-icon">🌳</span>
              <div v-if="hoveredTree === `K-${index}-${i}`" class="tree-tooltip">
                <DepTree :conll="getExampleData('K', index, i).conllu" />
              </div>
            </div>
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

/* Grid styles are now handled dynamically via :style binding */
/* .header-row, .definition-row, .examples-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
} */

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

/* .definition-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
} */

.def-col {
  padding: 10px 15px;
  font-size: 1.1em;
}

.bg-C { background-color: var(--bg-chinese-light); }
.bg-J { background-color: var(--bg-japanese-light); }
.bg-K { background-color: var(--bg-korean-light); }


/* .examples-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 10px 0;
} */
.examples-row {
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

.index {
  font-weight: bold;
  margin-right: 5px;
}

:deep(.highlight) {
  background-color: #00e676; /* Brighter green */
  color: #000; /* Black text for better contrast */
  font-weight: bold;
  border-radius: 4px;
  padding: 0 4px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

ruby {
  ruby-position: over;
}

rt {
  font-size: 0.6em;
  color: #666;
}

.tree-trigger {
  display: inline-block;
  position: relative;
  margin-left: 5px;
  cursor: pointer;
}

.tree-icon {
  font-size: 1.2em;
}

.tree-tooltip {
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  z-index: 1000;
  width: 400px; /* Adjust as needed */
  max-width: 90vw;
  overflow-x: auto;
}
</style>
