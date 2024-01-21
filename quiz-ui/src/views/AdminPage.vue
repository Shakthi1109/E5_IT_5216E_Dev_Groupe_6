<!-- Admin.vue -->
<template>
    <div class="admin">
      <div v-if="!token">
        <!-- Display login form -->
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" />
        <button @click="login">Connection</button>
      </div>
      <div v-else>
        <!-- Admin mode: Display subcomponents -->
        <QuestionsList />
        <QuestionEdition :originalQuestion="selectedQuestion" />
        <QuestionAdminDisplay :question="selectedQuestion" @deleteQuestion="deleteQuestion" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import apiService from '@/services/ApiService';
  
  const token = ref(localStorage.getItem('authToken'));
  const password = ref('');
  const adminMode = ref(false);
  const selectedQuestion = ref(null);
  
  const login = async () => {
    // Implement login logic and retrieve authentication token
    const response = await apiService.login(password.value);
    if (response.token) {
      token.value = response.token;
      localStorage.setItem('authToken', response.token);
      adminMode.value = true;
    }
  };
  
  const deleteQuestion = async () => {
    // Implement delete question logic
    if (selectedQuestion.value) {
      await apiService.deleteQuestion(selectedQuestion.value.id);
      // Refresh question list or handle deletion as needed
    }
  };
  </script>
  