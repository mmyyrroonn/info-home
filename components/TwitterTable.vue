<script setup>
const { data, pending, error, refresh } = await useFetch(
  "https://info.myron-moshui.online/twitter/queryLastDaySummary"
);
const twitters = data.value.data.filter((obj) => obj.score != 0).map((twitter) => {
  return {...twitter, createAt: twitter.createAt.substring(0, 16)};
});
const columns = [
  {
    key: "score",
    label: "Score",
    sortable: true,
    class: "w-1/6"
  },
  {
    key: "linkToTweet",
    label: "Content",
    class: "w-auto"
  },
  {
    key: "createAt",
    label: "Time",
    sortable: true,
    class: "w-1/6"
  },
];

const page = ref(1);
const pageCount = 50;

const scores = [9,7,5,0];
const score = ref(5);

const filtered_twitter = computed(() => {
  const limitScore = score.value?score.value:0;
  return twitters.filter((twitter) => {
    return twitter.score > limitScore;
  });
});

const rows = computed(() => {
  return filtered_twitter.value.slice((page.value - 1) * pageCount, (page.value) * pageCount)
});
</script>

<template>
    <div class="flex place-content-center">
      <div>
        <div class="flex justify-between">
        <!-- <div class="left-component px-3 py-3.5 dark:border-gray-700">
          <UInput v-model="score" placeholder="Filter Score" />
        </div> -->
          <div class="left-component px-3 py-3.5 dark:border-gray-700">
              <USelect v-model="score" :options="scores" color="primary" />
          </div>
          <div class="right-component justify-end px-3 py-3.5 dark:border-gray-700">
              <UPagination v-model="page" :page-count="pageCount" :total="filtered_twitter.length" />
          </div>
        </div>
      <UTable :columns="columns" :rows="rows" :sort="{ column: 'score', direction: 'desc' }">
      <template #linkToTweet-data="{ row }">
        <a v-bind:href="row.linkToTweet">
          <div class="w-[100rem]">
            <p class="truncate ..."> {{row.text}} </p>
          </div>
        </a>
      </template>
      </UTable>
      </div>
    </div>

</template>