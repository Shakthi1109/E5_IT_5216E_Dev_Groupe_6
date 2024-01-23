<!-- Shak -->
<template>
  <div class="wrapper-class2">
  <div class="wrapper2">
  <div class="about">
    <h1>Developers</h1>
    <div class="row">
      <div class="col-md-4">
        <div class="card">
          <img src="/src/assets/img/racer.png"/>
          <h3>Raccer</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <img src="/src/assets/img/erwan.png"/>
          <h3>Erwann</h3>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card">
          <img src="/src/assets/img/Shak.jpg"/>
          <h3>Shakthi</h3>
        </div>
      </div>
    </div>
    <p class="pAbout">The Quiz App encourages you to discover more about any topic of your choice.</p>
  </div>
  </div>
  </div>
</template>

<style>
 
 .wrapper-class2 {
  position: relative;
  height: 100vh;
  width: 100%;
  overflow: hidden; /* Add this line to prevent scrolling */
}

.wrapper2 {
  perspective: 100px;
  overflow-x: hidden;
  overflow-y: auto;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.about {
  display:grid;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 2rem;
  margin-top: 5rem;
  color: #FFFFFF;
}

h1 {
  font-size: 36px;
  margin-bottom: 30px;
}

.card {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #1e1e1f;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card img {
  display: block;
  margin: 0 auto 20px;
  border-radius: 50%;
  width: 150px;
  height: 150px;
  object-fit: cover;
}

.card h3 {
  font-size: 24px;
  margin-bottom: 10px;
}


.pAbout {
  font-size: 16px;
  margin-bottom: 20px;
  text-align: center;
}

</style>
