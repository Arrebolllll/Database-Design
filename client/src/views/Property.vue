<template>
  <div class="file-manager">
    <!-- 顶部按钮 -->
    <el-button type="primary" @click="openAdd" round>新增<i class="el-icon-plus el-icon--right"></i></el-button>
    <el-button round type="warning" @click="selectVisible = true" style="margin-left: 2%;">筛选<i
        class="el-icon-search el-icon--right"></i></el-button>
    <el-button round @click="toggleSelection()" style="margin-left: 2%;">取消选择<i
        class="el-icon-circle-close el-icon--right"></i></el-button>
    <el-button round @click="deleteRecord" type="danger" style="margin-left: 2%;">删除选定<i
        class="el-icon-delete el-icon--right"></i></el-button>

    <!-- 新增记录窗口 -->
    <el-dialog title="新增楼盘信息" :visible.sync="addVisible" width="30%" :before-close="handleClose">
      <el-form label-width="17%">
        <el-form-item label="楼号" required>
          <el-radio-group v-model="newLocate">
            <el-radio-button label="A"></el-radio-button>
            <el-radio-button label="B"></el-radio-button>
            <el-radio-button label="C"></el-radio-button>
            <el-radio-button label="D"></el-radio-button>
            <el-radio-button label="E"></el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="层号" required>
          <el-input v-model="newFloor" placeholder="请输入层号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="房号" required>
          <el-input v-model="newRoomNum" placeholder="请输入房号" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="面积" required>
          <el-input v-model="newArea" placeholder="请输入面积" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="户型" required placeholder="请选择户型" label-position="left">
          <el-select v-model="newRoomType" style="width: 70%;">
            <el-option v-for="item in roomTypeOptions" :key="item" :label="item" :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总价" required>
          <el-input v-model="newPrice" placeholder="请输入总价" style="width: 70%;">
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
    <el-dialog title="筛选" :visible.sync="selectVisible" width="30%" :before-close="handleClose">
      <el-form>
        <el-form-item label="新增属性一" required><el-input v-model="newAttr1" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性二" required><el-input v-model="newAttr2" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性三" required><el-input v-model="newAttr3" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性四" required><el-input v-model="newAttr4" placeholder=""></el-input></el-form-item>
      </el-form>
      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="selectVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitSelect">确 定</el-button>
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
      <el-table-column label="面积" min-width="20%" show-overflow-tooltip sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[4] }}</template>
      </el-table-column>
      <el-table-column label="户型" min-width="20%">
        <template slot-scope="scope">{{ scope.row[6] }}</template>
      </el-table-column>
      <el-table-column label="总价" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[5] + 'w' }}</template>
      </el-table-column>

      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <a href="javascript:;" @click="deleteRecord">删除 |</a>
          <a href="javascript:;">修改</a>
        </template>
      </el-table-column>

      <!-- 右侧关键字查询框 -->
      <el-table-column align="right" min-width="20%">
        <template slot="header" slot-scope="scope">
          <el-input v-model="searchKey" size="mini" placeholder="输入关键字搜索" />
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
      addVisible: false, //新增记录弹出窗口
      selectVisible: false, //筛选记录弹出窗口
      newAttr1: "",
      newAttr2: "",
      newAttr3: "",
      newAttr4: "",
      searchKey: "", //查询的关键字

      newLocate: 'A',
      newRoomNum: '',
      newFloor:'',
      newArea: '',
      newPrice: '',
      newRoomType: '',
      roomTypeOptions: ['A型', 'B型', 'C型', 'D型', 'E型'],
      insertResult: [],

      currentPage: 1, //默认页数
      pageSize: 10, //默认显示行数
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    openAdd() {
      // 打开弹窗，清空状态
      this.addVisible = true
      this.newLocate = "A"
      this.newFloor = ""
      this.newRoomNum = ""
      this.newArea = ""
      this.newPrice = ""
      this.newRoomType = ""
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
    },
    deleteRecord() {
      console.log('我要删除');
    },
    submitAdd() {
      console.log('我要增加记录')
      this.insertResult.push(quote(this.newLocate))
      this.insertResult.push(this.newFloor)
      this.insertResult.push(quote(this.newRoomNum))
      this.insertResult.push(this.newArea)
      this.insertResult.push(this.newPrice)
      this.insertResult.push(quote(this.newRoomType))
      console.log(this.insertResult)
      axios.post('http://127.0.0.1:5000/insert', {
        table: this.relationName,
        values: this.insertResult
      }).then(response => {
        console.log(response);
        return response;
      }).catch((error) => {
        console.log(error);
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
