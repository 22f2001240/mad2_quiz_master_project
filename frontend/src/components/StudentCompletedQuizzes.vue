<template>
    <div>
        <student-navbar/>
        <div class="container2" >
            <h1>Completed Quizzes</h1><br>
            <table class="table table-bordered table-dark">
                <thead>
                    <tr style="font-size: 15px;">
                        <th scope="col">Quiz Name</th>
                        <th scope="col" >Subject Name</th>
                        <th scope="col">Chapter Name</th>
                        <th scope="col">Date and Time</th>
                        <th scope="col">Total Correct Answers</th>
                        <th scope="col">Total Wrong Answers</th>
                        <th scope="col">Number of Attempted Questions</th>
                        <th scope="col">Total Score Earned</th>
                        <th scope="col">Total Score</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="score in scores" :key="score.id">
                        <td>
                            <router-link :to="'/student-quiz-detailes/'+score.quiz_id" class="remove-link"> {{ score.quiz_name }} </router-link>
                        </td>
                        <td scope="row">{{ score.subject_name }}</td>
                        <td>{{ score.chapter_name }}</td>
                        <td>{{ score.submitted_at }}</td>
                        <td style="color: green; font-weight: bold">{{ score.total_correct_answers }}</td>
                        <td style="color: red">{{ score.total_wrong_answers }}</td>
                        <td>{{ score.total_attempted_questions }}</td>
                        <td>{{ score.total_score }}</td>
                        <td>{{ score.total_quiz_score }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
    </div>
</template>

<script>
import StudentNavbar from './StudentNavbar.vue'
export default {
    components : {StudentNavbar},
    data() {
        return {
            scores : [],
            quizzes: {},
        }
    },
    methods: {
        async fetchScores() {
            try {
                const response = await fetch('/api/scores',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.scores = result;
                }
            } catch(error) {
                console.log(error.message)
            }
        },
        async fetchQuizzes(){
            try{
                const response = await fetch('/api/quiz/student/score',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.quizzes = result;
                }
            } catch (error){
                console.log(error.message)
            }
        },

        async fetchQuestions(quiz_id) {
            try {
                const response = await fetch(`/api/quiz/question/${quiz_id}`,{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    alert(result.message)
                } else {
                    return result.data.reduce((acc, question) => acc + question.score, 0);
                    }
            } catch(error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchScores();
        this.fetchQuizzes();
    }
}
</script>


<style scoped>
    .container2{
        margin-top: 50px;
        margin-bottom:50px;
        padding: 1rem;
        border-radius: 10px;
        position: relative;
        display: flex;
        flex-direction: column;
        width: auto;
        text-align: center;
        background-color: rgb(233, 238, 240);
    }
    .remove-link{
        text-decoration: none;
        /* color: inherit; */
    }
</style>