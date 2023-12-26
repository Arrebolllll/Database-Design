<template>
  <div class="file-manager">
    <!-- 顶部按钮 -->
    <el-button type="primary" @click="openAdd" round>新增客户<i class="el-icon-plus el-icon--right"></i></el-button>
    <el-button round type="warning" @click="selectVisible = true" style="margin-left: 2%;">筛选客户<i
        class="el-icon-search el-icon--right"></i></el-button>
    <el-button round @click="toggleSelection()" style="margin-left: 2%;">取消选择<i
        class="el-icon-circle-close el-icon--right"></i></el-button>
    <el-button round @click="submitDelete" type="danger" style="margin-left: 2%;">删除选定<i
        class="el-icon-delete el-icon--right"></i></el-button>

    <!-- 新增记录窗口 -->
    <el-dialog title="新增客户" :visible.sync="addVisible" width="30%" :before-close="handleClose">
      <el-form label-width="17%">
        <el-form-item label="姓名" required>
          <el-input v-model="newName" placeholder="请输入姓名" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="性别" required>
          <el-radio label="男" v-model="newGender" border></el-radio>
          <el-radio label="女" v-model="newGender" border></el-radio>
        </el-form-item>
        <el-form-item label="年龄" required>
          <el-input v-model="newAge" placeholder="请输入年龄" style="width: 70%;">
          </el-input>
        </el-form-item>
        <el-form-item label="联系方式" required placeholder="请输入联系方式" label-position="left">
          <el-input v-model="newAge" placeholder="请输入年龄" style="width: 70%;">
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
      <el-table-column label="客户名字" min-width="20%" sortable>
        <template slot-scope="scope">{{ scope.row[1] }}</template>
      </el-table-column>
      <el-table-column label="性别" min-width="20%">
        <template slot-scope="scope">{{ scope.row[3] === 'female' ? '女' : '男' }}</template>
      </el-table-column>

      <el-table-column label="年龄" min-width="20%" sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row[4] }}</template>
      </el-table-column>
      <el-table-column label="联系方式" min-width="20%">
        <template slot-scope="scope">{{ scope.row[2] }}</template>
      </el-table-column>
      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <a href="javascript:;" @click="deleteRecord(scope.row)">删除 | </a>
          <a href="javascript:;">修改</a>
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
      relationName: "custom_info",
      record: [],//表格信息
      addVisible: false, //新增记录弹出窗口
      selectVisible: false, //筛选记录弹出窗口
      newAttr1: "",
      newAttr2: "",
      newAttr3: "",
      newAttr4: "",
      searchKey: "", //查询的关键字

      newName: '',
      newGender: '',
      newAge: '',
      newContact: '',
      insertResult: [],

      currentPage: 1, //默认页数
      pageSize: 10, //默认显示行数

      deleteList: []  //删除列表
    }
  },
  created() {
    this.fetchData();
  },
  mounted() {
    this.pageSize = Math.floor(window.innerWidth / 170);
  },
  methods: {
    openAdd() {
      // 打开弹窗，清空状态
      this.addVisible = true
      this.newName = ""
      this.newGender = ""
      this.newAge = ""
      this.newContact = ""
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
      let cond = ['cid']
      cond.push(quote(row[0]))
      axios.post('http://127.0.0.1:5000/delete', {
        "table": this.relationName,
        "where": cond
      }).then(response => {
        let conf = '客户 ' + row[1] + ' 的信息已经被删除！'
        this.$message({
          message: conf,
          type: 'success'
        });
        this.fetchData()
        return response;
      }).catch((error) => {
        let warn = '无法删除客户 ' + row[1] + ' 的信息，他已经购买了房子!'
        this.$message({
          message: warn,
          type: 'error'
        });
        return error;
      });
    },
    submitAdd() {
      console.log('我要增加记录')

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
