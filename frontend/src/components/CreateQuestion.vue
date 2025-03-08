<template>
    <div class="mainContainer">
        <admin-navbar/>
        <div v-if="question_added" class="add-question">
            <img src="/assets/question_added.jpeg" /><br>
            <h2>Add More Questions ?</h2><br>
            <div class="d-flex gap-2">
                <button type="submit" class="btn btn-warning" @click="addMore" >Add More</button>
                <router-link :to="'/chapter/'+chapter_id">
                    <button type="submit" class="btn btn-warning">Go Back</button>
                </router-link>
            </div>
        </div>
        <div v-else class="container mt-4"> 
            <h2 class="text-center">Add Question to {{ quiz_name }}</h2>
            <form @submit.prevent="createQuestion">
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
                    <input type="text" class="form-control" id="quiz_id" :placeholder="quiz_name" v-model="quiz_name" disabled>
                </div>
                <button type="submit" class="btn btn-dark w-100 mt-3">Add Question</button>
                <p class="text-danger mt-3" v-if="errorMessage">{{ errorMessage }}</p>
            </form>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
export default {
    components : {AdminNavbar},
    data() {
        return {
            question_added : false,
            quiz_name : this.$route.params.quiz_name,
            chapter_id: this.$route.params.chapter_id,
            chapter_name :this.$route.params.chapter_name,
            new_question : {
                question : '',
                option_a : '',
                option_b : '',
                option_c : '',
                option_d : '',
                correct_option : '',
                mark : 1,
                quiz_id : this.$route.params.quiz_id,
             }
        }
    },
    methods : {
        async addMore() {
            this.question_added = false
        },
        async createQuestion() {
            try {
                const response = await fetch('/api/question',{
                    method : 'POST',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    },
                    body : JSON.stringify(this.new_question)
                });
                const result = await response.json()
                if (!response.ok) {
                    this.errorMessage = result.message;
                } else {
                    alert(result.message);
                    this.new_question = {
                            question : '',
                            option_a : '',
                            option_b : '',
                            option_c : '',
                            option_d : '',
                            correct_option : '',
                            mark : 1,
                            quiz_id : this.$route.params.quiz_id,
                        }
                    this.question_added = true;
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
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
