<template>
  <div class="file-manager">
    <!-- 顶部按钮 -->
    <el-button type="primary" round @click="openUpload">添加用户<i class="el-icon-upload el-icon--right"></i></el-button>
    <el-button round @click="toggleSelection()" style="margin-left: 2%;">取消选择<i
        class="el-icon-circle-close el-icon--right"></i></el-button>
    <el-button round @click="deleteFile" type="danger" style="margin-left: 2%;">删除选定<i
        class="el-icon-delete el-icon--right"></i></el-button>
    <el-button round @click="insertest" type="danger" style="margin-left: 2%;">插入销售信息<i
        class="el-icon-delete el-icon--right"></i></el-button>
    <!-- 上传弹出窗口 -->
    <el-dialog title="上传文件" :visible.sync="uploadVisible" width="30%" :before-close="handleClose">
      <el-form>
        <el-form-item label="数据集名称" required>
          <el-input v-model="customName" placeholder="默认为文件名"></el-input>
        </el-form-item>
      </el-form>
      <el-upload class="upload-demo" drag ref="upload" action="string" :file-list="uploadList" :auto-upload="false"
        :on-remove="handleRemove" :on-change="handleChange" accept=".zip">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传单个zip文件</div>
      </el-upload>
      <!-- 进度条 -->
      <transition name="fade">
        <div class="progressBar" v-show="progressBarShow" style="margin-top: 2px;">
          <el-progress v-if="uploadStatus == null" :text-inside="true" :stroke-width="20"
            :percentage="uploadProgress"></el-progress>
          <el-progress v-else :text-inside="true" :stroke-width="20" :percentage="uploadProgress"
            :status="uploadStatus"></el-progress>
        </div>
      </transition>

      <!-- 下方按钮 -->
      <span slot="footer" class="dialog-footer">
        <el-button @click="uploadVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitUpload">上 传</el-button>
      </span>
    </el-dialog>

    <!-- 用户数据集列表 -->
    <el-table ref="multipleTable"
      :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
      tooltip-effect="dark" style="width: 100%;margin-top: 2%;" @selection-change="handleSelectionChange"
      :default-sort="{ prop: 'date', order: 'descending' }">
      <el-table-column type="selection" width="100%"></el-table-column>
      <el-table-column type="index" min-width="20%"></el-table-column>
      <el-table-column label="面积" min-width="20%" show-overflow-tooltip sortable :sort-method="sortByName">
        <template slot-scope="scope">{{ scope.row.name }}</template>
      </el-table-column>
      
      <el-table-column label="户型" min-width="20%" sortable></el-table-column>
      <el-table-column label="每平方（元）" min-width="20%" sortable></el-table-column>
      <el-table-column label="操作" min-width="20%">
        <template slot-scope="scope">
          <a href="javascript:;" @click="goToMark(scope.row.name)">标注 |</a>
          <a href="javascript:;"> 清洗 |</a>
          <a href="javascript:;"> 增广</a>
        </template>
      </el-table-column>
      <el-table-column align="right" min-width="20%">
        <template slot="header" slot-scope="scope">
          <el-input v-model="search" size="mini" placeholder="输入关键字搜索" />
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
      uploadVisible: false, //控制弹出窗口
      fileName: "",
      tableData: [],
      selectedFiles: [],
      search: "", //关键字搜索
      deleteList: [], //待删除的列表
      
      progressBarShow: false, //上传进度条是否显示

      
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    insertest() {
      axios.post('http://127.0.0.1:5000/insert',{
        table:this.tableName,
        rid:this.rid,
        cid:this.cid,
        loan_month:12,
        if_full:"yes"
      })
        .then(response => {
          console.log('插入成功:', response.data);
        })
        .catch(error => {
          console.error('插入数据时发生错误:', error);
        });
    },
    openUpload() {
      this.uploadVisible = true
      this.uploadList = []
      this.customName = ''
      this.clearBarStatus()
    },
    handleClose(done) {
      // 控制上传窗口
      this.$confirm('确认关闭？你的文件可能还没有上传成功。')
        .then(_ => {
          done();
        })
        .catch(_ => { });
    },
    
    
    // createChunk(file) {
    //   const chunkList = []
    //   const totalChunks = Math.ceil(file.size / chunkSize)//最多需要多少块
    //   var i = 0, cur = 0
    //   for (i, cur; i < totalChunks; i += 1, cur += chunkSize) {
    //     chunkList.push({
    //       file: file.slice(cur, cur + chunkSize),  //每次切chunkSize，把这块放到file
    //       idx: i,  //每块的下标
    //       name: file.name,
    //       num: totalChunks
    //     })
    //   }
    //   return chunkList;   //返回装chunk的列表
    // },
    // uploadChunk(chunk, onUploadProgress) {
    //   // 创建一个FormData对象
    //   const formData = new FormData();
    //   // 定义上传文件的元信息
    //   const meta = {
    //     proc_type: 'upload_db',
    //     chunk_idx: chunk.idx,
    //     filename: this.customName,
    //     num: chunk.num
    //   };

    //   // 向formData中添加文件和元信息
    //   formData.append('file', chunk.file);
    //   formData.append('meta', JSON.stringify(meta));

    //   // 发送POST请求，使用onUploadProgress回调来监控上传进度
    //   return axios.post('http://114.132.154.44:5000/Dataset/upload', formData, {
    //     headers: {
    //       'Authorization': 'Bearer ' + Cookies.get('token'),
    //       'Content-Type': 'application/x-www-form-urlencoded'
    //     },
    //     onUploadProgress, // 添加这行
    //   })
    //     .then((response) => {
    //       console.log(chunk.idx, '上传成功', response);
    //       // 返回成功的响应
    //       return response;
    //     })
    //     .catch((error) => {
    //       console.log(chunk.idx, '上传失败', error);
    //       // 抛出错误，以便 Promise.all 捕获
    //       throw error;
    //     });
    // },
    // submitUpload() {
    //   // 获取上传文件
    //   var file = this.uploadList[0].raw;
    //   // 创建文件块列表
    //   var chunkList = this.createChunk(file);
    //   // 获取总的文件块数量
    //   var totalChunks = chunkList.length;
    //   // 用于跟踪已上传的文件块数量
    //   var uploadedChunks = 0;

    //   // 定义上传进度回调函数
    //   var onUploadProgress = (progressEvent) => {
    //     // 计算上传进度
    //     this.uploadProgress = Math.round((uploadedChunks / totalChunks) * 100);
    //   };

    //   // 使用 Promise.all 来等待所有上传请求完成
    //   var uploadPromises = chunkList.map(chunk => {
    //     return this.uploadChunk(chunk, onUploadProgress)
    //       .then(() => {
    //         uploadedChunks++;
    //       });
    //   });

    //   Promise.all(uploadPromises)
    //     .then(() => {
    //       // 所有上传请求完成后，执行 fetchData 更新数据
    //       this.uploadStatus = 'success'
    //       this.fetchData()
    //       this.uploadVisible = false  // 移动到这里确保只有在所有上传成功时才隐藏上传框
    //       this.$message({
    //         //文件上传成功
    //         message: '文件上传成功',
    //         type: 'success',
    //         offset: 100
    //       })
    //       // 触发进度条过渡效果
    //       setTimeout(() => {
    //         this.clearBarStatus()
    //       }, 3000); // 等待 3 秒钟后开始过渡
    //     })
    //     .catch(error => {
    //       console.error('Error uploading chunks:', error);
    //       // 处理上传失败的情况
    //       this.uploadStatus = 'exception'
    //       this.uploadVisible = false;  // 移动到这里确保在上传失败时也隐藏上传框
    //     });
    // },
    // 以上为上传文件部分

    // 状态栏相关
    clearBarStatus() {
      this.progressBarShow = false
      this.uploadProgress = 0
      this.uploadStatus = null
    },

    // 排序相关
    sortByName(obj1, obj2) {
      let val1 = obj1.name
      let val2 = obj2.name
      return val1 - val2
    },

    // 以下为用户数据集列表相关
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
      this.deleteList = val.map(row => row.name)  //将选中行的名字加入到待删除列表中
      this.multipleSelection = val;
    },
    fetchData() {
      let url_new = "http://127.0.0.1:5000/selectstar";
      axios.post(url_new, {
        table:'sell_info'
      }).then(response => {
        console.log(response)
        // for (var i = 0; i < response.data.info.length; ++i) {
        //   this.tableData.push({ name: response.data.info[i] })
        // }
      })
    },
    
    sendDelete(datasetName) {
      const formData = new FormData();
      let url_new = "http://114.132.154.44:5000/Dataset/delete";
      formData.append('dataset_name', datasetName);
      return axios.post(url_new, formData, {
        headers: {
          'Authorization': 'Bearer ' + Cookies.get('token'),
        },
      }).then(response => {
        console.log(response);
        return response;
      }).catch((error) => {
        console.log(error);
        return error;
      });
    },
    deleteFile() {
      if (this.deleteList.length == 0) {
        this.$alert('还未选择任何需要删除的数据集', '提示', {
          confirmButtonText: '确定',
          type: 'warning'
        })
      }
      else {
        this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          var deletePromises = this.deleteList.map(name => this.sendDelete(name))
          // 使用 Promise.all 来等待所有删除请求完成
          Promise.all(deletePromises)
            .then(() => {
              console.log('All delete operations completed successfully');
              // 在所有删除操作完成后，执行更新显示的操作
              this.fetchData(); // 假设存在一个更新显示的函数 fetchData
            })
            .catch(error => {
              console.error('Error in delete operations:', error);
              // 处理删除失败的情况
            });
          this.$message({
            type: 'success',
            message: '删除成功!',
            offset: 100
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除',
            offset: 100
          });
        });
      }
    },
  },
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
