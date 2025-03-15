<template>
    <div>
        <admin-navbar/>
        <div class="mainContainer"> 
            <div v-if="question_added" class="add-question">
                <img src="/assets/question_added.jpeg" /><br>
                <h2>Add More Questions ?</h2><br>
                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-warning" @click="addMore" >Add More</button>
                    <router-link :to="'/quiz/'+quiz.id">
                        <button type="submit" class="btn btn-warning">Go Back</button>
                    </router-link>
                </div>
            </div>
            <div v-else class="container"> 
                <h2 class="text-center">Add Question to {{ quiz.name }}({{ quiz.chapter_name }})</h2>
                <form @submit.prevent="createNewQuestion">
                    <div class="form-group">
                        <label for="question">Question</label>
                        <textarea type="text" class="form-control" id="question" minlength="6" v-model="new_question.question" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_a">Option A</label>
                        <textarea type="text" class="form-control" id="option_a" v-model="new_question.option_a" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_b">Option B</label>
                        <textarea type="text" class="form-control" id="option_b" v-model="new_question.option_b" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_c">Option C</label>
                        <textarea type="text" class="form-control" id="option_c" v-model="new_question.option_c" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_d">Option D</label>
                        <textarea type="text" class="form-control" id="option_d" v-model="new_question.option_d" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="correct_option">Select correct option</label>
                        <select id="correct_option" v-model="new_question.correct_option" class="form-select">
                            <option value="option_a">Option A</option>
                            <option value="option_b">Option B</option>
                            <option value="option_c">Option C</option>
                            <option value="option_d">Option D</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="mark">Mark for the question</label>
                        <input type="number" class="form-control" min="1" id="mark" v-model="new_question.mark" required>
                    </div>
                    <div class="form-group">
                        <label for="quiz_id">Quiz Name</label>
                        <input type="text" class="form-control" id="quiz_id" :placeholder="quiz.name" v-model="quiz_name" disabled>
                    </div>
                    <button type="submit" class="btn btn-dark w-100 mt-3">Add Question</button>
                    <p class="text-danger mt-3" v-if="errorMessage">{{ errorMessage }}</p>
                </form>
                <button type="submit" @click="goBack" class="btn btn-dark w-100 mt-3">Go Back</button>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
    export default {
        components: {AdminNavbar},
        data() {
            return {
                quiz : {},
                new_question : {
                    question : '',
                    option_a : '',
                    option_b : '',
                    option_c : '',
                    option_d : '',
                    correct_option : '',
                    mark : 1,
                    quiz_id : this.$route.params.quiz_id
                },
                question_added : false,
                errorMessage : ''
            }
        },
        methods: {
            goBack() {
                this.$router.push(`/quiz/${this.new_question.quiz_id}`)
            },
            async fetchQuiz(){
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
            },
            async createNewQuestion() {
                try {
                    const response = await fetch('/api/question',{
                        method : 'POST',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                        body : JSON.stringify(this.new_question)
                    });
                    const result = await response.json();
                    if (!response.ok) {
                        alert(result.message)
                        window.location.reload(); // Refresh the page
                    } else {
                        alert(result.message)
                        this.new_question = {
                            question : '',
                            option_a : '',
                            option_b : '',
                            option_c : '',
                            option_d : '',
                            correct_option : '',
                            mark : 1,
                            quiz_id : this.$route.params.quiz_id
                        };
                        this.question_added = true;
                    }
                } catch (error) {
                    console.log(error.message)
                }
            },
            async addMore() {
                this.question_added = false;
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
    height: 160vh;
    display: flex;
    justify-content: center; /* Center horizontally */
    align-items: center; /* Center vertically */
}
.container {
    background: rgb(136, 184, 199);
    padding: 3rem;
    border-radius: 10px;
    width: 600px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    font-weight: bold;
    font-size: 25px;
    margin-bottom: 10%;
    margin-top: 10%;
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
form button {
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
    
    color: rgb(164, 120, 37);
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
