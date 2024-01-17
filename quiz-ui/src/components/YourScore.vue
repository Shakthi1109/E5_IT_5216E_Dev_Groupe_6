<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from "@/services/ParticipationStorageService";
import scoreService from "@/services/ScoreService";

const playerName = ref('');
const userScore = ref(0);

onMounted(() => {
  // Retrieve the player name from local storage
  playerName.value = participationStorageService.getPlayerName();
  
  // Fetch and display the user's score
  userScore.value = scoreService.getUserScore();
});
</script>
