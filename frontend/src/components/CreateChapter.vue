<template>
    <div class="mainContainer">
        <admin-navbar/>
        <div class="container" > 
            <h2 class="text-center">Create New Chapter</h2><br>
            <form @submit.prevent="createNewChapter" >
                <div class="form-group">
                    <label for="name" >Name of Chapter</label>
                    <input type="text" class="form-control" id="name" minlength="2" v-model="name" required>
                </div>
                <div class="form-group">
                    <label for="description">Description about the Chapter </label>
                    <textarea type="text" class="form-control" id="description" v-model="description"> </textarea>
                </div>
                <div class="form-group">
                    <label for="subjectName" >Subject Name</label>
                    <input type="text" class="form-control" id="subjectName" :placeholder="subject_name" v-model="subject_name" disabled>
                </div><br>
                <button type="submit" >Add</button>
                <router-link :to="'/admin-subject/'+subject_id">
                    <button type="submit" >Go Back</button>
                </router-link>
                <p class="text-danger mt-3" v-if="errorMessage" >{{ errorMessage }}</p>
            </form>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
    export default {
  components: { AdminNavbar },
        data() {
            return {
                name:'',
                description:'',
                subject_name : this.$route.params.subject_name,
                subject_id : this.$route.params.subject_id,
                errorMessage : null
            }
        },
        methods : {
            async createNewChapter() {
                const payload = {
                    name : this.name,
                    description : this.description,
                    subject_id : this.subject_id
                }
                try {
                    const response = await fetch('/api/chapter',{
                        method : 'POST',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                        body : JSON.stringify(payload)
                    });
                    const result = await response.json()
                    if (!response.ok) {
                        this.errorMessage = result.message 
                    } else {
                        alert(result.message)
                        this.name = '';
                        this.description = '';
                    }
                }catch(error) {
                    console.log(error.message)
            }
            } 
        },
    }
</script>

<style scoped>
.mainContainer {
    background: linear-gradient(to bottom, rgb(5, 33, 49) 60%, white 50%);
    min-height: 100vh;
    padding-bottom: 20px;
}
.container {
    background: rgb(136, 184, 199);
    padding: 3rem;
    border-radius: 10px;
    width: 500px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    top: 150px;
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