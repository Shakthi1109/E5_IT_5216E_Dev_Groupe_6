// services/ParticipationStorageService.js

export default {
    clear() {
      // Clear all stored data
      window.localStorage.clear();
    },
    savePlayerName(playerName) {
      // Save the player name to local storage
      window.localStorage.setItem("playerName", playerName);
    },
    getPlayerName() {
      // Retrieve the player name from local storage
      return window.localStorage.getItem("playerName");
    },
    saveParticipationScore(participationScore) {
      // Save the participation score to local storage
      window.localStorage.setItem("participationScore", JSON.stringify(participationScore));
    },
    getParticipationScore() {
      // Retrieve the participation score from local storage
      const scoreString = window.localStorage.getItem("participationScore");
      return scoreString ? JSON.parse(scoreString) : null;
    }
  };
  