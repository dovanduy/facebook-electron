<template>
<el-drawer
  class="add-task"
  title="添加定时任务"
  :visible.sync="show"
  size="400px"
  :before-close="handleClose">
  <el-form class="task-form" ref="form" :model="tasks" label-width="100px" size="mini">
    <el-form-item label="账号设备" style="width: 85%">
      <span>{{defaultDevice.fb_nickName || defaultDevice.device_model}}</span>
      <el-divider direction="vertical"></el-divider>
      <span>{{defaultDevice.device_remark || '未设置'}}</span>
    </el-form-item>
    <el-divider content-position="left">好友任务</el-divider>
    <el-form-item title="建议最少10分钟以上" label="执行间隔" prop="minutesNum" style="width: 85%">
      <el-input @change="validate10f(tasks.friends.minutesNum)" type="number" min="10" v-model="tasks.friends.minutesNum" placeholder="每次任务隔多久执行">
        <template slot="append">分钟</template>
      </el-input>
    </el-form-item>
    <div v-for="(friend, index) in tasks.friends.params" :key="'friend' + index">
      <el-form-item label="搜索词" prop="msg" style="width: 85%">
        <el-input v-model="friend.msg" placeholder="搜索关键词"></el-input>
      </el-form-item>
      <el-form-item label="城市" prop="city" style="width: 85%">
        <el-input v-model="friend.city" placeholder="城市关键词"></el-input>
      </el-form-item>
      <el-form-item label="学校" prop="school" style="width: 85%">
        <el-input v-model="friend.school" placeholder="学校关键词"></el-input>
      </el-form-item>
      <el-form-item label="公司" prop="work" style="width: 85%">
        <el-input v-model="friend.work" placeholder="公司关键词"></el-input>
      </el-form-item>
      <el-form-item prop="sleepTime" style="width: 85%">
        <div slot="label">
          <el-popover
            placement="top-start"
            trigger="hover"
            content="每隔多久添加一个好友">
            <span slot="reference">添加延时<i class="el-icon-question"></i></span>
          </el-popover>
        </div>
        <el-input type="number" v-model="friend.sleepTime" placeholder="等待多久添加下一个">
          <template slot="append">秒</template>
        </el-input>
      </el-form-item>
      <el-form-item label="添加人数" prop="num" style="width: 85%">
        <el-input-number v-model="friend.num"></el-input-number>
      </el-form-item>
      <el-form-item style="width: 85%" v-if="index !== 0">
        <div class="right">
          <el-button type="danger" circle icon="el-icon-close" @click="deleteFriend(index)"></el-button>
        </div>
      </el-form-item>
      <el-divider></el-divider>
    </div>
    <el-form-item style="width: 85%">
      <div class="right">
        <el-button type="text" @click="addFriendParam">继续添加好友</el-button>
      </div>
    </el-form-item>

    <el-divider content-position="left">小组任务</el-divider>
    <el-form-item label="执行间隔" title="建议最少10分钟以上" prop="minutesNum" style="width: 85%">
      <el-input type="number" @change="validate10g(tasks.group.minutesNum)" min="10" v-model="tasks.group.minutesNum" placeholder="每次任务隔多久执行">
        <template slot="append">分钟</template>
      </el-input>
    </el-form-item>
    <div v-for="(group, index) in tasks.group.params" :key="index">
      <el-form-item label="搜索词" prop="msg" style="width: 85%">
        <el-input v-model="group.msg" placeholder="搜索关键词"></el-input>
      </el-form-item>
      <el-form-item label="城市" prop="city" style="width: 85%">
        <el-input v-model="group.city" placeholder="城市关键词"></el-input>
      </el-form-item>
      <el-form-item prop="sleepTime" style="width: 85%">
        <div slot="label">
          <el-popover
              placement="top-start"
              trigger="hover"
              content="每隔多久添加一个好友">
              <span slot="reference">添加延时<i class="el-icon-question"></i></span>
            </el-popover>
        </div>
        <el-input type="number" v-model="group.sleepTime" placeholder="等待多久添加下一个">
          <template slot="append">秒</template>
        </el-input>
      </el-form-item>
      <el-form-item label="添加小组数" prop="num" style="width: 85%">
        <el-input-number v-model="group.num"></el-input-number>
      </el-form-item>
      <el-form-item style="width: 85%" v-if="index !== 0">
        <div class="right">
          <el-button type="danger" circle icon="el-icon-close" @click="deleteGroup(index)"></el-button>
        </div>
      </el-form-item>
      <el-divider></el-divider>
    </div>
    <el-form-item style="width: 85%">
      <div class="right">
        <el-button type="text" @click="addGroupParam">继续添加小组</el-button>
      </div>
    </el-form-item>

    <el-form-item style="width: 85%">
      <div class="right">
        <el-button type="primary" @click="startAdd">开始执行</el-button>
      </div>
    </el-form-item>
  </el-form>
</el-drawer>
</template>

<script>
import { chooseMethod } from '../api/index.js'
import { setTimeout } from 'timers';
const { ipcRenderer } = require('electron')
export default {
  name: 'AddTask',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    defaultDevice: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      tasks: {
        friends: {
          minutesNum: 30,
          type: 'add_friends',
          params: [
            {msg: '', city: null, work: null, school: null, sleepTime: 15, num: 5}
          ]
        },
        group: {
          minutesNum: 30,
          type: 'add_tream',
          params: [
            {msg: '', city: null, sleepTime: 15, num: 5}
          ]
        }
      }
    }
  },
  methods: {
    deleteFriend (index) {
      this.tasks.friends.params.splice(index, 1)
    },
    deleteFriend (index) {
      this.tasks.friends.params.splice(index, 1)
    },
    validate10f (value) {
      if (value < 10) {
        // this.tasks.friends.minutesNum = 10
      }
    },
    validate10g (value) {
      if (value < 10) {
        this.tasks.group.minutesNum = 10
      }
    },
    addFriendParam () {
      this.tasks.friends.params.push({
        msg: '',
        city: null,
        work: null,
        school: null,
        sleepTime: 15,
        num: 5
      })
    },
    addGroupParam () {
      this.tasks.group.params.push({
        msg: '',
        city: null,
        sleepTime: 15,
        num: 5
      })
    },
    handleClose () {
      this.$emit('close')
    },
    startAdd () {
      this.tasks.friends.params.forEach(item => {
        for (let key in item) {
          if (item[key] === null) {
            delete item[key]
          }
        }
      })
      this.tasks.group.params.forEach(item => {
        for (let key in item) {
          if (item[key] === null) {
            delete item[key]
          }
        }
      })
      let friend = this.tasks.friends
      let group = this.tasks.group
      if (this.tasks.friends.params[0].msg) {
        chooseMethod(Object.assign({userId: 1}, friend, {equipments: this.defaultDevice.device_id})).then(res => {
          this.$store.dispatch('getDevicesList')
        })
        let myNotification = new Notification(this.defaultDevice.fb_nickName + '添加好友任务成功', {
          body: '即将执行第一次添加好友任务, 如有小组任务，将在5分钟后执行'
        })
        if (this.tasks.group.params[0].msg) {
          setTimeout(() => {
            chooseMethod(Object.assign({userId: 1}, group, {equipments: this.defaultDevice.device_id})).then(res => {
              this.$store.dispatch('getDevicesList')
            })
            let myNotification = new Notification(this.defaultDevice.fb_nickName + '添加小组任务成功', {
              body: '即将执行添加小组任务'
            })
            this.handleClose()
          }, 60000 * 5)
        }
        this.handleClose()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.add-task{
  /deep/ .el-drawer.rtl{
    display: flex;
    flex-direction: column;
  }
  /deep/ .el-drawer__body{
    height: calc(100% - 52px);
  }
}
.task-form{
  overflow: auto;
  height: 100%;
}
</style>

