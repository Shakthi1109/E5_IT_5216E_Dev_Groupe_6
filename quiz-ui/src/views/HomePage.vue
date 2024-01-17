<script setup>
import { ref, onMounted } from 'vue';
import YourScore from "@/components/YourScore.vue";
import scoreService from "@/services/ScoreService";

const playerName = ref('');
const userScore = ref(0);

onMounted(async () => {
  console.log("Home page mounted");

  // Retrieve the player name from local storage
  playerName.value = scoreService.getPlayerName();

  // Fetch and display the user's score
  userScore.value = scoreService.getUserScore();
});
</script>

<template>
  <div class="home">
    <h1>Welcome to the Home Page</h1>

    <!-- Display the user's score -->
    <div class="mt-3">
      <h2>Your Score</h2>
      {{ playerName }} - {{ userScore }}
    </div>

    <!-- Include the YourScore component -->
    <YourScore />

  </div>
</template>
