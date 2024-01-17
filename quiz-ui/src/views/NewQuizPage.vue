<template>
  <div class="new-quiz-page">
    <h1>Welcome to the QUIZ</h1>

    <form class="mt-3">
      <div class="mb-3">
        <label for="playerName" class="form-label">Player Name:</label>
        <input v-model="username" type="text" class="form-control" id="playerName" placeholder="Enter your name" required>
      </div>
      <button @click.prevent="submitForm" class="btn btn-primary">Submit</button>
    </form>

    <!-- Add the QuestionManager component for quiz management -->
    <QuestionManager v-if="quizStarted" />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";
import { useRouter } from 'vue-router';

// Import the QuestionManager component
import QuestionManager from "@/components/QuestionManager.vue";

const playerName = ref('');
const registeredScores = ref([]);
const username = ref('');
const quizStarted = ref(false);
const router = useRouter();

const submitForm = async () => {
  // Add logic to handle form submission and API interaction
  console.log('Player Name submitted:', username.value);
  // Save player name to local storage
  participationStorageService.savePlayerName(username.value);
  // Start the quiz
  quizStarted.value = true;
};

const launchNewQuiz = () => {
  // Save the player name before redirecting to the first question
  participationStorageService.savePlayerName(username.value);
  console.log("Launch new quiz with", username.value);
  // Start the quiz
  quizStarted.value = true;
};

onMounted(async () => {
  console.log("Home page mounted");
  // Fetch and update the list of scores
  // Example: registeredScores.value = await quizApiService.getScores();
});
</script>

<style scoped>
/* Add any custom styles for NewQuizPage.vue here */
.new-quiz-page {
  /* Add styling for the new quiz page container */
}
</style>
