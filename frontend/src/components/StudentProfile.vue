<template>
    <div class="mainContainer">
        <student-navbar/>
        <div class="container"> 
            <div class="header">
                <img class="avatar" src="/assets/Profile.jpeg" alt="Profile" />
                <div class="user-info">
                <h2>{{ user_detailes.name }}</h2>
                <p>{{ user_detailes.email }}</p>
                </div>
            </div>
            <hr>
            <div class="content">
                <div class="row">
                <span class="label">Name</span>
                <input v-model="user_detailes.name" class="input-field"  />
                </div><hr>
                <div class="row">
                <span class="label">Email account</span>
                <input v-model="user_detailes.email" class="input-field"  />
                </div><hr>
                <div class="row">
                <span class="label">Password</span>
                <input v-model="user_detailes.password" @click="passwordChanged" type="password" class="input-field"  />
                </div>
                <div class="row" v-if="isPasswordChanged">
                <span class="label">Confirm Password</span>
                <input v-model="user_detailes.confirmPassword" type="password" class="input-field"  />
                </div><hr>
                <div class="row">
                <span class="label">Date of Birth</span>
                <input v-model="user_detailes.dob" type="date" class="input-field"  />
                </div><hr>
                <div class="row">
                <span class="label">Remind Me At</span>
                <input v-model="user_detailes.reminder_time" type="time" class="input-field"  />
                </div><br>
                <p v-if="errorMessage" class="error-msg">{{ errorMessage }}</p>
            </div>
            <div>
                <button @click="submitNewDetails" class="save-btn">Save Change</button>
            </div>
        </div>
    </div>
</template>

<script>
import StudentNavbar from './StudentNavbar.vue';
export default {
    components : {StudentNavbar},
    data() {
        return {
            user_detailes: {},
            isPasswordChanged : false,
            errorMessage : null
        }
    },
    methods : {
        async fetchuser(){
            try {
                const response = await fetch('/api/single-user',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.errorMessage = null
                    this.user_detailes = result
                    this.$router.push('/student-profile')
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async submitNewDetails() {
            this.errorMessage = null
            try {
                const response = await fetch('/api/user',{
                    method : 'PUT',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    },
                    body : JSON.stringify(this.user_detailes)
                });
                const result = await response.json()
                if (!response.ok) {
                    this.errorMessage = result.message
                } else {
                    this.isPasswordChanged = false
                    alert(result.message)
                    this.$fetchuser();
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        passwordChanged()  {
            this.isPasswordChanged = true
        }
    },
    mounted() {
        this.fetchuser();
    }
}
</script>

<style scoped>
.mainContainer {
    background: linear-gradient(to bottom, rgb(5, 33, 49) 60%, white 50%);
    min-height: 100vh;
    padding-bottom: 20px;
}
.container {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    width: 500px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    top: 90px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    bottom: 100px;
  }
.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.avatar {
  border-radius: 50%;
  width: 60px;
  height: 60px;
  margin-right: 15px;
}

.user-info h2 {
  margin: 0;
  font-size: 19px;
  font-weight: bold;
}

.user-info p {
  margin: 0;
  font-size: 15px;
  color: gray;
}

.content {
  margin-bottom: 20px;
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  width: 100%;
}

.label {
  text-align: left;
  flex: 1;
  color: rgb(0, 0, 0);
  font-size: 16px;
}

.input-field {
  text-align: right;
  border: none; /* Removes the border */
  outline: none; /* Removes the outline when focused */
  background-color: transparent; /* Keeps the background clean */
  width: 100%; /* Ensures full width */
  padding-bottom: 5px; /* Optional padding for spacing */
  flex: 2;
}

.add-number {
  text-align: right;
  flex: 1;
  color: #007bff;
  cursor: pointer;
}

.save-btn {
  width: auto;
  background-color: #000000;
  color: white;
  border: none;
  padding: 10px ;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.save-btn:hover {
  background-color: #24262b;
}
.error-msg {
  color: red;
  font-size: 20px;
}
</style>