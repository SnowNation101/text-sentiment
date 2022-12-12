import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    output: "",
    load: false,
    show1: true,
    show2: false,
    tableData: [
      // {
      //   name: 'test1',
      //   date: '2016-05-02',
      //   comment: '我住的湖景房,房间不大但卫生间蛮大的还有阳台很不错,看风景很美,服务很热情',
      //   tag: 'GOOD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'BAD'
      // }, {
      //   name: 'test3',
      //   date: '2016-05-01',
      //   comment: '房间设施装修都不错,环境优雅,接待结帐服务不错,够星',
      //   tag: 'GOOD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'BAD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'BAD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'GOOD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'BAD'
      // }, {
      //   name: 'test2',
      //   date: '2016-05-04',
      //   comment: '酒店设施不算新，但是服务很周到。',
      //   tag: 'BAD'
      // }
    ],
    tableData1: [
      // {
      //   name: 'test1',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 10.5
      // }, {
      //   name: 'test2',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 3
      // }, {
      //   name: 'test3',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 55
      // }, {
      //   name: 'test4',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 1
      // }, {
      //   name: 'test4',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 1
      // }, {
      //   name: 'test5',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 4
      // }, {
      //   name: 'test5',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 11
      // }, {
      //   name: 'test6',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 1,
      //   negative: 1,
      //   anger: 2,
      //   disgust: 3,
      //   fear: 4,
      //   sadness: 5,
      //   surprise: 6,
      //   good: 7,
      //   happy: 8,
      //   score: 1
      // }, {
      //   name: 'test7',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 1
      // }, {
      //   name: 'test8',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 1
      // }, {
      //   name: 'test9',
      //   date: '123',
      //   comment: 'sdgsdjghujhg',
      //   positive: 0,
      //   negative: 1,
      //   anger: 0,
      //   disgust: 1,
      //   fear: 0,
      //   sadness: 0,
      //   surprise: 0,
      //   good: 0,
      //   happy: 0,
      //   score: 1
      // }
    ],
  },
  getters: {},

  mutations: {
    /* eslint-disable */
    show1(state) {
      state.show1 = true;
      state.show2 = false;
    },
    show2(state) {
      state.show1 = false;
      state.show2 = true;
    },
    getTable(state, data) {
      //拿表格数据
      state.tableData.splice(0, state.tableData.length);
      for (let i = 0; i < data.length; i++) {
        let tag_;
        if (data[i].tag == 1) {
          tag_ = "GOOD";
        } else {
          tag_ = "BAD";
        }
        let temp = {
          name: data[i].hotelName,
          date: data[i].time,
          comment: data[i].content,
          tag: tag_,
        };
        state.tableData.push(temp);
      }
      state.tableData.splice(1, 0);
    },
    getTable_1(state, data) {
      //拿表格数据
      state.tableData.splice(0, state.tableData.length);
      for (let i = 0; i < data.length; i++) {
        let tag_;
        if (data[i].score >= 0) {
          tag_ = "GOOD" + "(" + data[i].score + ")";
        } else {
          tag_ = "BAD" + "(" + data[i].score + ")";
        }
        let temp = {
          name: data[i].hotelName,
          date: data[i].time,
          comment: data[i].content,
          tag: tag_,
        };
        state.tableData.push(temp);
      }
      state.tableData.splice(1, 0);
    },
    getTable_2(state, data) {
      //拿表格数据
      state.tableData1.splice(0, state.tableData1.length);
      for (let i = 0; i < data.length; i++) {
        let temp = {
          name: data[i].hotelName,
          date: data[i].time,
          comment: data[i].content,
          positive: data[i].positive,
          negative: data[i].negative,
          anger: data[i].anger,
          disgust: data[i].disgust,
          fear: data[i].fear,
          sadness: data[i].sadness,
          surprise: data[i].surprise,
          good: data[i].good,
          happy: data[i].happy,
          score: data[i].score,
        };
        state.tableData1.push(temp);
      }
      state.tableData1.splice(1, 0);
    },
    analyze(state, data) {
      state.output = data;
      console.log(state.output)
    },
  },

  actions: {
    /* eslint-disable */
    getTable(context) {
      //拿xph评论列表信息
      axios({
        url: "http://localhost:8081/api/algo-2/get-all",
        method: "GET",
      }).then((res) => {
        context.commit("getTable_1", res.data);
      });
    },
    getTable_1(context) {
      //拿zch评论列表信息
      axios({
        url: "http://localhost:8081/api/comment/getall", //留空
        method: "GET",
      }).then((res) => {
        context.commit("getTable_1", res.data);
      });
    },
    getTable_2(context) {
      //拿laj评论列表信息
      axios({
        url: "http://localhost:8081/api/algo-1/get-all",
        method: "GET",
      }).then((res) => {
        context.commit("getTable_2", res.data);
      });
    },
    analyze_X(context, value) {
      axios({
        url: "http://localhost:8081/api/algo-2/run",
        method: "POST",
        params: { str: value.name1, language: value.name2 },
      }).then((res) => {
        console.log("zhixing xph!!!!!!!")
      });
      setTimeout(() => {
        axios({
          url: "http://localhost:8081/api/algo-2/get",
          method: "GET",
        }).then((res) => {
          context.commit("analyze", res.data);
        });
      }, 5000);
    },
    analyze_L(context, content) {
      console.log("lajlajlaj");
      axios({
        url: "http://localhost:8081/api/algo-1/run",
        method: "POST",
        params: { str: content },
      });
      setTimeout(() => {
        axios({
          url: "http://localhost:8081/api/algo-1/get",
          method: "GET",
        }).then((res) => {
          context.commit("analyze", res.data);
        });
      }, 5000);
    },
  },
  modules: {},
});
