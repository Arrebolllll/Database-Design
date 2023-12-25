<template>
  <div class="file-manager">
    <!-- 顶部按钮 -->
    <el-button type="primary" @click="addVisible = true" round>新增<i class="el-icon-upload el-icon--right"></i></el-button>
    <el-button round type="warning" @click="selectVisible = true" style="margin-left: 2%;">筛选<i
        class="el-icon-delete el-icon--right"></i></el-button>
    <el-button round @click="toggleSelection()" style="margin-left: 2%;">取消选择<i
        class="el-icon-circle-close el-icon--right"></i></el-button>
    <el-button round @click="deleteRecord" type="danger" style="margin-left: 2%;">删除选定<i
        class="el-icon-delete el-icon--right"></i></el-button>

    <!-- 新增记录窗口 -->
    <el-dialog title="新增记录" :visible.sync="addVisible" width="30%" :before-close="handleClose">
      <el-form>
        <el-form-item label="新增属性一" required><el-input v-model="newAttr1" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性二" required><el-input v-model="newAttr2" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性三" required><el-input v-model="newAttr3" placeholder=""></el-input></el-form-item>
        <el-form-item label="新增属性四" required><el-input v-model="newAttr4" placeholder=""></el-input></el-form-item>
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

    <el-table ref="multipleTable"
      :data="record.filter(data => !searchKey || data.name.toLowerCase().includes(search.toLowerCase()))"
      tooltip-effect="dark" style="width: 100%;margin-top: 2%;" @selection-change="handleSelectionChange">
      <!-- 选择框和index -->
      <el-table-column type="selection" width="100%"></el-table-column>
      <el-table-column type="index" min-width="20%"></el-table-column>

      <!-- 表的属性 -->
      <el-table-column label="面积" min-width="20%" show-overflow-tooltip sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      <el-table-column label="户型" min-width="20%" sortable></el-table-column>
      <el-table-column label="每平方（元）" min-width="20%" sortable></el-table-column>
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
  </div>
</template>
<script>
import axios from 'axios'
import Cookies from 'js-cookie'
export default {
  data() {
    return {
      record: [],//表格信息
      addVisible: false, //新增记录弹出窗口
      selectVisible: false, //筛选记录弹出窗口
      newAttr1: "",
      newAttr2: "",
      newAttr3: "",
      newAttr4: "",
      searchKey:"", //查询的关键字
    }
  },
  mounted(){
    this.fetchData();
  },
  methods: {
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
    },
    submitSelect() {
      console.log('我要筛选出记录')
    },
    fetchData(){
      console.log('我要一进来就获取数据')
    },
    sortByName(obj1, obj2) {
      // 排序
      let val1 = obj1.name
      let val2 = obj2.name
      return val1 - val2
    },
    handleClose(done) {
      // 控制上传窗口
      this.$confirm('确认关闭？你的文件可能还没有上传成功。')
        .then(_ => {
          done();
        })
        .catch(_ => { });
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
