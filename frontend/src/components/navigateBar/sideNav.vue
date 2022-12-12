<template>
    <div id="sideNav">
        <el-menu id="elm" default-active="1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose"
            background-color="#f4f6fb" text-color="#000000" active-text-color="#000000">
            <el-menu-item index="1" @click="show1()">
                <i class="el-icon-menu"></i>
                <span slot="title" style="font-size: 10px;">MOOD ClASSIFY</span>
            </el-menu-item>
            <el-menu-item index="2" @click="show2()">
                <i class="el-icon-document"></i>
                <span slot="title" style="font-size: 10px;">MOOD INCLINE</span>
            </el-menu-item>
        </el-menu>

    </div>
</template>

<script>
export default {
    name: 'sideNav',
    methods: {
        handleOpen(key, keyPath) {
            console.log(key, keyPath);
        },
        handleClose(key, keyPath) {
            console.log(key, keyPath);
        },
        show1(){
            this.$store.commit("show1");
        },
        show2(){
            this.$store.commit("show2");
        },
    }
}
</script>

<style>
#elm {
    overflow:hidden;
    height: 92vh;
}
</style>