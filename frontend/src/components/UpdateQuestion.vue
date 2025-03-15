<template>
    <div>
        <admin-navbar/>
        <div class="mainContainer">
            <div class="container" >  
                <h2 class="text-center">Update Question</h2>
                <form @submit.prevent="updateQuestion(question.id)">
                    <div class="form-group">
                        <label for="question">Question</label>
                        <textarea type="text" class="form-control" id="question" minlength="6" v-model="question.question" :placeholder="question.question" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_a">Option A</label>
                        <textarea type="text" class="form-control" id="option_a" v-model="question.option_a" :placeholder="question.option_a" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_b">Option B</label>
                        <textarea type="text" class="form-control" id="option_b" v-model="question.option_b" :placeholder="question.option_b" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_c">Option C</label>
                        <textarea type="text" class="form-control" id="option_c" v-model="question.option_c" :placeholder="question.option_c" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="option_d">Option D</label>
                        <textarea type="text" class="form-control" id="option_d" v-model="question.option_d" :placeholder="question.option_d" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="correct_option">Select correct option</label>
                        <select class="form-select" id="correct_option" v-model="question.correct_option" >
                            <!-- <option :value="question.correct_option" disabled selected>{{ question.correct_option || 'Select an option'}}</option> -->
                            <option value="option_a">Option A</option>
                            <option value="option_b">Option B</option>
                            <option value="option_c">Option C</option>
                            <option value="option_d">Option D</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="mark">Mark for the question</label>
                        <input type="number" class="form-control" min="1" id="mark" v-model="question.mark" required>
                    </div>
                    <div class="form-group">
                        <label for="quiz_id">Quiz Name</label>
                        <input type="text" class="form-control" id="quiz_id" :placeholder="question.quiz_name" disabled>
                    </div>
                    <button type="submit" class="w-100 mt-3">Update Question</button>
                    <router-link :to="'/quiz/'+question.quiz_id">
                        <button  type="button" >Go Back</button>
                    </router-link>
                    <p class="text-danger mt-3" v-if="errorMessage">{{ errorMessage }}</p>
                </form>
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
            question : {},
            errorMessage : ''
        }
    },
    methods: {
        async updateQuestion(id) {
            this.errorMessage = ''
            try {
                const response = await fetch(`/api/question/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
                    },
                    body: JSON.stringify(this.question)
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message;
                } else {
                    alert(result.message)
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async fetchQuestion(){
            try {
                const response = await fetch(`/api/single/question/${this.$route.params.question_id}`,{
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
                    this.question = result
                }
            } catch (error) {
                console.log(error.message)
            }
        },
    },
    mounted() {
        this.fetchQuestion();
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
form label {
    font-size: 18px;
}
form input, form select, form textarea {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
}
</style>