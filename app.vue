<template>
  <div>
    <div class="flex justify-center mt-8 space-x-4">
      <button @click="showTwitterTable" class="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded">
        搜索推特
      </button>
      <button @click="showLatestTwitter" class="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded">
        最新推特
      </button>
      <button @click="showAutoReply" class="bg-teal-500 hover:bg-teal-600 text-white py-2 px-4 rounded">
        自动回复
      </button>
    </div>
    <div class="mt-4">
      <TwitterTable v-if="showTable" />
      <LatestTwitter v-if="showLatest" />
      <AutoReply v-if="showAuto" />
    </div>
  </div>
</template>

<script>
export default {
  components: {
    TwitterTable: () => import('@/components/TwitterTable.vue'),
    LatestTwitter: () => import('@/components/LatestTwitter.vue'),
    AutoReply: () => import('@/components/AutoReply.vue')
  },
  data() {
    return {
      showTable: true,
      showLatest: false,
      showAuto: false
    };
  },
  methods: {
    showTwitterTable() {
      this.showTable = true;
      this.showLatest = false;
      this.showAuto = false;
    },
    showLatestTwitter() {
      this.showTable = false;
      this.showLatest = true;
      this.showAuto = false;
    },
    showAutoReply() {
      this.showTable = false;
      this.showLatest = false;
      this.showAuto = true;
    }
  }
};
</script>