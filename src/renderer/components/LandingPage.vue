<template>
  <div id="wrapper" class="layout-column__center">
    <div id="login"></div>
    <div style="margin-bottom: 30px;">
      <p class="logo-text" style="display:flex">
        <img src="../assets/images/logo.png" width="128px" style="align-self: center;">
        <span style="align-self: center;">泽鹿群控</span>
      </p>
    </div>
    <!-- 登录 -->
    <el-form
      v-if="isLogin"
      label-width="120px"
      label-position="left"
      size="small"
      :rules="rules"
      :model="form"
      style="width: 35%;margin: 0 auto;position: relative;"
    >
      <el-form-item label="用户名" prop="username" required>
        <el-input v-model="form.username"></el-input>
      </el-form-item>
      <el-form-item label="密 码" prop="password" required>
        <el-input type="password" v-model="form.password"></el-input>
      </el-form-item>
      <p class="right tip" @click="isLogin = false">还没有账号？</p>
      <el-form-item class="right">
        <div class="layout-row__between right">
          <a></a>
          <el-button type="primary" @click="login">登 录</el-button>
        </div>
      </el-form-item>
    </el-form>
    <!-- 注册 -->
    <el-form
      v-else
      ref="register"
      label-width="120px"
      label-position="left"
      size="small"
      :rules="registerRules"
      :model="register"
      style="width: 35%;margin: 0 auto;position: relative;"
    >
      <el-form-item label="用户名" prop="account" required>
        <el-input v-model="register.account"></el-input>
      </el-form-item>
      <!-- <el-form-item label="真实姓名" prop="realname" required>
        <el-input v-model="register.realname"></el-input>
      </el-form-item>-->
      <el-form-item label="密 码" prop="pwd" required>
        <el-input type="password" v-model="register.pwd"></el-input>
      </el-form-item>
      <p class="right tip" @click="isLogin = true">已有账号登录！</p>
      <el-form-item class="right">
        <div class="layout-row__between right">
          <a></a>
          <el-button type="primary" @click="registe">注 册</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { login, register } from "@/api/index.js";
import ParticleWave from "particle-wave";
export default {
  name: "landing-page",
  data() {
    return {
      isLogin: false,
      form: {
        username: "",
        password: ""
      },
      rules: {
        username: [
          { required: true, message: "请输入用户名", trigger: "blur" }
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      },
      register: {
        account: "",
        // realname: "",
        pwd: ""
      },
      registerRules: {
        account: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        // realname: [
        //   { required: true, message: "请输入真实姓名", trigger: "blur" }
        // ],
        pwd: [
          { required: true, message: "请输入密码", trigger: "blur" },
          { min: 6, message: "至少输入6个字符", trigger: "blur" }
        ]
      }
    };
  },
  created() {
    this.isLogin = !!this.$store.state.User.user;
  },
  mounted() {
    // let dt = new DotText(document.getElementById('logo'))
    // dt.text('FB自动化营销', {
    //   dotColor: {r: 25, g: 137, b: 250},
    //   textSize: 150
    // })

    const pointSize = 3;
    new ParticleWave(document.getElementById("login"), {
      uniforms: {
        size: { type: "float", value: pointSize },
        field: { type: "vec3", value: [0, 0, 0] },
        speed: { type: "float", value: 5 }
      },
      onResize(w, h, dpi) {
        const position = [];
        const color = [];
        const width = 400 * (w / h);
        const depth = 500;
        const height = 7;
        const distance = 9;
        for (let x = 0; x < width; x += distance) {
          for (let z = 0; z < depth; z += distance) {
            position.push(-width / 2 + x, -30, -depth / 2 + z);
            color.push(
              0,
              1 - (x / width) * 1,
              0.5 + (x / width) * 0.5,
              z / depth
            );
          }
        }
        this.uniforms.field = [width, height, depth];
        this.buffers.position = position;
        this.buffers.color = color;
        this.uniforms.size = (h / 400) * pointSize * dpi;
      }
    });
  },
  methods: {
    login() {
      if (!this.form.username || !this.form.password) {
        this.$message.error("请输入账号密码");
        return false;
      }
      let data = {
        account: this.form.username,
        pwd: this.form.password
      };
      this.$router.push("/home");
      return;
      login(data).then(res => {
        if (res.success) {
          this.$store.dispatch("set_user", res.data);
          this.$router.push("/home");
          this.$message.success("登录成功");
        } else {
          this.$message.error(res.msg);
        }
      });
    },
    registe() {
      this.$refs.register.validate(valid => {
        if (valid) {
          register(this.register)
            .then(res => {
              if (res.success) {
                this.$message({
                  message: "注册成功，请登录！",
                  type: "success"
                });
                this.isLogin = true;
              } else {
                this.$message.error(res.msg);
              }
            })
            .catch(err => {
              this.$message.error("注册失败！");
            });
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    open(link) {
      this.$electron.shell.openExternal(link);
    }
  }
};
</script>

<style lang="scss">
.logo-text {
  font-size: 60px;
  color: #fff;
  font-weight: bold;
  position: relative;
  text-shadow: 0px 3px 0px #b2a98f, 0px 14px 10px rgba(0, 0, 0, 0.15),
    0px 24px 2px rgba(0, 0, 0, 0.1), 0px 34px 30px rgba(0, 0, 0, 0.1);
}
.logo-text-sub {
  margin-top: 20px;
  color: #999;
  font-size: 24px;
  font-weight: 600;
}
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
#logo {
  margin: 0 auto;
  margin-bottom: 40px;
  width: 100%;
  height: 150px;
  position: relative;
}
.tip {
  cursor: pointer;
  font-size: 14px;
  color: #fff;
  margin-bottom: 18px;
}
#login {
  background-image: linear-gradient(rgba(30, 29, 79, 0.5), #1e1d46);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
}
body {
  font-family: "Source Sans Pro", sans-serif;
}

#wrapper {
  overflow: hidden;
  background: radial-gradient(
    ellipse at top left,
    rgba(255, 255, 255, 1) 40%,
    rgba(229, 229, 229, 0.9) 100%
  );
  height: 100vh;
  width: 100vw;
  .el-form-item__label {
    color: #fff;
  }
}

main {
  display: flex;
  justify-content: space-between;
}

main > div {
  flex-basis: 50%;
}

.left-side {
  display: flex;
  flex-direction: column;
}

.welcome {
  color: #555;
  font-size: 23px;
  margin-bottom: 10px;
}

.title {
  color: #2c3e50;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 6px;
}

.title.alt {
  font-size: 18px;
  margin-bottom: 10px;
}

.doc p {
  color: black;
  margin-bottom: 10px;
}

.doc button {
  font-size: 0.8em;
  cursor: pointer;
  outline: none;
  padding: 0.75em 2em;
  border-radius: 2em;
  display: inline-block;
  color: #fff;
  background-color: #4fc08d;
  transition: all 0.15s ease;
  box-sizing: border-box;
  border: 1px solid #4fc08d;
}

.doc button.alt {
  color: #42b983;
  background-color: transparent;
}
</style>
