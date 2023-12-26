<template>
  <div class="file-manager">
    <!-- 顶部按钮 -->
    <el-button type="primary" @click="openAdd" round>新增<i class="el-icon-plus el-icon--right"></i></el-button>
    <el-button round type="warning" @click="openSelect" style="margin-left: 2%;">筛选<i
        class="el-icon-search el-icon--right"></i></el-button>
    <el-button round type="info" @click="toggleSelection()" style="margin-left: 2%;">取消选择<i
        class="el-icon-circle-close el-icon--right"></i></el-button>
    <el-button round @click="submitDelete" type="danger" style="margin-left: 2%;">删除选定<i
        class="el-icon-delete el-icon--right"></i></el-button>
    <el-button round @click="fetchData" type="success" style="margin-left: 2%;">刷新列表<i
        class="el-icon-refresh el-icon--right"></i></el-button>

    <!-- 新增记录窗口 -->
    <el-dialog title="新增楼盘信息" :visible.sync="addVisible" width="30%" :before-close="handleClose">
      <el-form label-width="17%">
        <el-form-item label="楼号" required>
          <el-radio-group v-model="locate">
            <el-radio-button label="A"></el-radio-button>
            <el-radio-button label="B"></el-radio-button>
            <el-radio-button label="C"></el-radio-button>
            <el-radio-button label="D"></el-radio-button>
            <el-radio-button label="E"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="层号" required>
          <el-input v-model="floor" placeholder="请输入层号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="房号" required>
          <el-input v-model="roomNum" placeholder="请输入房号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="面积" required>
          <el-input v-model="area" placeholder="请输入面积" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="户型" required placeholder="请选择户型" label-position="left">
          <el-select v-model="roomType" style="width: 70%;">
            <el-option v-for="item in roomTypeOptions" :key="item" :label="item" :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总价" required>
          <el-input v-model="price" placeholder="请输入总价" style="width: 70%;">
          </el-input>
        </el-form-item>
      </el-form>
      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="addVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAdd">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 筛选记录弹出窗口 -->
    <el-dialog title="筛选" :visible.sync="selectVisible" width="60%" :before-close="handleClose">
      <el-form>
        <h3 style="margin-bottom: 3%;">筛选层高</h3>
        <el-form-item label="楼号"><el-radio-group v-model="locate">
            <el-radio-button label="A"></el-radio-button>
            <el-radio-button label="B"></el-radio-button>
            <el-radio-button label="C"></el-radio-button>
            <el-radio-button label="D"></el-radio-button>
            <el-radio-button label="E"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <h3 style="margin-bottom: 3%;">筛选面积</h3>
        <el-form-item label="面积">
          <div class="block" style="margin-left: 8%;">
            <el-slider v-model="areaRange" range>
            </el-slider>
          </div>
        </el-form-item>
        <h3 style="margin-bottom: 3%;">筛选价格</h3>
        <el-form-item label="价格">
          <div class="block" style="margin-left: 8%;">
            <el-slider v-model="priceRange" range>
            </el-slider>
          </div>
        </el-form-item>
      </el-form>
      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="selectVisible = false">取 消</el-button>
        <el-button type="primary" @click="selectArea">确 定</el-button>
      </span>
    </el-dialog>

    <!-- 新增修改窗口 -->
    <el-dialog title="修改楼盘信息" :visible.sync="modifyVisible" width="30%" :before-close="handleClose">
      <el-form label-width="17%">
        <el-form-item label="楼号" required>
          <el-radio-group v-model="locate">
            <el-radio-button label="A"></el-radio-button>
            <el-radio-button label="B"></el-radio-button>
            <el-radio-button label="C"></el-radio-button>
            <el-radio-button label="D"></el-radio-button>
            <el-radio-button label="E"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="层号" required>
          <el-input v-model="floor" placeholder="请输入层号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="房号" required>
          <el-input v-model="roomNum" placeholder="请输入房号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="面积" required>
          <el-input v-model="area" placeholder="请输入面积" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="户型" required placeholder="请选择户型" label-position="left">
          <el-select v-model="roomType" style="width: 70%;">
            <el-option v-for="item in roomTypeOptions" :key="item" :label="item" :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总价" required>
          <el-input v-model="price" placeholder="请输入总价" style="width: 70%;">
          </el-input>
        </el-form-item>
      </el-form>
      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="modifyVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitModify">确 定</el-button>
      </span>
    </el-dialog>

    <el-table ref="multipleTable" stripe :data="record.slice((currentPage - 1) * pageSize, currentPage * pageSize)"
      tooltip-effect="dark" style="width: 100%;margin-top: 2%;" @selection-change="handleSelectionChange">
      <!-- 选择框和index -->
      <el-table-column type="selection" width="100%"></el-table-column>
      <el-table-column type="index" min-width="20%"></el-table-column>

      <!-- 表的属性 -->
      <el-table-column label="楼号" min-width="20%" sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[1] }}</template>
      </el-table-column>
      <el-table-column label="层号" min-width="20%" sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[2] }}</template>
      </el-table-column>
      <el-table-column label="房号" min-width="20%" sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[3] }}</template>
      </el-table-column>
      <el-table-column label="面积（平方米）" min-width="20%" show-overflow-tooltip sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[4] }}</template>
      </el-table-column>
      <el-table-column label="户型" min-width="20%">
        <template slot-scope="scope">{{ scope.row[6] + '型' }}</template>
      </el-table-column>
      <el-table-column label="总价" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[5] + 'w' }}</template>
      </el-table-column>

      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <a href="javascript:;" @click="deleteRecord(scope.row)">删除 | </a>
          <a href="javascript:;" @click="modifyRecord(scope.row)">修改</a>
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
import Cookies from 'js-cookie'
export default {
  data() {
    return {
      relationName: "room_info",
      record: [],//表格信息

      newAttr1: "",
      newAttr2: "",
      newAttr3: "",
      newAttr4: "",
      searchKey: "", //查询的关键字

      rid: '',
      locate: '',
      roomNum: '',
      floor: '',
      area: '',
      price: '',
      roomType: '',
      roomTypeOptions: ['A', 'B', 'C', 'D', 'E'],
      insertResult: [],

      currentPage: 1, //默认页数
      pageSize: 10, //默认显示行数

      deleteList: [],  //删除列表

      // 修改信息
      modifyVisible: false, // 修改记录弹出窗口
      addVisible: false, //新增记录弹出窗口
      selectVisible: false, //筛选记录弹出窗口

      // 筛选
      areaRange: [10, 20],  //那两个滑动条
      priceRange: [10, 20],

      // 统计
      minArea: '12',
      maxArea: '34',
      minPrice: '',
      maxPrice: ''
    }
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.pageSize = Math.floor(window.innerWidth / 170);
  },
  methods: {
    openSelect() {
      //打开筛选窗口
      this.selectVisible = true
      this.locate = ''
      this.areaRange = [0, 100]
      this.priceRange = [0, 100]
    },
    openAdd() {
      // 打开弹窗，清空状态
      this.addVisible = true
      this.locate = "A"
      this.floor = ""
      this.roomNum = ""
      this.area = ""
      this.price = ""
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
      let cond = ['rid']
      cond.push(quote(row[0]))
      axios.post('http://127.0.0.1:5000/delete', {
        "table": this.relationName,
        "where": cond
      }).then(response => {
        let conf = '位置为' + row[1] + row[3] + '的房间信息已经被删除！'
        this.$message({
          //登陆成功
          message: conf,
          type: 'success'
        });
        this.fetchData()
        return response;
      }).catch((error) => {
        let warn = '无法删除位置为 ' + row[1] + row[3] + ' 的房间，他已被购入!'
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
      this.insertResult = []
      this.insertResult.push(quote(this.locate.toLowerCase()))
      this.insertResult.push(this.floor)
      this.insertResult.push(quote(this.roomNum))
      this.insertResult.push(this.area)
      this.insertResult.push(this.price)
      this.insertResult.push(quote(this.roomType))
      console.log(this.insertResult)
      axios.post('http://127.0.0.1:5000/insert', {
        table: this.relationName,
        values: this.insertResult
      }).then(response => {
        console.log(response);
        this.addVisible = false
        this.fetchData()
        this.$message({
          message: '插入成功',
          type: 'success'
        });
        return response;
      }).catch((error) => {
        this.$message({
          message: '插入失败',
          type: 'error'
        });
        return error;
      });
    },
    modifyRecord(row) {
      console.log(row)
      this.modifyVisible = true
      this.rid = row[0]
      this.locate = row[1].toUpperCase()
      this.floor = row[2]
      this.roomNum = row[3]
      this.area = row[4]
      this.price = row[5]
      this.roomType = row[6]
    },
    submitModify() {
      let setArr = []
      setArr.push('building', quote(this.locate).toLowerCase())
      setArr.push('floor', this.floor)
      setArr.push('room_number', this.roomNum)
      setArr.push('area', this.area)
      setArr.push('total_price', this.price)
      setArr.push('type', quote(this.roomType))
      console.log(setArr)
      let where = ['rid', quote(this.rid)]
      axios.post('http://127.0.0.1:5000/update', {
        table: this.relationName,
        set: setArr,
        where: where
      }).then(response => {
        console.log(response);
        this.modifyVisible = false
        this.fetchData()
        this.$message({
          message: '修改成功',
          type: 'success'
        });
        return response;
      }).catch((error) => {
        this.$message({
          message: '修改失败',
          type: 'error'
        });
        return error;
      });
    },
    submitSelect() {
      console.log('我要筛选出记录')
    },
    fetchData() {
      console.log('我要一进来就获取数据')
      axios.post('http://127.0.0.1:5000/selectstar', {
        table: this.relationName
      }).then(response => {
        console.log(response);
        this.addVisible = false;
        this.record = response.data;
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
    selectArea() {
      axios.post('http://127.0.0.1:5000/selectrange', {
        table: this.relationName,
        select: "*",
        where: ["area", this.areaRange[0], this.areaRange[1]]
      }).then(response => {
        console.log('筛选结果：', response)
        this.selectVisible = false
        this.record = response.data
        return response;
      }).catch((error) => {
        console.log(error);
        return error;
      });
    }
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
