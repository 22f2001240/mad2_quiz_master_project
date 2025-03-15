<template>
    <div>
        <admin-navbar/>
        <div class="container">
            <h1 class="text-center">{{ quiz.name }}</h1><br>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">Under {{ quiz.chapter_name }} Chapter</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">{{ quiz.level }} Level</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">⏰  Quiz planned on {{ quiz.date_of_quiz }} at {{quiz.time_of_quiz}} (IST)</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">⏳ {{quiz.time_duration}} Hour long duration</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">{{ quiz.num_questions }} Questions are available now  </p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text" v-if="quiz.num_questions < 5">⛔ Not fit for quiz. {{5- quiz.num_questions }} more questions are required!</p>
                    <p class="card-text" v-else>✅fit for quiz. </p>
                </div>
            </div>
        </div>
        <div class="container2" >
            <h1>Questions</h1>
            <table class="table table-bordered table-dark">
                <thead>
                    <tr>
                        <th scope="col">Question ID</th>
                        <th scope="col">Question</th>
                        <th scope="col">Option A</th>
                        <th scope="col">Option B</th>
                        <th scope="col">Option C</th>
                        <th scope="col">Option D</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="question in questions" :key="question.id">
                        <td scope="row">{{ question.id }}</td>
                        <td>{{ question.question }}</td>
                        <td v-if="question.correct_option == 'option_a'" style="color: green">{{ question.option_a }}</td>
                        <td v-else>{{ question.option_a }}</td>
                        <td v-if="question.correct_option == 'option_b'" style="color: green">{{ question.option_b }}</td>
                        <td v-else>{{ question.option_b }}</td>
                        <td v-if="question.correct_option == 'option_c'" style="color: green">{{ question.option_c }}</td>
                        <td v-else>{{ question.option_c }}</td>
                        <td v-if="question.correct_option == 'option_d'" style="color: green">{{ question.option_d }}</td>
                        <td v-else>{{ question.option_d }}</td>
                        <td>
                            <router-link :to="'/update-question-quiz/'+question.id" type="button" class="btn btn-primary" >Update</router-link>
                            <button class="btn btn-danger" @click="deleteQuestion(question.id)">Delete</button>
                        </td>
                    </tr>
                </tbody>
            </table>
            <router-link :to="'/create-questions-quiz/'+quiz.id" type="button" class="btn btn-dark " >Add Question</router-link>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
export default {
    components : {AdminNavbar},
    data() {
        return {
            errorMessage : null,
            quiz : {},
            questions : []
        }
    },
    methods : {
        async deleteQuestion(id) {
            try {
                const isConfirmed = window.confirm("Are you sure you want to delete the question?");
                if (!isConfirmed){
                    return
                }
                const response = await fetch(`/api/question/${id}`,{
                    method : 'DELETE',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json();
                if (!result.message) {
                    alert(result.message);
                } else {
                    alert(result.message)
                    this.fetchQuestions();
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async fetchQuiz() {
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
        async fetchQuestions(){
            try{
                const response = await fetch(`/api/quiz/question/${this.$route.params.quiz_id}`,{
                    method: 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok){
                    alert(result.message)
                }
                else {
                    this.questions = result.data
                } 
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchQuiz();
        this.fetchQuestions();
    }
}
</script>

<style scoped>
.container{
    margin: 50px auto;
    margin-bottom:50px;
    padding: 2rem;
    border-radius: 10px;
    position: relative;
    display: flex;
    flex-direction: column;
    width: 600px;
    text-align: center;
    background-color: rgb(233, 238, 240);
    } 
.container2{
    margin: auto;
    margin-bottom:50px;
    padding: 2rem;
    border-radius: 10px;
    position: relative;
    display: flex;
    flex-direction: column;
    width: auto;
    text-align: center;
    background-color: rgb(233, 238, 240);
}
</style>