<template>
    <div class="mainContainer">
        <admin-navbar/>

        <div v-if="quiz_added" class="add-question">
            <img src="/assets/add_question.jpeg"/><br>
            <h2>Add More Quiz Modules ?</h2> <br>
            <div class="d-flex gap-2"> 
            <button type="submit" class="btn btn-warning" @click="addNow" >Add Now</button>
            <router-link :to="'/chapter/'+chapter_id">
                <button type="submit" class="btn btn-warning">Go Back</button>
            </router-link>
            </div>
        </div>

        <div v-else class="container mt-4"> 
            <h2 class="text-center">Create New Quiz</h2>
            <form @submit.prevent="createNewQuiz">
                <div class="form-group">
                    <label for="name">Name of Quiz</label>
                    <input type="text" class="form-control" id="name" minlength="2" v-model="name" required>
                </div>
                <div class="form-group">
                    <label for="level">Select the level</label>
                    <select id="level" v-model="level" class="form-select">
                        <option value="Beginner">Beginner</option>
                        <option value="Intermediate">Intermediate</option>
                        <option value="Advanced">Advanced</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="date_of_quiz">Date of Quiz</label>
                    <input type="date" class="form-control" id="date_of_quiz" v-model="date_of_quiz" required>
                </div>
                <div class="form-group">
                    <label for="time_of_quiz">Time of Quiz</label>
                    <input type="time" class="form-control" id="time_of_quiz" v-model="time_of_quiz" required>
                </div>
                <div class="form-group">
                    <label for="time_duration">Time Duration of Quiz</label>
                    <input type="time" class="form-control" id="time_duration" v-model="time_duration" required>
                </div>
                <div class="form-group">
                    <label for="remarks">Remarks for the Quiz</label>
                    <textarea class="form-control" id="remarks" v-model="remarks"></textarea>
                </div>
                <div class="form-group">
                    <label for="chapter_id">Chapter Name</label>
                    <input type="text" class="form-control" id="chapter_id" :placeholder="chapter_name" v-model="chapter_name" disabled>
                </div>
                <button type="submit" class="btn btn-dark w-100 mt-3">Add</button>
                <p class="text-danger mt-3" v-if="errorMessage">{{ errorMessage }}</p>
            </form>
            <button type="submit" @click="goBack" class="btn btn-dark w-100 mt-3">Go Back</button>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
export default {
    data() {
        return {
            quiz_added:false,
            added_quiz_name:'',
            added_quiz_id:'',
            name: '',
            level: '',
            date_of_quiz:'',
            time_of_quiz:'',
            time_duration: '',
            remarks: '',
            chapter_id: this.$route.params.chapter_id,
            chapter_name :this.$route.params.chapter_name,
            errorMessage : null
        }  
    },
    methods : {
        goBack() {
            this.$router.push(`/chapter/${this.chapter_id}`)
        },
        async createNewQuiz(){
            const payload = {
                name : this.name,
                level : this.level,
                date_of_quiz: this.date_of_quiz,
                time_of_quiz: this.time_of_quiz,
                time_duration: this.time_duration,
                remarks: this.remarks,
                chapter_id: this.$route.params.chapter_id,
            }
            try {
                const response = await fetch('/api/quiz',{
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
                    this.added_quiz_name = this.name;
                    this.added_quiz_id = result.quiz_id;
                    this.name = '';
                    this.level = '';
                    this.date_of_quiz = '';
                    this.time_of_quiz = '';
                    this.time_duration =  '';
                    this.remarks = '';
                    this.quiz_added = true;
                }
            } catch(error) {
                console.log(error.message)
            }
        },
        async addNow() {
            this.quiz_added = false;
        }
    },
    components:{AdminNavbar}
}
</script>

<style scoped>
.mainContainer {
    background: linear-gradient(to bottom, rgb(5, 33, 49) 65%, white 50%);
    min-height: 100vh;
    padding-bottom: 20px;
}
.container {
    background: rgb(136, 184, 199);
    padding: 2rem;
    border-radius: 10px;
    width: 600px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    margin: 40px auto;
}
form label {
    font-size: 16px;
}
form input, form select, form textarea {
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}
button {
    padding: 0.5rem;
    background: #000000;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
form button:hover {
    background: #313131;
}
.add-question{
    display: flex;
    flex-direction: column;
    align-items: center; /* Center horizontally */
    justify-content: center;
    margin-top:50px;
    color: wheat;
    text-decoration: none !important;
}
img {
        width: 300px;
        height: auto;
        object-fit: cover;
        border-radius: 10px; 
    }
button:hover{
        transform: scale(1.05);
        transition: transform 0.3s ease-in-out;   
    }
</style>