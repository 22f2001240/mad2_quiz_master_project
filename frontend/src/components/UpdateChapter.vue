<template>
    <div>
        <admin-navbar/>
        <div class="mainContainer">
            <div class="container" > 
                <h2 class="text-center">Update Chapter</h2><br>
                <form @submit.prevent="updateChapter(chapter.id)" >
                    <div class="form-group">
                        <label for="name" >Name of Chapter</label>
                        <input type="text" class="form-control" id="name" minlength="2" v-model="chapter.name" required>
                    </div>
                    <div class="form-group">
                        <label for="description">Description about the Chapter </label>
                        <textarea type="text" class="form-control" id="description" v-model="chapter.description"> </textarea>
                    </div>

                    <div class="form-group">
                        <label for="subject_id" >Choose Subject</label>
                        <select id="subject_id" class="form-select mb-3 w-100" v-model="chapter.subject_id" required>
                            <option v-for="subject in subjects" :key="subject.id" :value="subject.id" >{{ subject.name }}</option>
                        </select>
                    </div><br>
                    <button type="submit" >Update</button>
                    <router-link :to="'/admin-subject/'+chapter.subject_id">
                        <button type="button">Go Back</button>
                    </router-link>
                    <p class="text-danger mt-3" v-if="errorMessage" >{{ errorMessage }}</p>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
    export default {
  components: { AdminNavbar },
        data() {
            return {
                chapter :{},
                subjects : [],
                errorMessage : null
            }
        },
        methods : {
            async updateChapter(id){
                const payload = this.chapter
                try {
                    const response = await fetch(`/api/chapter/crud/${id}`,{
                        method : 'PUT',
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
                        this.fetchChapter();
                        this.fetchSubjects();
                    }
                } catch (error) {
                    console.log(error.message)
                }
            },
            async fetchChapter() {
                try {
                    const response = await fetch(`/api/chapter/one/${this.$route.params.chapter_id}`,{
                        method : 'GET',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        }
                    });
                    const result = await response.json()
                    if (!response.ok) {
                        this.errorMessage = result.message
                    } else {
                        this.chapter = result
                    }
                } catch(error) {
                    console.log(error.message)
                }
            },
            async fetchSubjects (){
                const response = await fetch('/api/subject',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                })
                .then((response)=> response.json())
                .then(data => {
                    this.subjects = data;
                })
                .catch(error => {
                    console.log(error)
                })
            },
        },
        mounted(){
            this.fetchChapter();
            this.fetchSubjects();
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

