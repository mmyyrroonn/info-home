<script setup>
const { data, pending, error, refresh } = await useFetch(
  "https://info.myron-moshui.online/twitter/queryLastDaySummary"
);
const twitters = data.value.data.filter((obj) => obj.score != 0).map((twitter) => {
  return {...twitter, createAt: new Date(twitter.createAt.substring(0, 16))};
});
const columns = [
  {
    key: "score",
    label: "Score",
    sortable: true,
  },
  {
    key: "linkToTweet",
    label: "Content",
  },
  {
    key: "createAt",
    label: "Time",
    sortable: true,
  },
];

const page = ref(1);
const pageCount = 50;

const scores = [9,8,7,5,0];
const score = ref(7);

const dates = [1, 6, 12, 24, 48];
const date = ref(24);

var sort = ref({
  prop: 'createAt',
  order: 'descending'
});

function updateSortData(data)
{
  console.log(data);
  sort.value.prop = data.prop;
  sort.value.order = data.order;
};

const sortFunctions = {
  score: {
    ascending: (a, b) => a.score - b.score,
    descending: (a, b) => b.score - a.score
  },
  createAt: {
    ascending: (a, b) => a.createAt - b.createAt,
    descending: (a, b) => b.createAt - a.createAt
  }
};

const filtered_twitter = computed(() => {
  const limitScore = score.value?score.value:0;
  const limitDate = new Date(Date.now() - (date.value?date.value:48) * 60 * 60 * 1000);
  return twitters.filter((twitter) => {
    return twitter.score > limitScore && twitter.createAt > limitDate;
  }).sort(sortFunctions[sort.value.prop][sort.value.order]);
});

const dateFormat = { hour: 'numeric', month: 'numeric', day: 'numeric', minute: 'numeric' };
const formatDate = (twitter) => {
  return {...twitter, createAt: twitter.createAt.toLocaleString('en-US', dateFormat)}
}

const rows = computed(() => {
  return filtered_twitter.value.slice((page.value - 1) * pageCount, (page.value) * pageCount).map(formatDate);
});

const contentWidth = computed(() => {
  return parseInt((window.innerWidth - 290));
  // return "500";
})
</script>

<template>
    <div class="flex">
      <div>
        <div class="flex justify-between">
          <div class="flex left-component">
            <span class="flex items-center py-3.5">显示AI分析得分高于</span>
            <div class="py-3.5 dark:border-gray-700">
              <USelect v-model="score" :options="scores" color="primary" />
            </div>
            <span class="flex items-center py-3.5">分且处于过去</span>
            <div class="py-3.5 dark:border-gray-700">
              <USelect v-model="date" :options="dates" color="primary" />
            </div>
            <span class="flex items-center py-3.5">小时之内的推文</span>
          </div>
          <div class="right-component justify-end px-3 py-3.5 dark:border-gray-700">
              <UPagination v-model="page" :page-count="pageCount" :total="filtered_twitter.length" />
          </div>
        </div>
      <!-- <UTable v-model:sort="sort" :columns="columns" :rows="rows">
      <template #linkToTweet-data="{ row }">
        <a v-bind:href="row.linkToTweet">
          <div class="w-[101rem]">
            <p class="flex truncate ..."> {{row.text}} </p>
          </div>
        </a>
      </template>
      </UTable> -->

      <el-table fit :data="rows" @sort-change="updateSortData">
        <el-table-column prop="score" label="Score" width="110" sortable="custom"></el-table-column>
        <el-table-column prop="text" label="Content" :width="contentWidth">
          <template v-slot:default="table">
            <a v-bind:href="table.row.linkToTweet">
              <p class="whitespace-nowrap truncate ..."> {{table.row.text}} </p>
            </a>
         </template>
        </el-table-column>
        <el-table-column prop="createAt" label="Time" width="150" sortable="custom"></el-table-column>
      </el-table>
      </div>
    </div>

</template>