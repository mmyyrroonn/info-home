<template>
  <div>
    <div class="flex justify-center mt-8 space-x-4">
      <button @click="showTwitterTable" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">
        搜索推特
      </button>
      <button @click="showLatestTwitter" class="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded">
        最新推特
      </button>
    </div>
    <div class="mt-4">
      <TwitterTable v-if="showTable" />
      <LatestTwitter v-if="showLatest" />
    </div>
  </div>
</template>

<script>
export default {
  components: {
    TwitterTable: () => import('@/components/TwitterTable.vue'),
    LatestTwitter: () => import('@/components/LatestTwitter.vue')
  },
  data() {
    return {
      showTable: true,
      showLatest: false
    };
  },
  methods: {
    showTwitterTable() {
      this.showTable = true;
      this.showLatest = false;
    },
    showLatestTwitter() {
      this.showTable = false;
      this.showLatest = true;
    }
  }
};
</script>

