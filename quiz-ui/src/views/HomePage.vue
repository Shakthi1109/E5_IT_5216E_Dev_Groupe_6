<template>
  <div class="wrapper-class1">
    <div class="wrapper1">
      <div class="content-container">
        <div class="rounded-text1">
          Start the Quiz !
          <p></p>
          <router-link to="/start-new-quiz-page" class="glow-on-hover">
            <button class="custom-button1">Take Quiz</button>
          </router-link>
        </div>

        <div class="top-scores1">
          <h4>Top 3 Players</h4>
          <div class="top-scores-list1">
            <span v-for="(bestScore, index) in topScores()" :key="index">
              <span v-if="index === 0">1st</span>
              <span v-else-if="index === 1">2nd</span>
              <span v-else-if="index === 2">3rd</span>
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
  name: "HomePage",
  data() {
    return {
      registeredScores: [],
      scoreColumns: [] // Tableau pour stocker les colonnes de scores
    };
  },
  async created() {
    var quizInfoPromise = quizApiService.getQuizInfo();
    var quizInfoAPIResult = await quizInfoPromise;
    this.registeredScores = quizInfoAPIResult.data.scores;
    this.updateScoreColumns(); // Appeler la fonction pour mettre à jour les colonnes de scores
    console.log("Composant Home page 'created'");
    console.log("Registered Scores :", this.registeredScores);
  },
  methods: {
    topScores() {
      const topThreeScores = this.registeredScores.slice(0, 3); // Récupérer uniquement les trois premiers scores
      return topThreeScores.map((score, index) => ({
        ...score,
        stars: Array(3-index).fill(0) // Générer un tableau avec le nombre d'étoiles correspondant au score
      }));
    },
    updateScoreColumns() {
      const columnCount = Math.ceil(this.registeredScores.length / 10); // Calculer le nombre de colonnes nécessaires
      this.scoreColumns = []; // Réinitialiser le tableau des colonnes
      for (let i = 0; i < columnCount; i++) {
        const start = i * 10; // Indice de début de la colonne
        const end = (i + 1) * 10; // Indice de fin de la colonne
        const scores = this.registeredScores.slice(start, end); // Extraire les scores pour la colonne actuelle
        this.scoreColumns.push({ id: i, scores }); // Ajouter la colonne au tableau des colonnes
      }
    }
  }
};
</script>

<style>
h2,
h3 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

h4 {
  color: #ffffff;
}

.content-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 100vh; /* Use full height of the viewport */
}

.rounded-text1 {
  text-align: center;
  font-size: 24px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
}

.custom-button1 {
  padding: 12px 35px;
  background: #41d215;
  font-size: 17px;
  font-weight: 500;
  color: white;
  border: 3px solid #ffffff;
  border-radius: 8px;
  margin-top: 1em;
  cursor: pointer;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
}

.custom-button1:hover {
  color: #000000;
}

.top-scores1 {
  text-align: center;
  font-size: 24px;
  color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  padding: 20px;
}

.top-scores-list1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  font-size: 24px;
  color: #ffffff;
  padding: 20px;
}

.top-scores-list1 span {
  display: flex;
  align-items: center;
  font-size: 24px;
}


</style>