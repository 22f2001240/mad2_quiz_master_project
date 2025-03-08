<template>
    <div class="container-fluid">
      <div class="left-section">
        <img src="@/assets/bg2.jpg" class="top-image">
        <div class="overlay">
          <h2>Welcome to My own App</h2>
          <p>Your app description goes here.</p>
        </div>
      </div>
  
      <div class="right-section">
        <div class="login-container">
          <form class="login-form">
            <h2 class="text-center">Login</h2>
            <label>Email address</label>
            <input type="email" class="form-control" />
            <label>Password</label>
            <input type="password" class="form-control" />
            <button class="btn btn-primary w-100 mt-3">Login</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "Home2",
  };
  </script>
  
  <style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  .container-fluid {
    height: 100vh;
    display: flex;
  }
  
  .left-section {
    position: relative;
    width: 50%;
    height: 100vh;
    background: linear-gradient(to right, rgb(51, 132, 165),rgb(77, 152, 183));
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }
  
  .top-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 50vh;
    object-fit: cover;
    z-index: 1;
  }
  
  .overlay {
    position: relative;
    background: rgba(0, 0, 0, 0.5);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-top: 500px;
    z-index: 2;
  }
  
  .right-section {
    width: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  /* Login Form Container */
  .login-container {
    width: 90%;
    max-width: 400px;
    background: rgb(132, 186, 207);
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .login-form h2 {
    margin-bottom: 20px;
  }
  
  /* Button Full Width */
  .btn-primary {
    width: 100%;
  }
  </style>
  