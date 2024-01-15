<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
		console.log("Home page mounted");
});
</script>

<template>
  <div>
    <h1>Home page</h1>
    
    <!-- Display the list of scores using v-for -->
    <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
      {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
    </div>
  </div>
</template>