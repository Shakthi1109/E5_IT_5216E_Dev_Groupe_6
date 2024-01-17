<template>
  <div class="question-display" v-if="currentQuestion">
    <h2>{{ currentQuestion.questionText }}</h2>
    <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question Image" />
    <ul>
      <li v-for="answer in currentQuestion.answers" :key="answer.id" @click="handleAnswerClick(answer)">
        {{ answer.text }}
      </li>
    </ul>
    <a @click="emit('answer-clicked', 2)">La réponse D</a>
  </div>
  <div v-else>
    <!-- Handle the case when currentQuestion is null -->
    <p>No question available</p>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  currentQuestion: Object
});
const emit = defineEmits();

const handleAnswerClick = (selectedAnswer) => {
  // Emit the answerClicked event with the selected answer
  emit('answer-clicked', selectedAnswer);
};
</script>

<style scoped>
/* Add any custom styles for QuestionDisplay.vue here */
.question-display {
  /* Add styling for the question display container */
}

.question-display img {
  /* Add styling for the question image */
  max-width: 100%;
  height: auto;
}
</style>
