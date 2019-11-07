<template>
  <div class="layout-column layout-container" element-loading-text="初始化中...请稍后">
    <h3>人员管理</h3>
    <div class="wjp-table">
      <div class="wjp-table-header layout-row align-center">
        <div class="buttons">
          <el-button type="primary" @click="visible = true">添加分组</el-button>
        </div>
        <div style="margin-left:20px">
          <span>当前分组：</span>
          <el-tag
            class="tag"
            v-for="tag in tags"
            :key="tag[0]"
            closable
            @close="delTeam(tag)"
          >{{tag[1]}}</el-tag>
        </div>
      </div>
      <div class="wjp-table-content">
        <el-table :data="acountData" style="width: 100%">
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="[1]" label="用户名"></el-table-column>
          <!-- <el-table-column prop="name" label="真实姓名"></el-table-column> -->
          <el-table-column prop="[2]" label="分组">
            <template slot-scope="scope">
              <el-select
                v-model="scope.row[2]"
                placeholder="请选择分组"
                @change="groupChange(scope.row)"
              >
                <el-option v-for="tag in tags" :key="tag[0]" :label="tag[1]" :value="tag[0]"></el-option>
              </el-select>
            </template>
          </el-table-column>
          <!-- <el-table-column prop="address" label="今日添加"></el-table-column> -->
          <!-- <el-table-column prop="address" label="今日成功"></el-table-column> -->
          <!-- <el-table-column prop="address" label="占比"></el-table-column> -->
          <el-table-column prop="[3]" label="注册时间"></el-table-column>
          <el-table-column label="操作">
            <template slot-scope="scope">
              <!-- <el-switch v-model="scope.using" :active-text="scope.using?'禁用':'已启用'"></el-switch> -->
              <el-button type="danger" plain size="mini" @click="delUser(scope.row[0])">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    <el-dialog
      title="添加分组"
      :visible.sync="visible"
      :append-to-body="true"
      :close-on-click-modal="false"
    >
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="组 名">
          <el-input v-model="form.teamName"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addTeam">添加</el-button>
          <el-button @click="visible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {
  getAllAcount,
  getTeam,
  addTeam,
  delTeam,
  setGroup,
  delUser
} from "@/api/index";
import dayjs from "dayjs";
const { ipcRenderer } = require("electron");
import { mapState } from "vuex";
export default {
  components: {},
  data() {
    return {
      visible: false,
      tags: [],
      acountData: [],
      form: {
        teamName: ""
      },
      rules: {
        teamName: [
          { required: true, message: "请输入分组名称", trigger: "blur" }
        ]
      }
    };
  },
  computed: {
    ...mapState(["User"])
  },
  created() {
    this.getTeam();
    this.getAllAcount();
  },
  mounted() {},
  methods: {
    //添加分组
    addTeam() {
      this.$refs.form.validate(valid => {
        if (valid) {
          addTeam({
            createAdmin: this.User.user.userName,
            teamName: this.form.teamName
          })
            .then(res => {
              if (res.success) {
                this.visible = false;
                this.$message.success("添加成功！");
                this.getTeam();
              } else {
                this.$message.error("添加失败");
              }
            })
            .catch(_ => {
              this.$message.error("添加失败");
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    //获取分组
    getTeam() {
      getTeam(this.User.user.userName)
        .then(res => {
          if (res.success) {
            res.data.map(item => {
              item[0] = String(item[0]);
            });
            this.tags = res.data;
          } else {
            this.$message.error("获取分组失败");
          }
        })
        .catch(_ => {
          this.$message.error("获取分组失败");
        });
    },
    groupChange(row) {
      setGroup({
        userId: row[0],
        teamId: Number(row[2])
      })
        .then(res => {
          if (res.success) {
            this.$message.success("分组成功");
          } else {
            this.$message.error(res.msg);
          }
        })
        .catch(err => {
          this.$message.error("分组失败");
        })
        .finally(_ => {
          this.getAllAcount();
        });
    },
    //获取全部人员
    getAllAcount() {
      getAllAcount(this.User.user.userName).then(res => {
        if (res.success) {
          res.data.map(item => {
            item[3] = new dayjs(item[3]).format("YYYY-MM-DD HH:mm:ss");
          });
          this.acountData = res.data;
        } else {
        }
      });
    },
    //删除人员
    delUser(id) {
      this.$confirm("是否删除该账号?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          delUser(id).then(res => {
            if (res.success) {
              this.$message.success("删除人员成功！");
              this.getAllAcount();
            } else {
            }
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    //删除分组
    delTeam(row) {
      this.$confirm(`是否删除分组${row[1]}?`, "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          delTeam(row[0]).then(res => {
            if (res.success) {
              this.$message.success("删除分组成功！");
              this.getTeam();
            } else {
            }
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    }
  }
};
</script>
<style lang="scss" scoped>
.tag {
  margin-right: 5px;
}
</style>

