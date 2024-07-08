<script setup>
const page = ref(1);
const pageCount = 50;

const scores = [9,8,7,5,0];
const score = ref(0);

const dates = [1, 6, 12, 24, 48, 96];
const date = ref(96);

const query_text = ref('')
const twitters = ref([]);
const quering = ref(false);

var sort = ref({
  prop: 'createAt',
  order: 'descending'
});

function updateSortData(data)
{
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
  return twitters.value.filter((twitter) => {
    return twitter.score >= limitScore && twitter.createAt >= limitDate;
  }).sort(sortFunctions[sort.value.prop][sort.value.order]);
});

const dateFormat = { hour: 'numeric', month: 'numeric', day: 'numeric', minute: 'numeric', hour12: false };
const formatDate = (twitter) => {
  return {...twitter, createAt: twitter.createAt.toLocaleString('en-US', dateFormat)}
}

const rows = computed(() => {
  return filtered_twitter.value.slice((page.value - 1) * pageCount, (page.value) * pageCount).map(formatDate);
});

watch(page, (newValue, oldValue) => {
    if (newValue !== oldValue) {
      // 当 page.value 改变时，滚动到页面顶部
      window.scrollTo(0, 0);
    }
});

const columnsWidth = computed(() => {
  const innerWidth = window.innerWidth;
  if(isPhone.value) {
    return { score: 70, text: parseInt((innerWidth - 60)), createAt: 60};
  }
  return { score: 110, text: parseInt((innerWidth - 110)), createAt: 110};
});

const contentClass = computed(() => {
    return isPhone.value?"":"whitespace-nowrap truncate ...";
});

const isPhone = ref(false);
onMounted(() => {
  if(window.innerWidth<600) {
    console.log("The device is phone")
    isPhone.value = true;
  }
})

async function queryTwitter() {
  quering.value = true;
  const { data, pending, error, refresh } = await useFetch(
      `https://info.myron-moshui.online/twitter/queryRelatedTwitter`,
      {
        method: "POST",
        body: {
          query_text: query_text.value,
          limit: 100
        }
      });
  // 处理得到的数据
  if (data.value && data.value.data) {
    twitters.value = data.value.data.map((twitter) => {
      return {
        ...twitter,
        createAt: new Date(twitter.createAt.substring(0, 16)),
        linkToTweet: "https://twitter.com/" + twitter.userName + "/status/" + twitter.tweetId
      };
    });
  }
  quering.value = false;
  // console.log("Twitters: ", twitters);
}

function searchAirdrop() {
  // 模拟搜索空投的逻辑
  query_text.value = '空投 融资 作业 交互 撸毛';
  queryTwitter();
}

function checkBitcoin() {
  // 模拟搜索大饼走势的逻辑
  query_text.value = '大饼走势 以太坊走势';
  queryTwitter();
}
</script>

<template>
    <div class="flex">
      <div>
        <div class="">
      <div class="w-full mx-auto">
        <el-form @submit.native.prevent="queryTwitter">
          <div class="flex flex-col">
            <el-form-item>
              <el-input v-model="query_text" placeholder="搜索你想了解的币圈推特, 例如空投, 大饼走势"></el-input>
            </el-form-item>
            <div class="flex justify-start">
              <button @click="searchAirdrop" class="px-4 py-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 focus:outline-none focus:bg-blue-600">
                空投交互
              </button>
              <button @click="checkBitcoin" class="px-4 py-2 rounded-full bg-green-500 text-white hover:bg-green-600 focus:outline-none focus:bg-green-600">
                币价走势
              </button>
            </div>
            <div class="flex justify-end">
            <el-form-item>
              <el-button type="primary" native-type="submit" :loading="quering">
                {{ quering ? '搜索中...' : '确认' }}
              </el-button>
            </el-form-item>
            </div>
          </div>
          </el-form>
        </div>
      </div>
          <div class="flex justify-between" v-if="false">
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
          <!-- Pagenation Part-->
          <div v-if="isPhone">
          </div>
          <div v-else>
            <div class="right-component justify-end px-3 py-3.5 dark:border-gray-700">
              <UPagination v-model="page" :page-count="pageCount" :total="filtered_twitter.length" />
          </div>
          </div>
        </div>

      <el-table fit :data="rows" @sort-change="updateSortData">
        <el-table-column prop="score" label="Score" :width="columnsWidth.score" v-if="false"></el-table-column>
        <el-table-column prop="text" label="Content" :width="columnsWidth.text">
          <template v-slot:default="table">
            <a v-bind:href="table.row.linkToTweet" target="_blank">
              <p :class="contentClass"> {{table.row.text}} </p>
            </a>
         </template>
        </el-table-column>
        <el-table-column prop="createAt" label="Time" :width="columnsWidth.createAt" sortable="custom"></el-table-column>
      </el-table>

      <div class="flex place-content-center px-3 py-3.5 dark:border-gray-700">
          <UPagination v-model="page" :page-count="pageCount" :total="filtered_twitter.length" />
      </div>
      </div>
    </div>

</template>