<template>
  <div>
    <div class="wrapper-class">
      <div class="wrapper">
        
        <div class="rounded-text">
          Start the Quiz ! 
          <p></p>
          <router-link to="/start-new-quiz-page" class="glow-on-hover">
              <button class="custom-button">Take Quiz</button>
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>


<style>

h2, h3 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.rounded-text {
  text-align: center;
  font-size: 24px;
  border-radius: 10px;
  padding: 20px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ffffff;
}


.custom-button {
  position: relative;
  padding: 12px 35px;
  background: #41d215;
  font-size: 17px;
  font-weight: 500;
  color: white;
  border: 3px solid #ffffff;
  border-radius: 8px;
  margin-top: 1em;
}


.custom-button:hover {
  color: #000000;
}

.custom-button:active {
  transform: scale(0.95);
}

.wrapper-class {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden;
}

.wrapper {
  perspective: 100px;
  background-color: #000000;
  overflow-x: hidden;
  overflow-y: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}


</style>