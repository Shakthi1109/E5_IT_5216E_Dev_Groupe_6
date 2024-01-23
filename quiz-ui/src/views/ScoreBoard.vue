<template>
  <div class="ScoreBoard">
    <h3 class="endGame"> Game Over </h3>
    <div class="grid-container">
      <div class="playerName">
        <h2>Pseudo : {{ playername }}</h2>
        <p class="yourScores">Your score : {{ sessionScore }}</p>
        <p class="ranking">Ranking : {{ ranking }}</p>
      </div>
    </div>
  </div>
</template>
  
<script>
import quizApiService from "@/services/QuizApiService.js";
import participationStorageService from "@/services/ParticipationStorageService.js"
export default {
  name: 'ScorePage',
  data() {
    return {
      playername: "",
      ranking: 0,
      sessionScore: 0,
      registeredScores: []
    };
  },
  async created() {
    this.sessionScore = this.$route.params.score;
    this.playername = participationStorageService.getPlayerName();
    this.getParticipations();
  },
  methods: {
    backToHomePage() {
      participationStorageService.clear();
      this.$router.push('/');
    },
    async getParticipations() {
      try {
        const getAllParticipationsAPIResult = await quizApiService.getAllParticipations();

        if (getAllParticipationsAPIResult.status === 200) {
          const scores = getAllParticipationsAPIResult.data;
          if (scores == null || scores.length <= 0) {
            this.ranking = 1;
            return;
          }

          this.ranking = scores.length + 1;

          for (let i = 0; i < scores.length; i++) {
            if (scores[i][3] <= sessionScore) {
              this.ranking -= 1;
            }
          }

          if (this.ranking == 1) {
            this.ranking = `${this.ranking}st`;
          }
          else if (this.ranking == 2) {
            this.ranking = `${this.ranking}nd`;
          }
          else if (this.ranking == 3) {
            this.ranking = `${this.ranking}rd`;
          }
          else if (this.ranking >= 4) {
            this.ranking = `${this.ranking}th`;
          }
        }
        else {
          console.error("Error retrieving quiz scores");
        }
      } catch (error) {
        console.error("Error during API request", error);
      }
    }
  },
};
</script>
<style>
.ScoreBoard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  color: #FFFFFF;
  text-align: center;
}

.playerName {
  margin-bottom: 2em;
  margin-left: -17em;
  text-align: center;
}

.grid-container {
  display: grid;
  width: 100%;
  grid-template-columns: 15em 1fr;
}

.endGame {
  color: #41d215;
  margin-bottom: 1em;
  font-size: 3rem;
}

.yourScores {
  font-size: 2rem;
}

.ranking {
  font-size: 2rem;
}

.custom-button-scoreboard {
  position: relative;
  padding: 24px 70px;
  background: #ffffff;
  font-size: 40px;
  font-weight: 500;
  color: rgb(0, 0, 0);
  border-radius: 8px;
  margin-top: 1em;
}
</style>

