<template>
    <div class="full-page">
      <div class="overlay">
        <div class="container">
          <div class="app-name">
            <h1 >QUIZ MASTER</h1>
            <hr>
          </div>
          <p class="tagline"> Please fill the below form </p>
          <form class="signup-form" @submit.prevent="signup">
            <label for="email">Email*</label>
            <input type="text" id="email" v-model="email" placeholder="example@gmail.com" required/>
            <label for="password">Password*</label>
            <input type="password" id="password" v-model="password" minlength="4" maxlength="20" placeholder="Atleast 4 and atemost 20 characters" required/>
            <label for="name">Full Name*</label>
            <input type="text" id="name" v-model="name" required/>
            <label for="dob">Date of Birth</label>
            <input type="date" id="dob" v-model="dob" />
            <button type="submit">Sign Up</button>
            <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
            <p>Already have an account? <router-link to="/">login page</router-link></p>
          </form>
        </div>
      </div>
    </div>
  </template>
  
<script>
  export default{
    data() {
        return {
          email : '' ,
          password : '',
          name : '',
          dob : '',
          errorMessage : null
        }
    },
    methods : {
        async signup() {
            const payload = {
                email : this.email,
                password : this.password,
                name : this.name,
                dob : this.dob,
            }
            try {
                const response = await fetch('/api/signup',{
                    method : "POST",
                    headers : {
                        "content-Type" : "application/json",
                    },
                    body : JSON.stringify(payload)
                })
                const result = await response.json()
                if(!response.ok) {
                    this.errorMessage = result.message || "Something went wrong";
                } else {
                    alert("Signup successfull")
                    this.$router.push('/')
                }
            } catch(error) {
                alert(error.message || "Internal server error")
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
    height: auto;
    width: 450px;
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
    margin-bottom: 2rem; /* Add more space below */
  }
  .tagline {
    font-size: 1rem; /* Bigger text */
    font-weight: bold; /* Make it bold */
    color: rgb(0, 0, 0); /* White text */
    text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5); /* Soft shadow */
    letter-spacing: 2px; /* Add spacing */
  }
  
  .signup-form input {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  .signup-form label {
    font-weight:bold ;
    display: flex;
    text-align: left;
  }
  
  .signup-form button {
    width: 100%;
    padding: 0.5rem;
    background: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .signup-form button:hover {
    background: #0056b3;
  }

</style>
  