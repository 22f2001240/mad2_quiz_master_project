<template>
    <div>
        <admin-navbar/>
        <div class="mainContainer">
            <div v-if="updated" class="updated">
                <img src="/assets/question_added.jpeg">
                <h2>Quiz Updated Successfully</h2><br>
                <div class="image-button"> 
                    <button type="submit" @click="ContinueEditing">Continue Editing</button> 
                    <router-link :to="'/chapter/'+quiz.chapter_id"> 
                        <button type="button">Go Back</button>
                    </router-link>
                </div>
            </div>
            <div v-else class="container"> 
                <h2 class="text-center">Update Quiz - {{ quiz.name }}</h2>
                <form @submit.prevent="updateQuiz(quiz.id)">
                    <div class="form-group">
                        <label for="name">Name of Quiz</label>
                        <input id="name" type="text" class="form-control" minlength="2" v-model="new_quiz.name" :placeholder="quiz.name">
                    </div>
                    <div class="form-group">
                        <label for="level">Level of Quiz [{{ quiz.level }}]</label>
                        <select id="level" class="form-select" v-model="new_quiz.level">
                            <option value="Beginner">Beginner</option>
                            <option value="Intermediate">Intermediate</option>
                            <option value="Advanced">Advanced</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="date_of_quiz">Date of Quiz [{{ quiz.date_of_quiz }}]</label>
                        <input id="date_of_quiz" type="date" class="form-control" v-model="new_quiz.date_of_quiz" >
                    </div>
                    <div class="form-group">
                        <label for="time_of_quiz">Time of Quiz [{{ quiz.time_of_quiz }}]</label>
                        <input id="time_of_quiz" type="time" class="form-control" v-model="new_quiz.time_of_quiz">
                    </div>
                    <div class="form-group">
                        <label for="time_duration">Time Duration [{{ quiz.time_duration }} Hours]</label>
                        <input id="time_duration" type="time" class="form-control" v-model="quiz.time_duration"  >
                    </div>
                    <div class="form-group">
                        <label for="remarks">Remarks</label>
                        <textarea id="remarks" type="text" class="form-control" v-model="new_quiz.remarks" :placeholder="quiz.remarks"></textarea>
                    </div>
                    <div class="form-group">
                        <label for="chapter_name">Chapter Name</label>
                        <input id="chapter_name" type="text" class="form-control" v-model="quiz.chapter_name" disabled/>
                    </div>
                    <button type="submit" >Update</button>
                    <p class="text-danger mt-3" style="font-size: 20px" v-if="errorMessage" >{{ errorMessage }}</p>
                </form>
                <button class="gobackbutton" type="submit" @click="goBack" >Go Back</button>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
export default {
    components : {AdminNavbar},
    data() {
        return {
            quiz : {},
            new_quiz : {},
            updated : false,
            errorMessage : ''
        }
    },
    methods : {
        goBack() {
            this.$router.push(`/chapter/${this.quiz.chapter_id}`)
        },
        async updateQuiz(id) {
            try {
                const response = await fetch(`/api/quiz/${id}`,{
                    method : 'PUT',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    },
                    body : JSON.stringify(this.new_quiz)
                });
                const result = await response.json()
                if (!response.ok) {
                    this.errorMessage = result.message
                } else {
                    this.fetchQuiz();
                    this.updated = true
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async ContinueEditing(){
            this.updated = false
        },
        async fetchQuiz() {
            this.errorMessage= ''
            try {
                const response = await fetch(`/api/single/quiz/${this.$route.params.quiz_id}`,{
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
                    this.quiz = result
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchQuiz();
    }
}
</script>

<style scoped>
.mainContainer {
    background: linear-gradient(to bottom, rgb(5, 33, 49) 50%, white 50%);
    height: 120vh;
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
    margin-bottom: 20%;
    margin-top: 20%;
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
    transform: scale(1.05); 
    transition: transform 0.3s ease-in-out;
  }
.gobackbutton {
    width: 100%;
    padding: 0.5rem;
    background: #000000;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: medium;
}
.gobackbutton:hover {
    background: #313131;
    transform: scale(1.05); 
    transition: transform 0.3s ease-in-out;
  }
.updated{
    display: flex;
    flex-direction: column;
    align-items: center; /* Center horizontally */
    justify-content: center;
    margin-top:50px;
    color: rgb(33, 133, 33);
    text-decoration: none !important;
}

img {
        width: 400px;
        height: auto;
        object-fit: cover;
        border-radius: 10px; 
    }

.image-button {
    display: flex;
    gap: 20px;
}

.image-button button {
    background-color: black; 
    color: white;             
    border: none;            
    padding: 10px 20px;       
    font-size: 16px;          
    cursor: pointer;          /* Show pointer on hover */
    border-radius: 5px;    
}

.image-button button:hover {
    background-color: #333;   
    transform: scale(1.05); 
    transition: transform 0.3s ease-in-out;
}
</style>
