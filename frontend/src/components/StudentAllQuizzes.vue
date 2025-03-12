<template>
    <div>
        <student-navbar/>
        <div class="container">
            <h1 class="text-center">Upcoming Quizzes</h1><br>
            <div class="row row-cols-1 row-cols-md-4 g-2 ">
                <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col d-flex align-items-stretch ">
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
                            <p class="card-text">Chapter: {{ quiz.chapter_name }}</p>
                            <p class="card-text">Subject: {{ quiz.subject_name }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script> 
import StudentNavbar from './StudentNavbar.vue'
export default {
    components: {StudentNavbar},
    data () {
        return {
            quizzes: [],
            timeDiff:0,
        }
    },
    computed: {
        filteredQuizzes() {
            return this.quizzes.filter(quiz => (quiz.num_questions >=5) && (this.upCompingQuizzes(quiz)));
        }
    },
    methods: {
        upCompingQuizzes(quiz) {
            const splittedDate = quiz.date_of_quiz.split("-");
            const convertedDate = `${splittedDate[2]}-${splittedDate[1]}-${splittedDate[0]}`;
            const scheduledDateTimeString = `${convertedDate}T${quiz.time_of_quiz}`;
            const scheduledDateTime = new Date(scheduledDateTimeString);
            const currentDateTime = new Date();
            return ( scheduledDateTime > currentDateTime );
        },
        async fetchQuizzes() {
            try {
                const response = await fetch('/api/quiz', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.quizzes = result;
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchQuizzes();
    }
}
</script>

<style scoped> 
.container{
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