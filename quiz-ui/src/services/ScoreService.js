// services/ScoreService.js
const SCORE_KEY = 'userScore';

export default {
  // Save the user's score to localStorage
  saveUserScore(score) {
    window.localStorage.setItem(SCORE_KEY, score.toString());
  },

  // Retrieve the user's score from localStorage
  getUserScore() {
    const storedScore = window.localStorage.getItem(SCORE_KEY);
    return storedScore ? parseInt(storedScore, 10) : 0;
  },

  // Clear the user's score from localStorage
  clearUserScore() {
    window.localStorage.removeItem(SCORE_KEY);
  },
};
