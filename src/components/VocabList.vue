<script setup>
import { computed } from 'vue'
import VocabItem from './VocabItem.vue'
import vocabData from '../assets/tcdv.json'

const props = defineProps({
  searchQuery: {
    type: String,
    default: ''
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

const filteredList = computed(() => {
  const query = props.searchQuery.toLowerCase().trim()
  if (!query) return vocabData

  return vocabData.filter(item => {
    // Search in Words
    const words = [
      item.chinese.word, item.chinese.romanization,
      item.japanese.word, item.japanese.pronunciation, item.japanese.romanization,
      item.korean.word, item.korean.pronunciation, item.korean.romanization
    ].join(' ').toLowerCase()

    if (words.includes(query)) return true

    // Search in Definitions (all languages)
    // We need to check all definitions in all languages
    const checkDefs = (langObj) => {
      return langObj.definitions.some(def => 
        def.text.toLowerCase().includes(query) ||
        (def.examples && def.examples.some(ex => ex.text.toLowerCase().includes(query)))
      )
    }

    if (checkDefs(item.chinese)) return true
    if (checkDefs(item.japanese)) return true
    if (checkDefs(item.korean)) return true

    return false
  })
})
</script>

<template>
  <div class="vocab-list">
    <VocabItem 
      v-for="item in filteredList" 
      :key="item.rank" 
      :item="item"
      :show-chinese="showChinese"
      :show-japanese="showJapanese"
      :show-korean="showKorean"
      :search-query="searchQuery"
      :show-pinyin="showPinyin"
      :show-furigana="showFurigana"
      :show-korean-romanization="showKoreanRomanization"
      :show-dep-tree="showDepTree"
    />
    <div v-if="filteredList.length === 0" class="no-results">
      No results found for "{{ searchQuery }}"
    </div>
  </div>
</template>

<style scoped>
.vocab-list {
  padding: 20px 0;
}
.no-results {
  text-align: center;
  color: #888;
  margin-top: 40px;
}
</style>
