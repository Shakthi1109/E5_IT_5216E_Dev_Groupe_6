<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const playerName = ref('');
const registeredScores = ref([]);
const username = ref('');

const submitForm = async () => {
  // Add logic to handle form submission and API interaction
  console.log('Player Name submitted:', username.value);
  // Call your API service or perform other actions here
};

const launchNewQuiz = () => {
  console.log("Launch new quiz with", username.value);
  // Add logic to store the player name and redirect to the first question of the quiz
  // Example: storePlayerName(username.value);
  // Example: redirect('/quiz/1');
};

onMounted(async () => {
  console.log("Home page mounted");
  // Fetch and update the list of scores
  // Example: registeredScores.value = await quizApiService.getScores();
});
</script>

<template>
  <div class="home">
    <h1>Welcome to the Home Page</h1>

    <form @submit.prevent="submitForm" class="mt-3">
      <div class="mb-3">
        <label for="playerName" class="form-label">Player Name:</label>
        <input v-model="username" type="text" class="form-control" id="playerName" placeholder="Enter your name" required>
      </div>
      <button @click="launchNewQuiz" type="submit" class="btn btn-primary">Submit</button>
    </form>

    <!-- Display the list of scores -->
    <div v-if="registeredScores.length === 0" class="mt-3">No scores available.</div>
    <div v-else class="mt-3">
      <h2>Top Scores</h2>
      <div v-for="scoreEntry in registeredScores" :key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>
  </div>
</template>
