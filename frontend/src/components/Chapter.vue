<template>
    <div>
        <admin-navbar/> 
<!-- container for the chapter -->
        <div class="container">
            <h1 class="text-center">{{ chapter.name }}</h1><br>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">Subject Name: {{ chapter.subject_name }}</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text">Description: {{ chapter.description }}</p>
                </div>
            </div>
        </div>

        <!-- container for quizzes -->
        <div class="container2">
            <h1 class="text-center">Quizzes</h1><br>
            <div class="row row-cols-1 row-cols-md-4 g-2 ">
                <div v-for="quiz in quizzes" :key="quiz.id" class="col d-flex align-items-stretch ">
                    <div class="card d-flex flex-column ">
                        <router-link :to="'/quiz/'+quiz.id">
                        <img class="card-img-top" src="/assets/Quiz2.jpeg" alt="Quiz" >
                        </router-link>
                        <div class="card-body flex-grow-1" >
                            <h5 class="card-title">{{ quiz.name }}</h5>
                            <p class="card-text">{{ quiz.level }} Level</p>
                            <p class="card-text">📅 {{ quiz.date_of_quiz }}</p>
                            <p class="card-text">⏰{{ quiz.time_of_quiz }} (IST)</p>
                            <p class="card-text">⏳{{ quiz.time_duration }} Hours</p>
                            <p class="card-text">{{ quiz.num_questions }} Questions </p>
                            <p v-if="quiz.num_questions < 5" class="card-text">⛔ Not fit for quiz.</p>
                            <p v-else class="card-text">✅fit for quiz. </p>
                        </div>
                        <div class="card-footer d-flex justify-content-center gap-2">
                            <router-link :to="'/update-quiz/'+quiz.id" type="submit"  >
                                <button type="button" class="btn btn-dark">Update</button>
                            </router-link>
                            <button type="button" @click="deleteQuiz(quiz.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-3 d-flex align-items-stretch ">
                    <div class="card h-100 w-100 d-flex flex-column new-card">
                        <div class="card-body d-flex flex-column justify-content-center align-items-center">
                            <h5 class="card-title">Add Quiz</h5><br>
                            <router-link :to="'/create-quiz/'+chapter.id+'/'+chapter.name" type="submit" class="btn btn-dark">➕ </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AdminNavbar from './AdminNavbar.vue';
export default {
    data() {
        return {
            errorMessage : null,
            chapter : {},
            quizzes : []
        }
    },
    methods : {
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
            } catch (error) {
                console.log(error)
            }
        },
        async fetchQuizzes() {
            try {
                const response = await fetch(`/api/quiz/one/${this.$route.params.chapter_id}`,{
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
                    this.quizzes = result
                }
            } catch (error) {
                console.log(error)
            }
        },
        async deleteQuiz(id) {
            const isConfirmed = window.confirm("Are you sure you want to delete the quiz?")
            if (!isConfirmed){
                return
            }
            try {
                const response = await fetch(`/api/quiz/${id}`,{
                    method : 'DELETE',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    this.errorMessage = result.message
                } else {
                    this.fetchQuizzes();
                    alert(result.message);
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchChapter();
        this.fetchQuizzes();
    },
    components : {
        AdminNavbar
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
    
    img:hover{
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease-in-out;
        border-radius: 10px;
        
    }
    .new-card{
        background-color: rgb(217, 228, 231);
    }
    .container2{
    margin-top: 50px;
    margin-bottom:50px;
    margin-left: 50px;
    margin-right: 50px;
    padding: 2rem;
    border-radius: 10px;
    position: relative;
    text-align: center;
    background-color: rgb(233, 238, 240);
    }
</style>