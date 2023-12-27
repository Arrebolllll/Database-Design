<template>
  <div class="file-manager">
    <div style="display: flex; align-items: center; gap: 10px;">
      <el-button type="primary" @click="openAdd" round>新增销售记录<i class="el-icon-plus el-icon--right"></i></el-button>
      <el-button round type="info" @click="toggleSelection()">取消选择<i
          class="el-icon-circle-close el-icon--right"></i></el-button>
      <el-button round @click="submitDelete" type="danger">删除选定<i class="el-icon-delete el-icon--right"></i></el-button>
      <el-button round @click="fetchData" type="success">刷新列表<i class="el-icon-refresh el-icon--right"></i></el-button>
      <el-button round @click="overallShow">查看总体销售情况</el-button>
      <el-input v-model="searchKey1" size="mini" placeholder="输入客户名字搜索" />
      <el-input v-model="searchKey2" size="mini" placeholder="输入楼号搜索" />
    </div>
    <!-- 新增记录窗口 -->
    <el-dialog title="新增楼盘信息" :visible.sync="addVisible" width="30%" :before-close="handleClose">
      <el-form label-width="17%">
        <h2 style="margin-bottom: 5%;">购入房间信息</h2>
        <el-form-item label="楼栋" required>
          <el-radio-group v-model="locate">
            <el-radio-button label="A"></el-radio-button>
            <el-radio-button label="B"></el-radio-button>
            <el-radio-button label="C"></el-radio-button>
            <el-radio-button label="D"></el-radio-button>
            <el-radio-button label="E"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="房间号" required>
          <el-input v-model="roomNum" placeholder="请输入房间号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="户型" required placeholder="请选择户型" label-position="left">
          <el-select v-model="roomType" style="width: 70%;">
            <el-option v-for="item in roomTypeOptions" :key="item" :label="item" :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <h2 style="margin-bottom: 5%;">购买人信息</h2>
        <el-form-item label="姓名" required label-position="left">
          <el-input v-model="name" placeholder="请输入买家姓名" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="联系方式" required>
          <el-input v-model="contact" placeholder="请输入联系方式" style="width: 70%;">
          </el-input>
        </el-form-item>
        <h2 style="margin-bottom: 5%;">付费情况</h2>
        <el-form-item label="剩余分期数" required label-position="left">
          <el-input v-model="remain" style="width: 70%;">
          </el-input>
        </el-form-item>
      </el-form>
      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAdd">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 总览窗口 -->
    <el-dialog title="销售信息总览" :visible.sync="overallVisible" width="30%">
      <div ref="bar" class="myBarchart" style="height: 300px;"></div>
      <div ref="pie" class="myPie" style="height: 300px;"></div>
    </el-dialog>
    <el-table ref="multipleTable" stripe :data="filteredData" tooltip-effect="dark" style="width: 100%;margin-top: 2%;"
      @selection-change="handleSelectionChange">
      <!-- 选择框和index -->
      <el-table-column type="selection" width="100%"></el-table-column>
      <el-table-column type="index" min-width="20%"></el-table-column>

      <!-- 表的属性 -->
      <el-table-column label="买家姓名" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[7] }}</template>
      </el-table-column>
      <el-table-column label="联系方式" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[8] }}</template>
      </el-table-column>
      <el-table-column label="楼号" min-width="20%" show-overflow-tooltip sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[0] }}</template>
      </el-table-column>
      <el-table-column label="房号" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[2] }}</template>
      </el-table-column>
      <el-table-column label="剩余分期数" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[6] }}</template>
      </el-table-column>
      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <a href="javascript:;" @click="deleteRecord(scope.row)">删除</a>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination align="center" @size-change="handleSizeChange" @current-change="handleCurrentChange"
      :current-page="currentPage" :page-sizes="[1, 5, 10, 20]" :page-size="pageSize" style="margin-top: 2%;"
      layout="total, sizes, prev, pager, next, jumper" :total="record.length"></el-pagination>
  </div>
</template>
<script>
import axios from 'axios'
import { quote } from '../utils/quoteString'
import * as echarts from 'echarts'
export default {
  data() {
    return {
      relationName: "sell_info",
      record: [],//关系元组信息
      addVisible: false, //新增记录弹出窗口
      overallVisible: false,
      searchKey1: '', //处理sell_info的后续查询
      searchKey2: '',

      locate: 'A',
      roomNum: '',
      roomType: '',
      name: '',
      contact: '',
      remain: '',
      roomTypeOptions: ['A', 'B', 'C', 'D', 'E'],
      insertResult: [],

      currentPage: 1,
      pageSize: 10,

      deleteList: [],  //删除列表
      overall: {
        total: 200,
        male: 140,
        female: 60,
        maxRemain: '',
        minRemain: '',
        A: null,
        B: null,
        C: null,
        D: null,
        E: null
      }
    }
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.pageSize = Math.floor(window.innerWidth / 170);
  },
  computed: {
    filteredData() {
      const filteredBySearchKey1 = this.record.filter(item => item[7].toLowerCase().includes(this.searchKey1.toLowerCase()));
      const filteredBySearchKey2 = this.record.filter(item => item[0].toLowerCase().includes(this.searchKey2.toLowerCase()));
      if (!this.searchKey1 && !this.searchKey2) {
        return this.record.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
      }
      if (this.searchKey1 && this.searchKey2) {
        let result = filteredBySearchKey1.filter(item => filteredBySearchKey2.includes(item))
        return result.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
      }
      else {
        if (this.searchKey1.length > 0) {
          return filteredBySearchKey1.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
        }
        if (this.searchKey2.length > 0) {
          return filteredBySearchKey2.slice((this.currentPage - 1) * this.pageSize, this.currentPage * this.pageSize)
        }
      }
    },
  },
  methods: {
    openAdd() {
      // 打开弹窗，清空状态
      this.addVisible = true
      this.locate = "A"
      this.newFloor = ""
      this.newArea = ""
      this.newPrice = ""
      this.roomType = ""
      this.insertResult = []
    },
    toggleSelection(rows) {
      // 取消选择
      if (rows) {
        rows.forEach(row => {
          this.$refs.multipleTable.toggleRowSelection(row);
        });
      } else {
        this.$refs.multipleTable.clearSelection();
      }
    },
    handleSelectionChange(val) {
      console.log(val);
      this.deleteList = val
    },
    deleteRecord(row) {
      // 处理单条删除
      this.deleteAxios(row)
    },
    submitDelete() {
      if (this.deleteList.length === 0) {
        this.$alert('还未选择任何需要删除的数据集', '提示', {
          confirmButtonText: '确定',
          type: 'warning'
        });
      } else {
        console.log('我要全部删除', this.deleteList)
        var deletePromises = this.deleteList.map(item => this.deleteAxios(item));
        // 使用 Promise.all 来等待所有删除请求完成
        Promise.all(deletePromises)
          .then(() => {
            // 在所有删除操作完成后，执行更新显示的操作
            this.deleteList = []  //清空待删除列表
            this.fetchData(); // 假设存在一个更新显示的函数 fetchData
          })
          .catch(error => {
            // 处理删除失败的情况
          });
      }
    },
    deleteAxios(row) {
      let cond = ['sid']
      cond.push(quote(row[11]))
      axios.post('http://127.0.0.1:5000/delete', {
        "table": this.relationName,
        "where": cond
      }).then(response => {
        let conf = '客户' + row[7] + '买入' + row[0] + row[2] + '的销售信息已经被删除！'
        this.$message({
          //登陆成功
          message: conf,
          type: 'success'
        });
        this.fetchData()
        return response;
      }).catch((error) => {
        let warn = '无法删除客户 ' + row[7] + '买入' + row[0] + row[2] + '的销售信息！'
        this.$message({
          //登陆成功
          message: warn,
          type: 'error'
        });
        return error;
      });
    },
    submitAdd() {
      console.log('我要增加记录')
      this.addVisible = false
      this.insertResult.push(quote(this.locate))
      this.insertResult.push(this.newFloor)
      this.insertResult.push(quote(this.roomType))
      this.insertResult.push(quote(this.name))
      this.insertResult.push(quote(this.contact))
      this.insertResult.push()
      console.log(this.insertResult)
      axios.post('http://127.0.0.1:5000/insertsell', {
        roomnumber: this.roomNum,
        building: this.locate,
        type: this.roomType,
        telephone: this.contact,
        cname: this.name,
        remain: this.remain
      }).then(response => {
        console.log(response);
        this.addVisible = false
        this.$message({
          message: '销售记录插入成功',
          type: 'success'
        });
        return response;
      }).catch((error) => {
        this.$message({
          message: '请先插入对应的客户和房间信息！',
          type: 'error'
        });
        return error;
      });
    },
    submitSelect() {
      console.log('我要筛选出记录')
    },
    fetchData() {
      console.log('我要一进来就获取数据', this.record)
      axios.get('http://127.0.0.1:5000/selectsell', {
        table: this.relationName
      }).then(response => {
        console.log(response);
        this.addVisible = false;
        this.record = response.data
        return response;
      }).catch((error) => {
        console.log(error);
        return error;
      });
    },
    sortByName(obj1, obj2) {
      // 排序
      let val1 = obj1.name
      let val2 = obj2.name
      return val1 - val2
    },
    handleClose(done) {
      // 控制上传窗口
      this.$confirm('确认关闭？你的操作可能还没有完成。')
        .then(_ => {
          done();
        })
        .catch(_ => { });
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
    overallShow() {
      this.overallVisible = true
      setTimeout(() => {
        this.renderCharts();
      }, 1000)
    },
    getOverall(){
      axios.post('',{

      })
    },
    renderCharts() {
      // 使用 ECharts 渲染柱状图
      const optionBar = {
        xAxis: {
          data: ['总人数', '男性', '女性']
        },
        yAxis: {},
        series: [
          {
            type: "bar", //形状为柱状图
            data: [this.overall.total, this.overall.male, this.overall.female]
          }
        ]
      };
      const barChart = echarts.init(this.$refs.bar);
      barChart.setOption(optionBar);

      const optionPie = {
        series: [
          {
            name: '住户分析',
            type: 'pie',    // 设置图表类型为饼图
            radius: '55%',  // 饼图的半径，外半径为可视区尺寸（容器高宽中较小一项）的 55% 长度。
            data: [          // 数据数组，name 为数据项名称，value 为数据项值
              { value: 235, name: 'A栋' },
              { value: 274, name: 'B栋' },
              { value: 310, name: 'C栋' },
              { value: 335, name: 'D栋' },
              { value: 400, name: 'E栋' }
            ]
          }
        ]
      }
    const pieChart = echarts.init(this.$refs.pie);
    pieChart.setOption(optionPie);
  },
}
};
</script>
<style scoped lang="less">
.upload-demo {
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/deep/.el-list-enter-active,
/deep/.el-list-leave-active {
  transition: none;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
