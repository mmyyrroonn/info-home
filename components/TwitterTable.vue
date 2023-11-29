<script setup>
const { data, pending, error, refresh } = await useFetch('https://info.myron-moshui.online/twitter/queryLastDaySummary');
const twitters = data.value.data.filter(obj => obj.score != 0);
const columns = [{
  key: 'score',
  label: 'Score',
  sortable: true,
},
{
  key: 'linkToTweet',
  label: 'Content'
}]

const page = ref(1)
const pageCount = 50

const rows = computed(() => {
  return twitters.slice((page.value - 1) * pageCount, (page.value) * pageCount)
})
</script>

<template>
    <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
        <UPagination v-model="page" :page-count="pageCount" :total="twitters.length" />
    </div>
    <UTable :columns="columns" :rows="rows" :sort="{ column: 'score', direction: 'desc' }">
    <template #linkToTweet-data="{ row }">
        <a v-bind:href="row.linkToTweet"> {{row.text}} </a>
    </template>
    </UTable>
</template>