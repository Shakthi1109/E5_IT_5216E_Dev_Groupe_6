<template>
  <div class="ScoreBoard">
    <h3 class="endGame"> Game Over </h3>
    <div class="grid-container">
      <div class="pastParticipations">
        <p class="pastParticipationsTitle">Past participations :</p>
        <span v-for="topScore in pastParticipations" :key="topScore.id">
          Score : {{ topScore[2] }}
        </span>
      </div>
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
      pastParticipations: [],
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
    async getParticipations(){
      try {
        const getAllParticipationsAPIResult = await quizApiService.getAllParticipations();
        if (getAllParticipationsAPIResult.status === 200) {
          const scores = getAllParticipationsAPIResult.data.scores;
          console.log("Scores " + scores);
          const lastParticipation = scores.length;
          let currentId = 0;
          for(let i=0; i<lastParticipation; i++){
            if(scores[i][1] === this.playername){
              this.pastParticipations.push(scores[i]);
            }
            if(scores[i][1] === this.playername && scores[i][0] > currentId){
              this.ranking = i+1;
              currentId = scores[i][0];                    
            }
            
          }
          if (this.ranking == 1){
            this.ranking=`${this.ranking}st`;
          }
          else if (this.ranking == 2) {
            this.ranking=`${this.ranking}nd`;
          } 
          else if (this.ranking == 3) {
            this.ranking=`${this.ranking}rd`;
          } 
          else if (this.ranking >= 4) {
            this.ranking=`${this.ranking}th`;
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
.ScoreBoard{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  color: #FFFFFF;
  text-align: center;
}

.playerName{
  margin-bottom: 2em;
  margin-left:-17em;
  text-align: center;
}
.grid-container {
  display: grid;
  width: 100%;
  grid-template-columns:15em 1fr;
}

.pastParticipations{
  margin-top: -2em;
  display: flex;
  flex-direction: column;
  border: 4px solid white; 
  padding: 10px; 
}
.pastParticipations:hover{
  background: #7ded5b;
  color: #000000;
}
.pastParticipationsTitle {
  border-bottom: 2px solid white;
  font-size: large;
}

.endGame{ 
  color: #41d215;
  margin-bottom: 1em;
  font-size: 3rem;
}
.yourScores{
  font-size: 2rem;
}
.ranking{
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
  margin-top: 1em ;
}

</style>

