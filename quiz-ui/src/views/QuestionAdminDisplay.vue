<template>
  <div class="adminArea">
    <h1>Admin</h1>
    <div class="inputContainer" :class="{parse: passwordInvalid && showPopup }">
      <input type="password" placeholder="Password" v-model="password"/>
    </div>
    <button class="buttonConnection" @click="loginAdmin">Log in</button>
    <div v-if="showPopup" :class="{ popupInvalid: passwordInvalid }">
      <p>{{ popupMessage }}</p>
    </div>
  </div>
</template>

<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "AdminVue",
  data() {
    return {
      password: "",
      passwordInvalid: false,
      showPopup: false,
      popupMessage: ""
    };
  },

  methods: {
    async loginAdmin() {
      var body = {
        password: this.password
      };
      const loginAPIResult = await quizApiService.loginAdmin(body);
      try {
        if (loginAPIResult.status == 200) {
          window.localStorage.setItem("token", loginAPIResult.data.token);
          this.$router.push("/question-list");
        }
      } catch (error) {
        this.passwordInvalid = true;
        this.showPopup = true;
        this.popupMessage = "Password invalid";
        setTimeout(() => {
          this.showPopup = false;
          this.passwordInvalid = false;
        }, 1000);
      }
    }
  }
};
</script>

<style>
.adminArea {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  color: #ffffff;
  text-align: center;
}

.inputContainer {
  position: relative;
  width: 200px;
}

input[type="password"] {
  padding: 0.5rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  width: 100%;
  background: transparent;

  border: 2px solid #ff0000;
  color: #FFFFFF;
  font-size: 20px;
  margin-top: 15px;
}


.buttonConnection {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #41d215;
  color: rgb(255, 255, 255);
  border: none;
  cursor: pointer;
  width: 200px;
  font-size: 16px;
  margin-top: 1rem;
}

.buttonConnection:hover {
  color: #000000;
}

.buttonConnection:active {
  transform: scale(0.95);
}

.popupInvalid {
  position: fixed;
  bottom: 180px;
  width: 200px;
  height: 50px;
  color: #ff0000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}


</style>
