<template>
    <div class="question-manager">
      <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
      <QuestionDisplay :currentQuestion="currentQuestion" @answerClicked="answerClickedHandler" />
  
      <!-- Add any additional UI elements or messages as needed -->
  
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import QuestionDisplay from "@/components/QuestionDisplay.vue";
  import quizApiService from "@/services/QuizApiService";
  
  const currentQuestion = ref(null);
  const currentQuestionPosition = ref(0);
  const totalNumberOfQuestions = ref(0);
  
  onMounted(async () => {
    // Initialize the component by loading the first question and getting the total number of questions
    await loadQuestionByPosition(1); // Assuming the first question is at position 1
  });
  
  const loadQuestionByPosition = async (position) => {
    // Retrieve the question at the specified position from the API
    currentQuestion.value = await quizApiService.getQuestionByPosition(position);
  
    // Update the current question position and total number of questions
    currentQuestionPosition.value = position;
    totalNumberOfQuestions.value = await quizApiService.getTotalNumberOfQuestions();
  };
  
  const answerClickedHandler = async (selectedAnswer) => {
    // Handle the user's selected answer (e.g., submit it to the server, update scores, etc.)
    // ...
  
    // Load the next question
    await loadQuestionByPosition(currentQuestionPosition.value + 1);
  };
  
  const endQuiz = async () => {
    // Add logic to handle the end of the quiz, e.g., display results, submit final scores, etc.
    // ...
  
    // You may also want to navigate to a results page or another appropriate route
    // router.push('/results');
  };
  </script>
  
  <style scoped>
  /* Add any custom styles for QuestionManager.vue here */
  .question-manager {
    /* Add styling for the question manager container */
  }
  </style>
  