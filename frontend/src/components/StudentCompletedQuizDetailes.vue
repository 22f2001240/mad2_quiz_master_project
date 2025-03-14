<template>
    <div>
        <student-navbar/>
<!-- for the quiz page -->
        <div class="maincontainer"> 
            <div class="container1">
                <div class="container2">
                    <div class="info-icon">ℹ</div><span> Question No. {{ currentQuestionNumber+1 }} of {{ questions.length }}</span>
                </div>
            </div>
            <div class="container4"> 
                <div> {{ currentQuestion.question }} (MCQ)</div>
            </div>
            <div class="container5">
                <div v-for="(option, index) in currentOptions"
                    :key="index"
                    :class="{ 'correct-option': option.label === currentQuestion.correct_option,
                              'wrong-option': option.label === selectedOption.selected_option && option.label !== currentQuestion.correct_option
                        }"
                    class="option">
                    <strong>{{ option.Index }}. </strong>{{ option.text }}
                </div><hr>
                <div style="text-align: end; margin-right: 10px;">
                    <p> Mark: {{ currentQuestion.mark }}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 10px;">
                        <button v-if="currentQuestionNumber > 0" class="btn btn-primary" @click="PrevQuestion">Prev.</button>
                        <button v-else class="btn btn-primary" @click="PrevQuestion" disabled>Prev.</button>
                        <button v-if="currentQuestionNumber < questions.length - 1" class="btn btn-primary" @click="NextQuestion">Next</button>
                        <button v-else class="btn btn-primary" @click="NextQuestion" disabled>Next</button>
                    </div>

                </div>
            </div><br>
            <div style="text-align: left; margin-left: 10px;">
                <button class="btn btn-danger"  @click="exitQuiz">Go Back</button>
            </div>
        </div>
    </div>
  </template>
  

<script>
import StudentNavbar from './StudentNavbar.vue';
  export default {
  components: { StudentNavbar },
    data() {
        return {
            questions: [],
            currentQuestionNumber: 0,
            selected_options: [],
        };
    },
    computed: {
        currentQuestion() {
            return this.questions[this.currentQuestionNumber] || {};
        },
        currentOptions() {
            if (!this.currentQuestion) return [];
            return [
                { Index:'A', label: "option_a", text: this.currentQuestion.option_a },
                { Index:'B', label: "option_b", text: this.currentQuestion.option_b },
                { Index:'C', label: "option_c", text: this.currentQuestion.option_c },
                { Index:'D', label: "option_d", text: this.currentQuestion.option_d },
            ];
        },
        selectedOption(){
            return this.selected_options[this.currentQuestionNumber] || {}
        }
    },
    methods: {
        async fetchQuestions() {
        try {
            const response = await fetch(`/api/quiz/question/${this.$route.params.quiz_id}`,{
                method: 'GET',
                headers : {
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                }
            });
            const result = await response.json();
            if (!response.ok) {
                alert(result.error)
            } else {
                this.questions = result.data;
            }
            } catch (error) {
                this.errorMessage = error.message;
            }
        },
        async fetchSelectedOptions() {
        try {
            const response = await fetch(`/api/subject/answers/${this.$route.params.score_id}`,{
                method: 'GET',
                headers : {
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                }
            });
            const result = await response.json();
            if (!response.ok) {
                alert(result.error)
            } else {
                this.selected_options = result;
            }
            } catch (error) {
                this.errorMessage = error.message;
            }
        },
        PrevQuestion() {
            if (this.currentQuestionNumber > 0) {
                this.currentQuestionNumber --;
            } 
        },
        
        NextQuestion() {
            if (this.currentQuestionNumber < this.questions.length - 1) {
                this.currentQuestionNumber++;
            }
        },

        exitQuiz() {
            this.$router.push('/student-completed-quizzes');
        }
    },
    mounted() {
        this.fetchQuestions();
        this.fetchSelectedOptions();
    },
  };
  </script>
  

<style scoped>
h2{
    color:rgb(86, 156, 214);
    margin-left: 20px;
}
.maincontainer {
  position: relative; 
  top: 100px;
  left: 10px;
  right: 20px;
  bottom: 20px;
  background-color: white; /* White box */
  border: 0.5px solid #f1efef;
}
.container1 {
    display: flex;
  align-items: flex-start; /* Align to the top */
  justify-content: flex-start; /* Align to the left */
}

.container2 {
  margin: 20px;
  padding: 5px;
  background-color: #f0f0f0; /* Light gray background */
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  width: fit-content; /* Adjust size based on content */
  height: fit-content;
  font-size: 20px;
  font-weight: bold;
}

.container3 {
  margin-top: 20px;
  margin-left:500px;
  padding: 5px;
  background-color: #f0f0f0; /* Light gray background */
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  width: fit-content; /* Adjust size based on content */
  height: fit-content;
  font-size: 20px;
  font-weight: bold;
}
.container4 {
  margin: 20px;
  padding: 5px;
  background-color: #f0f0f0; /* Light gray background */
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  width: 1025px ; 
  height: fit-content;
  font-size: 19px;
}
.container5 {
  margin: 20px;
  padding: 5px;
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  width: 1025px ; 
  height: fit-content;
  font-size: 19px;
  border-radius: 5px;
}
p {
  margin: 20px;
}
.info-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  background-color: black;
  color: white;
  font-size: 24px;
  font-weight: bold;
  border-radius: 50%;
  font-family: Arial, sans-serif;
}
.option {
  padding: 10px;
  margin: 5px;
  font-size: 15px;
}
.correct-option {
  background: #23a312;
}
.wrong-option {
    background-color: #dd959b; /* Red */
    color: #721c24;
}
</style>