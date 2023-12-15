<script setup>
// import TheWelcome from '../components/TheWelcome.vue'

function greet(event) {
  const request = new Request("http://127.0.0.1:5000", {
    method: "GET"
  });

  fetch(request)
    .then((response) => {
      if (response.status === 200) {
        console.log(response.json())
      }
    })
}

</script>

<template>
  <h1>Quiz App</h1>
  <p>Test your knowledge</p>
  <button @click="greet">Start</button>
</template>