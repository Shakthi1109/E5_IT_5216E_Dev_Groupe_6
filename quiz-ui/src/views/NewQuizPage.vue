<template>
  <div class="newQuizPage">
    <form>
      <div class="mb-3">
        <input class="inputName" required type="text" id="playerName" placeholder="Username"
          v-model="username" />
      </div>
      <button :disabled="!username" @click="launchNewQuiz" type="submit" class="designButton">
        Start
      </button>
    </form>
  </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";

export default {
  name: 'NewQuizPage',
  data() {
    return {
      username: ''
    };
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      console.log("Launch new quiz with", participationStorageService.getPlayerName());
      this.$router.push('/questions');
    },
  }
}
</script>


<style>
.newQuizPage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  color: #FFFFFF;
  text-align: center;
}


.inputName {
  width: 300px;
  height: 60px;
  padding: 0 20px;
  background: transparent;
  border-radius: 8px;
  border: 2px solid #ff0000;
  color: #FFFFFF;
  font-size: 20px;
  margin-bottom: 20px;
}
.inputName:valid {
  border-color: #0dff00;
}

.designButton {
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

.designButton:hover {
  color: #000000;
}

.designButton:active {
  transform: scale(0.95);
}

</style>
