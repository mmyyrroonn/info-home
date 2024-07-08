<script setup>
const { data, pending, error, refresh } = await useFetch(
  "https://info.myron-moshui.online/twitter/queryLastestTwitter"
);
const twitters = data.value.data.filter((obj) => obj.score != 0).map((twitter) => {
  const languageType = isChineseOrEnglish(twitter.text);
  return {...twitter, createAt: new Date(twitter.createAt.substring(0, 16)), language: languageType};
});
const page = ref(1);
const pageCount = 50;

const dates = [1, 2, 3, 4, 5, 6];
const date = ref(24);

const language = ref("zh");

var sort = ref({
  prop: 'createAt',
  order: 'descending'
});

function isChineseOrEnglish(text) {
      // 示例的辅助函数，判断文本是否为中文或英文
      const regChinese = new RegExp('[\\u4E00-\\u9FFF]+', 'g'); // 匹配中文的正则表达式
      const regEnglish = new RegExp('[a-zA-Z]+', 'g'); // 匹配英文的正则表达式

      const hasChinese = regChinese.test(text);
      const hasEnglish = regEnglish.test(text);

      if (hasChinese) {
        return 'zh'; // 有中文就叫中文！
      } else if (hasEnglish) {
        return 'en'; // 否则是英文
      } else {
        return 'unknown'; // 未知
      }
    }

function updateSortData(data)
{
  sort.value.prop = data.prop;
  sort.value.order = data.order;
};

const sortFunctions = {
  createAt: {
    ascending: (a, b) => a.createAt - b.createAt,
    descending: (a, b) => b.createAt - a.createAt
  }
};

function toggleLanguage() {
    if (language.value === 'zh') {
      language.value = 'en';
    } else {
      language.value = 'zh';
    }
    console.log(`new language value is ${language.value}`);
};

const filtered_twitter = computed(() => {
  const limitDate = new Date(Date.now() - (date.value?date.value:48) * 60 * 60 * 1000);
  return twitters.filter((twitter) => {
      return twitter.createAt > limitDate && twitter.language === language.value;
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
    return { text: parseInt((innerWidth - 60)), createAt: 60};
  }
  return { text: parseInt((innerWidth - 110)), createAt: 110};
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
</script>

<template>
    <div class="flex">
      <div>
        <div class="flex justify-between">
          <div class="flex left-component">
            <span class="flex items-center py-3.5">显示处于过去</span>
            <div class="py-3.5 dark:border-gray-700">
              <USelect v-model="date" :options="dates" color="primary" />
            </div>
            <span class="flex items-center py-3.5">小时之内的推文</span>
          </div>

          <!-- 切换按钮 -->
          <div class="switch-language">
            <button @click="toggleLanguage" class="px-3 py-1 bg-blue-500 text-white rounded-md shadow-md hover:bg-blue-600">
              {{ language === 'zh' ? '切换为英文' : '切换为中文' }}
            </button>
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
        <el-table-column prop="text" label="Content" :width="columnsWidth.text">
          <template v-slot:default="table">
            <a v-bind:href="'https://x.com/' + table.row.userName + '/status/' + table.row.tweetId" target="_blank">
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