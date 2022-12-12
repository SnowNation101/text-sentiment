<template>
    <div id="visualNode">
        <div style="width:100%;height:100%">
            <div id="com_top">
                <div style="height:100%;width: 20%;float:left;">
                    <p style="margin:0;padding-bottom:0;font-family: Arial, Helvetica, sans-serif;font-size: 30px;">
                        Comment
                        analyzer</p>
                    <p style="margin:0;padding-top:0;font-family: Arial, Helvetica, sans-serif;font-size: 10px;">
                        Select hotels and different types of comment.</p>
                </div>
                <div style="height:100%;width: 80%;float:left;">
                    <el-input style="width:25%;" placeholder="请输入酒店" v-model="searchHotel">
                        <i slot="prefix" class="el-input__icon el-icon-search"></i>
                    </el-input>
                    <el-divider direction="vertical"></el-divider>
                    <a>筛选分数 大于 </a>
                    <el-input style="width:8%" placeholder="输入分值" v-model="searchUp">
                    </el-input>
                    <a> 的评论</a>
                    <el-divider direction="vertical"></el-divider>
                    <a>小于 </a>
                    <el-input style="width:8%" placeholder="输入分值" v-model="searchDown">
                    </el-input>
                    <a> 的评论</a>
                    <el-divider direction="vertical"></el-divider>
                    <el-button @click="search_Hotel(searchHotel)">Search</el-button>
                    <el-divider direction="vertical"></el-divider>
                    <el-button @click="getTables()">Analyse</el-button>
                </div>
            </div>
            <div id="tac">
                <div id="table">
                    <template>
                        <el-table v-loading="this.$store.state.loading"
                            :data="$store.state.tableData1.filter(data =>
                            (!searchHotel || data.name.toLowerCase().includes(searchHotel.toLowerCase())) &&
                            (!searchUp || data.score >= searchUp) &&
                            (!searchDown || data.score <= searchDown)).slice((currentPage - 1) * pageSize, currentPage * pageSize)" stripe height="92%" border
                            style="width: 100%">
                            <el-table-column prop="name" label="酒店名称" min-width="90">
                            </el-table-column>
                            <el-table-column prop="date" label="日期" min-width="90">
                            </el-table-column>
                            <el-table-column prop="comment" label="评论" min-width="180">
                            </el-table-column>
                            <el-table-column prop="positive" label="positive" min-width="60">
                            </el-table-column>
                            <el-table-column prop="negative" label="negative" min-width="62">
                            </el-table-column>
                            <el-table-column prop="anger" label="anger" min-width="50">
                            </el-table-column>
                            <el-table-column prop="disgust" label="disgust" min-width="60">
                            </el-table-column>
                            <el-table-column prop="fear" label="fear" min-width="40">
                            </el-table-column>
                            <el-table-column prop="sadness" label="sadness" min-width="60">
                            </el-table-column>
                            <el-table-column prop="surprise" label="surprise" min-width="60">
                            </el-table-column>
                            <el-table-column prop="good" label="good" min-width="45">
                            </el-table-column>
                            <el-table-column prop="happy" label="happy" min-width="50">
                            </el-table-column>
                            <el-table-column prop="score" label="score" min-width="50">
                            </el-table-column>
                        </el-table>
                    </template>
                    <div class="block" style="margin-top:15px;height:5%">
                        <el-pagination align='center' @size-change="handleSizeChange"
                            @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="pageSizes"
                            :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="$store.state.tableData1.filter(data =>
                            (!searchHotel || data.name.toLowerCase().includes(searchHotel.toLowerCase())) &&
                            (!searchUp || data.score >= searchUp) &&
                            (!searchDown || data.score <= searchDown)).length">
                        </el-pagination>
                    </div>
                </div>
            </div>
        </div>
        <div style="width:100%;height:200%;">
            <div id="bar" style="height:50%;width:100%;"></div>
            <div id="bar1" style="height:50%;width:100%;"></div>
        </div>
    </div>
</template>

<script>
import * as echarts from "echarts";
export default {
    /* eslint-disable */
    name: 'visualNode',
    data() {
        return {
            sum: 100,
            load: false,
            searchHotel: '',
            searchUp: '',
            searchDown: '',
            currentPage: 1, // 当前页码
            total: 20, // 总条数
            pageSize: 8,// 每页的数据条数
            pageSizes: [10],
            option_bar: {
                title: {
                    text: '酒店评论平均分数排名',
                    subtext: '从高到低排序',
                    left: 'center'
                },
                dataset: [
                    {
                        dimensions: ['name', 'score'],
                        source: [

                        ]
                    },
                    {
                        transform: {
                            type: 'sort',
                            config: { dimension: 'score', order: 'desc' }
                        }
                    }
                ],
                xAxis: {
                    type: 'category',
                    axisLabel: { interval: 0, rotate: 30 }
                },
                yAxis: {},
                series: {
                    type: 'bar',
                    encode: { x: 'name', y: 'score' },
                    datasetIndex: 1
                }
            },
            option_bar1: {
                title: {
                    text: '酒店评论中各情绪因子所占比例',
                    subtext: '从高到低排序',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'item',
                },
                xAxis: {
                    type: 'category',
                    data: ['positive', 'negative', 'anger', 'disgust', 'fear', 'sadness', 'surprise', 'good', 'happy']
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        show: true,
                        interval: 'auto',
                        formatter: '{value} %'//纵坐标百分比
                    }
                },
                series: [
                    {
                        data: [],
                        type: 'bar',
                        itemStyle: {
                            normal: {
                                //这里是颜色
                                color: function (params) {
                                    //注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
                                    var colorList = ['#00A3E0', '#FFA100', '#ffc0cb', '#CCCCCC', '#BBFFAA', '#749f83', '#ca8622', '#00A3E0', '#FFA100'];
                                    return colorList[params.dataIndex]
                                }
                            }
                        }
                    }
                ]
            }
        }
    },
    methods: {
        search_Hotel(name) {
            var tempSet = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            for (let i = 0; i < this.$store.state.tableData1.length; i++) {
                if (this.$store.state.tableData1[i].name == name) {
                    tempSet[0] += this.$store.state.tableData1[i].positive
                    tempSet[1] += this.$store.state.tableData1[i].negative
                    tempSet[2] += this.$store.state.tableData1[i].anger
                    tempSet[3] += this.$store.state.tableData1[i].disgust
                    tempSet[4] += this.$store.state.tableData1[i].fear
                    tempSet[5] += this.$store.state.tableData1[i].sadness
                    tempSet[6] += this.$store.state.tableData1[i].surprise
                    tempSet[7] += this.$store.state.tableData1[i].good
                    tempSet[8] += this.$store.state.tableData1[i].happy
                }
            }
            let sum = tempSet[0] + tempSet[1] + tempSet[2] + tempSet[3] + tempSet[4] + tempSet[5] + tempSet[6] + tempSet[7] + tempSet[8]
            for (let i = 0; i < 9; i++) {
                tempSet[i] = tempSet[i] / sum * 100
            }
            this.option_bar1.series[0].data = tempSet
            this.refreshChart()
        },
        getTables() {
            this.$store.dispatch("getTable_2");
            
            setTimeout(() => {  //设置延迟执行
                this.sortScore()
                this.refreshChart()
            }, 1000);
        },
        draw() {
            var myChart1 = echarts.init(document.getElementById('bar'));
            this.option_bar && myChart1.setOption(this.option_bar);
            var myChart2 = echarts.init(document.getElementById('bar1'));
            this.option_bar1 && myChart2.setOption(this.option_bar1);
        },
        refreshChart() {
            document.getElementById('bar').removeAttribute('_echarts_instance_');
            this.draw();
        },
        //每页条数改变时触发 选择一页显示多少行
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
            this.currentPage = 1;
            this.pageSize = val;
        },
        //当前页改变时触发 跳转其他页
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
            this.currentPage = val;
        },
        handleClose(done) {
            done();
        },
        sortScore() {
            var tempNameSet = []
            var tempScoreSet = []
            var tempNumSet = []
            for (let i = 0; i < this.$store.state.tableData1.length; i++) {
                if (tempNameSet.indexOf(this.$store.state.tableData1[i].name) == -1) {
                    tempNameSet.push(this.$store.state.tableData1[i].name)
                    tempScoreSet.push(this.$store.state.tableData1[i].score)
                    tempNumSet.push(1)
                }
                else {
                    let index = tempNameSet.indexOf(this.$store.state.tableData1[i].name)
                    tempScoreSet[index] += this.$store.state.tableData1[i].score
                    tempNumSet[index] += 1
                }
            }
            for (let i = 0; i < tempNameSet.length; i++) {
                this.option_bar.dataset[0].source.push([tempNameSet[i], tempScoreSet[i] / tempNumSet[i]])
            }
            this.$store.state.tableData1
        }
    },
    mounted() {
        this.draw();
        //this.$store.dispatch("getTable");
    }
}
</script>

<style>
#visualNode {
    width: 100%;
    height: 86vh;
}

#com_top {
    width: 100%;
    height: 11%;
}

#tac {
    width: 100%;
    height: 85%;
}

#table {
    float: left;
    /* width: 57%; */
    width: 97%;
    height: 95%;
    padding: 1%;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin: 1%;
}
</style>