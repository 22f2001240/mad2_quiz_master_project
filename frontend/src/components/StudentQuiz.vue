<template>
    <div>
        <nav class="navbar navbar-dark bg-dark">
            <h2>Quiz Master</h2>
        </nav>
<!-- For the result part -->
        <div v-if="submitted" class="resultContainer">
            <u><h1 class="text-center">Quiz Results</h1></u> <br><br>
            <h3 style="text-align: left">Total score: {{ new_score.total_score }}</h3><br>
            <h5 style="text-align: left">✅ Number of Correct Answers: {{ new_score.total_correct_answers }}</h5>
            <h5 style="text-align: left">❌ Number of Wrong Answers: {{ new_score.total_wrong_answers }}</h5><br>
            <hr>
            <h3 class="text-success text-center">Correct Answers</h3>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Question</th>
                        <th scope="col">Correct Answer</th>
                        <th scope="col">Your Answer</th>
                        <th scope="col">Mark</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(correctSubmission,index) in correctAnswers" :key="'correct-'+index">
                        <td >{{ correctSubmission.question }}</td>
                        <td>{{correctSubmission.correct_answer}}</td>
                        <td>{{correctSubmission.selected_answer}}</td>
                        <td>{{ correctSubmission.mark }}</td>
                    </tr>
                </tbody>
            </table><br>
            <h3 class="text-danger text-center">Wrong Answers</h3>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">Question</th>
                        <th scope="col">Correct Answer</th>
                        <th scope="col">Your Answer</th>
                        <th scope="col">Mark</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(wrongSubmission,index) in wrongAnswers" :key="'wrong-' +index">
                        <td>{{ wrongSubmission.question }}</td>
                        <td>{{ wrongSubmission.correct_answer  }}</td>
                        <td>{{ wrongSubmission.selected_answer }}</td>
                        <td>0</td>
                    </tr>
                </tbody>
            </table><br>
            <div style="text-align: right; margin-right: 10px;">
                <button class="btn btn-primary" @click="exitQuiz">Go Back</button>
            </div><br>
        </div>

<!-- for the quiz page -->
        <div class="maincontainer" v-else> 
            <div class="container1">
                <div class="container2">
                    <div class="info-icon">ℹ</div><span> Question No. {{ currentQuestionNumber+1 }} of {{ questions.length }}</span>
                </div>
                <div class="container3">
                    <div >⏳ Quiz ends in: {{ convertedTime }} </div>
                </div>
            </div>
            <div class="container4"> 
                <div> {{ currentQuestion.question }} (MCQ)</div>
            </div>
            <p> Choose an option:</p>
            <div class="container5">
                <div v-for="(option, index) in currentOptions"
                    :key="index"
                    @click="selectOption(option)"
                    :class="{ 'selected-option': selectedOption?.label === option.label }"
                    class="option">
                    <strong>{{ option.Index }}. </strong>{{ option.text }}
                </div><hr>
                <div style="text-align: end; margin-right: 10px;">
                    <p> Mark: {{ currentQuestion.mark }}</p>
                    <button v-if="!quiz_completed" class="btn btn-primary" @click="NextQuestion">Next</button>
                </div>
            </div>
            <div style="text-align: center; margin-right: 10px;">
                <button class="btn btn-success btn-lg" v-if="quiz_completed" @click="submitQuiz">Submit</button>
            </div><br>
            <div style="text-align: left; margin-left: 10px;">
                <button class="btn btn-danger" v-if="!quiz_completed"  @click="exitQuiz">Exit Quiz</button>
            </div>
        </div>
    </div>
  </template>
  

  <script>
  export default {
    data() {
        return {
            quiz : {},
            questions: [],
            timeLeft : 0, 
            timer: null,
            currentQuestionNumber: 0,
            selectedOption: null,
            correctAnswers: [], 
            wrongAnswers: [], 
            selectOptions:[],
            error: null, 
            new_score:{
                total_correct_answers : 0,
                total_wrong_answers : 0,
                total_score : 0,
                total_attempted_questions : 0,
            },
            question_ans : [],
            submitted : false,
            quiz_completed : false,
            
        };
    },
    computed: {
        convertedTime(){
            let hour = Math.floor(this.timeLeft / 3600);
            let minute = Math.floor((this.timeLeft % 3600) / 60);
            let second = this.timeLeft % 60;
            return `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}:${String(second).padStart(2, '0')}` //displayed in 2 digit format
        },
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
    },
    methods: {
// setup for timer
        async fetchQuiz() {
            try {
                const response = await fetch(`/api/single/quiz/${this.$route.params.quiz_id}`,{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.quiz = result
                    const storedTimeDuration = localStorage.getItem("quizTimeDuration");
                    const storedStartTime = localStorage.getItem("quizStartTime");
                    if (storedTimeDuration && storedStartTime) {
                        const elapsedTime = Math.floor((Date.now() - parseInt(storedStartTime)) / 1000); // Calculate the elapsed time and convert ms -> s
                        this.timeLeft = Math.max(0, storedTimeDuration - elapsedTime); // Prevent negative values
                    } else {
                        this.convertDurationToSeconds();
                    }
                    this.startTimer();
                }
            } catch (error) {
                console.log(error.message)
            }
        },

        convertDurationToSeconds() {
            const [hours, minutes] = this.quiz.time_duration.split(":").map(Number);
            this.timeLeft = hours * 3600 + minutes * 60; // Convert to total seconds
            localStorage.setItem("quizTimeDuration", this.timeLeft); // Save initial time
            localStorage.setItem("quizStartTime", Date.now()); // Save start timestamp in millisecond
            this.startTimer(); // Start the timer after setting timeLeft
        },

        startTimer() {
            this.timer = setInterval(() => {
                if (this.timeLeft > 0) {
                    this.timeLeft--;
                } else {
                    clearInterval(this.timer);
                    this.submitQuiz();
                }
            },1000);
        },

// For the question page
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
                this.loading = false;
            }
        },
        selectOption(option) {
            this.selectedOption = option;
        },

        NextQuestion() {
            if (!this.selectedOption) {
                alert("Please select an option before proceeding.");
                return;
            }

            this.question_ans.push({
                    question_id: this.currentQuestion.id,
                    selected_option: this.selectedOption.label,
                });

            const correctOptionLabel = this.currentQuestion.correct_option;
            const correctAnswerText = this.currentQuestion[correctOptionLabel];
            if (this.selectedOption.label === correctOptionLabel) {
                this.new_score.total_correct_answers++
                this.new_score.total_score = this.new_score.total_score + this.currentQuestion.mark
                this.correctAnswers.push({
                    question: this.currentQuestion.question,
                    mark: this.currentQuestion.mark,
                    selected_answer: this.selectedOption.text,
                    correct_answer: correctAnswerText,
                });
            } else {
                this.new_score.total_wrong_answers++
                this.wrongAnswers.push({
                    question: this.currentQuestion.question,
                    selected_answer: this.selectedOption.text,
                    correct_answer: correctAnswerText,
                });
            }
            if (this.currentQuestionNumber < this.questions.length - 1) {
                this.currentQuestionNumber++;
                this.selectedOption = null;
            } else {
                alert("Quiz completed!");
                this.quiz_completed = true
                this.new_score.total_attempted_questions = this.new_score.total_correct_answers + this.new_score.total_wrong_answers;
            }
        },

// Result page
        async submitQuiz() {
            try {
        //fetch for submit the score
                const response = await fetch(`/api/scores/${this.$route.params.quiz_id}`,{
                    method: 'POST',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    },
                    body: JSON.stringify({scores : this.new_score,question_answers : this.question_ans})
                });
                const result = await response.json();
                if (!response.ok) {
                    alert(result.message)
                } else {
                    alert(result.message);
                    this.submitted = true
                    
                }
            } catch (error) {
                console.log(error.message);
            }
        },

        exitQuiz() {
            localStorage.removeItem("quizTimeLeft");
            localStorage.removeItem("quizStartTime");
            this.$router.push('/student-dashboard');
        }
    },
    mounted() {
        this.fetchQuiz();
        this.fetchQuestions();
    },
    beforeUnmount() {
        localStorage.removeItem("quizTimeLeft");
        localStorage.removeItem("quizStartTime");
        clearInterval(this.timer) 
    }
  };
  </script>
  



<style scoped>
h2{
    color:rgb(86, 156, 214);
    margin-left: 20px;
}
.maincontainer {
  position: absolute; /* Use absolute positioning. cover the complete page */
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
  margin-left:1125px;
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
  margin-left: 20px;
  margin-right:20px;
  padding: 5px;
  background-color: #f0f0f0; /* Light gray background */
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
   
  height: fit-content;
  font-size: 19px;
}
.container5 {
  margin: 20px;
  padding: 5px;
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
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
  cursor: pointer;
}

.option:hover {
  background: #f5f5f5;
  transition: 0.5ms;

}

.selected-option {
  background: #e2e2e2;
  color: rgb(0, 0, 0);
}

.error {
  color: red;
}

.resultContainer {
  margin: 20px;
  padding: 5px;
  background-color: #f0f0f0; /* Light gray background */
  border: 1px solid #ccc;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin-top: 10px;
    background-color: #ffffff;
}
th, td {
    padding: 8px;
    border: 1px solid #ccc;
    font-size: 15px;
}

th {
    font-size: 16px;
}

</style>