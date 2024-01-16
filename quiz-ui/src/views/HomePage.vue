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
    <div class="about">
    <h1>This is home page</h1>
    
      <!-- Display the list of scores using v-for -->
      <div v-for="scoreEntry in registeredScores" v-bind:key="scoreEntry.date">
        {{ scoreEntry.playerName }} - {{ scoreEntry.score }}
      </div>
    </div>
  </div>
</template>