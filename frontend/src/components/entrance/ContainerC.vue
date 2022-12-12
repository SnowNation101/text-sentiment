<template>
  <div id="ContainerC">
    <el-container style="position:absolute;left:0;right:0;top:0;bottom:0;">
      <el-header height="8vh">
        <topNav></topNav>
      </el-header>
      <el-container>
        <el-aside width="10%">
          <sideNav></sideNav>
        </el-aside>
        <el-main>
          <textMoodNode v-if="this.$store.state.show1"></textMoodNode>
          <visualNode v-if="this.$store.state.show2"></visualNode>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import sideNav from '../navigateBar/sideNav.vue';
import topNav from '../navigateBar/topNav.vue';
import textMoodNode from '../Fun1_textMood/textMoodNode.vue'
import visualNode from '../Fun2_visual/visualNode.vue'
export default {
  name: 'ContainerC',
  data() {
    return {

    }
  },
  components: {
    sideNav,
    topNav,
    textMoodNode,
    visualNode,
  }
}
</script>

<style>
.el-header {
  background-color: rgba(244,246,251,1.00);
  padding:0
}

#ContainerC {
  width: 100%;
  height: 100%;
}
</style>