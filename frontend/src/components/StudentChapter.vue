<template>
    <div>
        <student-navbar/>
<!-- container for the chapter -->
        <div class="container">
            <h1 class="text-center">{{ chapter.name }}</h1><br>
            <div class="card">
                <img class="card-img-top" :src="`/assets/${chapter.name}.jpeg`" :alt="chapter.name" @error="handleImageError">
                <div class="card-body">
                    <p class="card-text"><span style="font-weight: bold">Subject Name: </span>{{ chapter.subject_name }}</p>
                </div>
            </div>
            <div class="card">
                <div class="card-body">
                    <p class="card-text"><span style="font-weight: bold">Description: </span>{{ chapter.description }}</p>
                </div>
            </div>
        </div>

<!-- container for quizzes -->
        <div class="container2">
            <h1 class="text-center">Quizzes</h1><br>
            <div class="row row-cols-1 row-cols-md-4 g-2 ">
                <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col d-flex align-items-stretch " :class="{'disabled-card': isCompletedQuiz(quiz)}">
                    <div v-if="isCompletedQuiz" class="card d-flex flex-column" >
                        <img class="card-img-top bottom-image" src="/assets/Quiz2.jpeg" alt="Quiz" >
                        <div class="card-body flex-grow-1" >
                            <h5 class="card-title">{{ quiz.name }}</h5>
                            <p class="card-text">{{ quiz.level }} Level</p>
                            <p class="card-text">📅 {{ quiz.date_of_quiz }}</p>
                            <p class="card-text">⏰{{ quiz.time_of_quiz }} (IST)</p>
                            <p class="card-text">⏳{{ quiz.time_duration }} Hours</p>
                            <p class="card-text">{{ quiz.num_questions }} Questions </p>
                            <p v-if="isQuizTime(quiz)">🔥 Quiz is Live Now!</p>
                            <p v-else>⛔ Quiz not Available Now!</p>
                            <router-link :to="'/student-quiz/'+quiz.id" v-if="isQuizTime(quiz)">
                                <button type="button" class="btn btn-primary" >Start</button>
                            </router-link>
                            <button type="button" v-else class="btn btn-primary" disabled>Start</button>
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
    components : {StudentNavbar},
    data() {
        return {
            chapter : {},
            quizzes : [],
            errorMessage : ''
        }
    },
    computed: {
        filteredQuizzes() {
            return this.quizzes.filter(quiz => quiz.num_questions >= 5);
        },
         // The Date() format is "Mon Mar 10 2025 09:13:04 GMT+0530 (India Standard Time)"
    },
    methods : { 
        isQuizTime(quiz) {
        const splittedDate = quiz.date_of_quiz.split("-"); // YYYY-MM-DD ["12", "03", "2025"]
        const convertedDate = `${splittedDate[2]}-${splittedDate[1]}-${splittedDate[0]}`; // 2025-03-12
        const scheduledDateTimeString = `${convertedDate}T${quiz.time_of_quiz}`; // "2025-03-12T10:15:00"
        const scheduledDateTime = new Date(scheduledDateTimeString);
        const currentDateTime = new Date();
        const timeDiff = Math.abs(scheduledDateTime - currentDateTime);
        // Check if the quiz is happening within the 1 minute
        return (
            timeDiff <= 120000 
        );
        },
        isCompletedQuiz(quiz) {
            const splittedDate = quiz.date_of_quiz.split("-");
            const convertedDate = `${splittedDate[2]}-${splittedDate[1]}-${splittedDate[0]}`
            const scheduledDateTimeString = `${convertedDate}T${quiz.time_of_quiz}`
            const scheduledDateTime =new Date(scheduledDateTimeString)
            const cutoffTime = new Date(scheduledDateTime.getTime() + 10 * 60 * 1000); // Add 10 minutes to the scheduled time
            const currentDateTime = new Date();
            return ( cutoffTime < currentDateTime)
        },
        async fetchChapter() {
            try {
                const response = await fetch(`/api/chapter/one/${this.$route.params.chapter_id}`,{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json()
                if(!response.ok) {
                    this.errorMessage = result.error
                } else {
                    this.chapter = result
                }
            } catch(error) {
                console.log(error.message)
            }
        },
        async fetchQuizzes() {
            try {
                const response = await fetch(`/api/quiz/one/${this.$route.params.chapter_id}`,{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json()
                if(!response.ok) {
                    this.errorMessage = result.error
                } else {
                    this.quizzes = result
                }
            } catch(error) {
                console.log(error.message)
            }
        }
    },
    mounted(){
        this.fetchChapter();
        this.fetchQuizzes();
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
    .card-title {
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    margin-top: 10px;
    padding: 10px;
    }
    .card-text {
    flex-grow: 1; /* Allows the description to take available space */
    text-align: center;
    font-size: 18px;
    }
    .disabled-card {
    pointer-events: none; 
    opacity: 0.6;
}

</style>