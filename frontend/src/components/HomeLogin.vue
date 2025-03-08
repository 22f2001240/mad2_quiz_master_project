<template>
    <div class="full-page">
      <div class="overlay">
        <div class="container">
          <div class="app-name">
            <h1 >QUIZ MASTER</h1>
            <p class="tagline"> Enhance your skills </p>
          </div>
          <form class="login-form" @submit.prevent="login">
            <input type="text" v-model="email" placeholder="👤Username" />
            <input type="password" v-model="password" placeholder="🔗Password" />
            <button type="submit">Login</button>
            <p> 
              Don't have an account? <router-link to="/signup">Register here</router-link>
            </p>
            <div v-if="errorMessages" class="text-danger mt-3">{{ errorMessages }}</div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
<script>
  export default{
    data() {
      return {
        email : '',
        password : '',
        errorMessages : null
      }
    },
    methods : {
      async login() {
        const payload = {
          email : this.email,
          password : this.password
        }
        try {
          const response = await fetch('/api/login',{
            method : 'POST',
            headers : {
              'Content-Type' : 'application/json',
            },
            body : JSON.stringify(payload)
          });
          const result = await response.json()
          if (!response.ok) {
            this.errorMessages = result.message || "Something went wrong"
          }
          else {
            if(result.user_role == 'user'){
              alert("UserLogin Successful")
              localStorage.setItem("userToke",result.token)
              this.$router.push("user-dashboard")
            } else {
              if(result.user_role == 'admin') {
                alert("Admin Login Successful")
                localStorage.setItem("adminToken", result.token)
                this.$router.push("/admin-dashboard")
              } else {
                alert("Sorry, You are not authorized to access this page!")
              }
            }
          }
        } catch (error) {
          this.errorMessages = error.message || "Unable to connect to server"
        }
      }
    }
  }
</script>
  

<style scoped>
  .full-page {
    background-image: url("@/assets/bg11.jpeg");
    background-size: cover;
    background-position: center;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center; /* Centers horizontally */
    align-items: center; /* Centers vertically */
  }
  
  .overlay {
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .container {
    background: rgb(136, 184, 199);
    padding: 3rem;
    border-radius: 10px;
    text-align: center;
    height: 400px;
    width: 400px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    left: -25%;
  }
  
  .app-name {
    font-size: 2.5rem; /* Bigger text */
    font-weight: bold; /* Make it bold */
    color: rgb(0, 0, 0); /* White text */
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5); /* Soft shadow */
    letter-spacing: 3px; /* Add spacing */
    margin-bottom: 3rem; /* Add more space below */
  }
  .tagline {
    font-size: 0.8rem; /* Bigger text */
    font-weight: bold; /* Make it bold */
    color: rgb(0, 0, 0); /* White text */
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5); /* Soft shadow */
    letter-spacing: 4px; /* Add spacing */
  }
  
  .login-form input {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .login-form button {
    width: 100%;
    padding: 0.5rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .login-form button:hover {
    background: #0056b3;
  }

</style>
  