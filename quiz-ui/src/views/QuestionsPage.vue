<template>
    <div class="new-question-page">
        <h1>Page de question</h1>
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import quizApiService from "@/services/QuizApiService";
    import participationStorageService from "@/services/ParticipationStorageService";
    import { useRouter } from 'vue-router';
</script>