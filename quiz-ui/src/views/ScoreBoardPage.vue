<!-- Shak -->
<template>
    <div class="wrapper-class">
      <div class="wrapper">
        <div class="score-container">
            <h2>Score Board</h2>
            <div class="score-board">
                <div class="score-column" v-for="column in scoreColumns" v-bind:key="column.id">
                    <div class="score-entry" v-for="scoreEntry in column.scores">
                    {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
                    </div>
                </div>
            </div>
            <div class="top-scores">
            <h2>Top Scorers</h2>            
            <div class="top-scores-list" >
                <span v-for="(bestScore, index) in topScores()">
                <img v-if="index === 0"/>
                <img v-else-if="index === 1"/>
                <img v-else-if="index === 2"/>
                - {{ bestScore.playerName }}
                </span>
            </div>
            </div>
        </div>
        </div>
    </div>
</template>
  
<script>
import quizApiService from "@/services/QuizApiService";

export default {
  name: "ScoreBoardPage",
  data() {
    return {
      registeredScores: [],
      scoreColumns: []
    };
  },
  async created() {
    var quizInfoPromise = quizApiService.getQuizInfo();
    var quizInfoAPIResult = await quizInfoPromise;
    this.registeredScores = quizInfoAPIResult.data.scores;
    this.updateScoreColumns();
    console.log("Composant Home page 'created'");
    console.log("Registered Scores :", this.registeredScores);
  },
  methods: {
    topScores() {
      const topThreeScores = this.registeredScores.slice(0, 3);
      return topThreeScores.map((score, index) => ({
        ...score,
        stars: Array(3-index).fill(0) 
      }));
    },
    updateScoreColumns() {
      const columnCount = Math.ceil(this.registeredScores.length / 10);
      this.scoreColumns = []; 
      for (let i = 0; i < columnCount; i++) {
        const start = i * 10; 
        const end = (i + 1) * 10; 
        const scores = this.registeredScores.slice(start, end); 
        this.scoreColumns.push({ id: i, scores });
      }
    }
  }
};
</script>

<style>

.wrapper-class {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  perspective: 100px;
  background-color: #000000;
  overflow-x: hidden;
  overflow-y: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}


.score-container {
  text-align: center;
}
.score-board {
  margin-bottom: 1.5rem;
  display: flex;
  flex-wrap: wrap; 
  justify-content: center;
}

.score-column {
  margin: 0 1rem;
}

.score-entry {
  margin-bottom: 0.5rem;
}

.top-scores {
  margin-bottom: 1.5rem;
  text-align: center;
}

.top-scores-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.top-scores-list span {
  display: flex;
  align-items: center;
  font-size: 24px;
}

.top-scores-list img {
  width: 40px; 
  margin-left: 20px; 
}

.top-scores-list span:not(:last-child) {
  margin-right: 10px;
}


.rounded-text {
  text-align: center;
  font-size: 24px;
  border-radius: 10px;
  padding: 20px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ffffff;
}

.go-btn {
  position: relative;
  padding: 10px 35px;
  background: #41d215;
  font-size: 17px;
  font-weight: 500;
  color: white;
  border: 1px solid #ffffff;
  border-radius: 8px;
  margin-top: 1em;
}

.go-btn:hover {
  color: #000000;
}


/* Le bouton */
.custom-button {
  position: relative;
  padding: 12px 35px;
  background: #41d215;
  font-size: 17px;
  font-weight: 500;
  color: white;
  border: 3px solid #ffffff;
  border-radius: 8px;
  margin-top: 1em;
}


.custom-button:hover {
  color: #000000;
}

</style>