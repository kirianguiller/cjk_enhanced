<script setup>
defineProps({
  conll: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="dep-tree-container">
    <reactive-dep-tree 
      :conll="conll" 
      interactive="false"
      shown-features="UPOS,LEMMA,FORM,DEPREL"
      arc-height="40"
      token-spacing="20"
    ></reactive-dep-tree>
  </div>
</template>

<style scoped>
.dep-tree-container {
  margin-top: 10px;
  overflow-x: auto;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 4px;
}
</style>
