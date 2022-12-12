<template>
    <div id="dataInfoNode">
        <div id="com_top">
            <div style="height:100%;width: 20%;float:left;">
                <p style="margin:0;padding-bottom:0;font-family: Arial, Helvetica, sans-serif;font-size: 30px;">Comment
                    analyzer</p>
                <p style="margin:0;padding-top:0;font-family: Arial, Helvetica, sans-serif;font-size: 10px;">
                    Select hotels and different types of comment.</p>
            </div>
            <div style="height:100%;width: 60%;float:left;">
                <el-input style="width:25%;" placeholder="请输入酒店" v-model="searchHotel">
                    <i slot="prefix" class="el-input__icon el-icon-search"></i>
                </el-input>
                <el-divider direction="vertical"></el-divider>
                <el-input style="width:15%" placeholder="请输入标签" v-model="searchTag">
                    <i slot="prefix" class="el-input__icon el-icon-search"></i>
                </el-input>
                <el-divider direction="vertical"></el-divider>
                <el-button @click="search_Hotel(searchHotel)">Search</el-button>
                <el-divider direction="vertical"></el-divider>
                <el-select v-model="value" placeholder="请选择算法种类">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value">
                    </el-option>
                </el-select>
                <el-divider direction="vertical"></el-divider>
                <el-button @click="getTables()">Analyse</el-button>
            </div>
            <div style="height:100%;width: 20%;float: left;text-align: right;">
                <el-button @click="drawer = true">Text Test</el-button>
            </div>
        </div>
        <div id="tac">
            <div id="table1">
                <template>
                    <el-table v-loading="this.$store.state.loading"
                        :data="$store.state.tableData.filter(data =>
                        (!searchHotel || data.name.toLowerCase().includes(searchHotel.toLowerCase())) &&
                        (!searchTag || data.tag.toLowerCase().includes(searchTag.toLowerCase()))).slice((currentPage - 1) * pageSize, currentPage * pageSize)"
                        stripe height="92%" border style="width: 100%">
                        <el-table-column prop="name" label="酒店名称" min-width="110">
                        </el-table-column>
                        <el-table-column prop="comment" label="评论" min-width="180">
                        </el-table-column>
                        <el-table-column prop="tag" label="标签" min-width="90">
                        </el-table-column>
                        <el-table-column prop="date" label="日期" min-width="110">
                        </el-table-column>
                    </el-table>
                </template>
                <div class="block" style="margin-top:15px;height:5%">
                    <el-pagination align='center' @size-change="handleSizeChange" @current-change="handleCurrentChange"
                        :current-page="currentPage" :page-sizes="pageSizes" :page-size="pageSize"
                        layout="total, sizes, prev, pager, next, jumper" :total="$store.state.tableData.filter(data =>
                        (!searchHotel || data.name.toLowerCase().includes(searchHotel.toLowerCase())) &&
                        (!searchTag || data.tag.toLowerCase().includes(searchTag.toLowerCase()))).length">
                    </el-pagination>
                </div>
            </div>
            <div id="charts">
                <div id="lineChart">
                    <div style="width:100%;height:10%;">
                        <p style="font-family:Arial,Helvetica,sans-serif;color:rgb(10, 11, 11);">Change Chart of Weekly
                            Positive Comments</p>
                    </div>
                    <div id="line" v-loading="load" style="height:90%;width:100%;"></div>
                </div>
                <div id="pieChart">
                    <div style="width:100%;height:10%;">
                        <p style="font-family:Arial,Helvetica,sans-serif;color:rgb(10, 11, 11);">酒店评论总数:{{ sum }}</p>
                    </div>
                    <div id="pie" v-loading="load" style="height:100%;width:100%;"></div>
                </div>
            </div>
        </div>

        <el-drawer title="查看数据载体" :visible.sync="drawer" direction="rtl" :before-close="handleClose" size="35%">
            <div style="text-align: center;width: 100%;height: 100%;">
                <div class="input">
                    <el-input type="textarea" :rows="12" placeholder="请输入内容" v-model="inputText">
                    </el-input>
                </div>
                <div style="text-align: center;margin-top:15px;margin-bottom:15px;">
                    <el-button type="success" @click="show()">开始识别</el-button>
                    <el-divider direction="vertical"></el-divider>
                    <el-select v-model="lan" placeholder="选择语言种类" style="width:30%">
                        <el-option v-for="item in languages" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                    <el-divider direction="vertical"></el-divider>
                    <el-select v-model="alo" placeholder="选择算法种类" style="width:30%">
                        <el-option v-for="item in alos" :key="item.value" :label="item.label" :value="item.value">
                        </el-option>
                    </el-select>
                </div>
                <div class="input">
                    <el-input type="textarea" :rows="12" placeholder="识别结果" v-model="this.$store.state.output">
                    </el-input>
                </div>
            </div>

        </el-drawer>
    </div>
</template>

<script>
import * as echarts from "echarts";
export default {
    /* eslint-disable */
    name: 'dataInfoNode',
    data() {
        return {
            lan: '',
            alo: '',
            inputText: '',
            value: '基于规则的情绪识别算法',
            sum: 0,
            load: false,
            drawer: false,
            searchHotel: '',
            searchTag: '',
            currentPage: 1, // 当前页码
            total: 20, // 总条数
            pageSize: 8,// 每页的数据条数
            pageSizes: [10],
            options: [{
                value: '1',
                label: '基于规则的情绪识别算法'
            }, {
                value: '2',
                label: '基于机器学习的情绪识别算法'
            },],
            languages: [{
                value: '0',
                label: '中文情绪识别'
            }, {
                value: '1',
                label: '英文情绪识别'
            }],
            alos: [
                {
                    value: '1',
                    label: '基于规则的识别算法'
                }, {
                    value: '2',
                    label: '基于词典的识别算法'
                }
            ],
            option_line_1: {
                xAxis: {
                    type: 'category',
                    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
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
                        type: 'line',
                        smooth: true
                    }
                ]
            },
            option_bar_1: {
                tooltip: {
                    trigger: 'item'
                },
                legend: {
                    top: '5%',
                    left: 'center'
                },
                series: [
                    {
                        name: 'Access From',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '40',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: [
                            { value: 0, name: 'GOOD' },
                            { value: 0, name: 'BAD' },
                        ]
                    }
                ]
            },
        }
    },
    methods: {
        show() {
            if (this.alo == 1) {
                this.$store.dispatch("analyze_X", {name1: this.inputText, name2: this.lan});
                console.log(this.lan)
            }
            else {
                this.$store.dispatch("analyze_L", this.inputText);
            }
        },
        search_Hotel(name) {
            this.sum = 0
            var good = 0, bad = 0;
            for (let i = 0; i < this.$store.state.tableData.length; i++) {
                if (this.$store.state.tableData[i].name == name) {
                    this.sum += 1
                    if (this.$store.state.tableData[i].tag.includes('GOOD')) {
                        good += 1;
                    }
                    else {
                        bad += 1;
                    }
                }
            }
            for (let i = 0; i < 7; i++) {
                this.option_line_1.series[0].data[i] = Math.floor(Math.random() * 100 + 1)
            }
            this.option_bar_1.series[0].data[0].value = good
            this.option_bar_1.series[0].data[1].value = bad
            this.refreshChart()
        },
        getTables() {
            // if (this.value == 1) {
            //     this.$store.dispatch("getTable");
            // }
            // else if (this.value == 2) {
            //     this.$store.dispatch("getTable_1");
            // }
            this.$store.dispatch("getTable");
        },
        draw() {
            var myChart1 = echarts.init(document.getElementById('line'));
            var myChart2 = echarts.init(document.getElementById('pie'));
            this.option_line_1 && myChart1.setOption(this.option_line_1);
            this.option_bar_1 && myChart2.setOption(this.option_bar_1);
        },
        refreshChart() {
            document.getElementById('line').removeAttribute('_echarts_instance_');
            document.getElementById('pie').removeAttribute('_echarts_instance_');
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
        }
    },
    mounted() {
        this.draw();
    }
}
</script>

<style>
.input {
    width: 90%;
    margin: 0 auto;
}

#dataInfoNode {
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

#table1 {
    float: left;
    width: 57%;
    height: 95%;
    padding: 1%;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin: 1%;
}

#charts {
    float: left;
    width: 39%;
    height: 100%;
    padding: 0;
    margin: 0;
}

#lineChart {
    width: 100%;
    height: 49%;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin-bottom: 1%;
    margin-left: 1%;
    margin-top: 3%;
    text-align: center;
}

#pieChart {
    width: 100%;
    height: 49%;
    border-radius: 6px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    margin-top: 1%;
    margin-left: 1%;
    text-align: center;
}
</style>