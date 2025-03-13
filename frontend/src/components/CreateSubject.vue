<template>
    <div>
        <admin-navbar/>
        <div class="mainContainer">
            <div class="container" > 
                <h2 class="text-center">Create New Subject</h2><br>
                <form @submit.prevent="createNewSubject" >
                    <div class="form-group">
                        <label for="name" >Name of Subject</label>
                        <input type="text" class="form-control" id="name" minlength="2" v-model="name" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Description about the Subject </label>
                        <textarea type="text" class="form-control" id="description" v-model="description"> </textarea>
                    </div><br>
                    <button type="submit" >Add</button>
                    <p class="text-danger mt-3" v-if="errorMessage" >{{ errorMessage }}</p>
                    <button type="submit" @click="goBack" >Go Back</button>
                </form>
            </div>
        </div>
    </div>

</template>

<script>
import AdminNavbar from './AdminNavbar.vue'
    export default{
  components: { AdminNavbar },
        data() {
            return{
                name : '',
                description : '',
                errorMessage : null,
            }
        },
        methods : {
            async createNewSubject(){
                const payload = {
                    name : this.name,
                    description : this.description
                }
                try {
                    const response = await fetch('/api/subject',{
                        method : 'POST',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                        body : JSON.stringify(payload)
                    });
                    const result = await response.json()
                    if (!response.ok){
                        this.errorMessage = result.message;
                    } else {
                        alert(result.message)
                        this.name = '';
                        this.description = '';
                        this.errorMessage = null;
                        this.$router.push('/admin-subject/create')
                    }
                } catch(error) {
                    alert(error.message)
                }
            },
            goBack() {
                this.$router.push('/admin-dashboard')
            }
        }
    }
</script>

<style scoped>
.mainContainer {
    background: linear-gradient(to bottom, rgb(5, 33, 49) 50%, white 50%);
    height: 100vh;
    display: flex;
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically */
}
.container {
    background: rgb(136, 184, 199);
    padding: 3rem;
    border-radius: 10px;
    width: 500px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    font-weight: bold;
    font-size: 25px;
}
  form label{
    font-size: 18px;
  }
  form input {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  form button {
    width: 100%;
    padding: 0.5rem;
    background: #000000;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: medium;
  }
  
  form button:hover {
    background: #313131;
  }
</style>
