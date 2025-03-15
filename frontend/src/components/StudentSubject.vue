<template>
    <div >
        <admin-navbar/>
<!-- container for subject -->
        <div class="container">
            <h1 class="text-center">{{ subject.name }}</h1><br>
            <div class="card">
            <img class="card-img-top" :src="`/assets/${subject.name}.jpeg`" :alt="subject.name" @error="handleImageError">
            <div class="card-body">
                <p class="card-text">{{ subject.description }}</p>
            </div>
            <div class="card-body">
                <h3 class="card-text">Chapters</h3>
            </div>
            <ul v-for="chapter in subject.chapters" :key="chapter.id" class="list-group list-group-flush">
                <li class="list-group-item">{{ chapter }}</li>
            </ul>
            </div>
        </div>

        <div v-if="chapters.length > 0" class="container2">
            <h1 class="text-center">Chapters of {{ subject.name }}</h1><br>
            <div class="row row-cols-1 row-cols-md-5 g-2 ">
                <div v-for="chapter in chapters" :key="chapter.id" class="col d-flex align-items-stretch">
                    <div class="card  d-flex flex-column">
                        <div class="card d-flex flex-column h-100">
                            <router-link :to="'/student-chapter/'+chapter.id">
                                <img class="card-img-bottom" :src="'/assets/'+chapter.name+'.jpeg'" :alt="chapter.name" @error="handleImageError" >
                            </router-link><br>
                            <h5 class="card-title">{{ chapter.name }}</h5><hr>
                            <p class="card-text">{{ chapter.description }}</p>
                        </div>
                        <ul v-for="quiz in chapter.quizzes" :key="quiz.id" class="list-group list-group-flush">
                            <li class="list-group-item">{{ quiz }}</li>
                        </ul>
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
            subject : {},
            chapters : [],
            errorMessage : ''
        }
    },
    methods : {
        async fetchSubject() {
            try {
                const response = await fetch(`/api/subject/get/${this.$route.params.subject_id}`,{
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
                    this.subject = result
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async fetchChpaters() {
            try {
                const response = await fetch(`/api/subject/chapters/${this.$route.params.subject_id}`,{
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
                    this.chapters = result
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchSubject();
        this.fetchChpaters();
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
    width: fit-content;
    text-align: center;
    background-color: rgb(233, 238, 240);
    }
    .card-img-top{
        width: 100;
        height: 250px;
        object-fit: cover;
    }
    .card-img-bottom{
        width: 100;
        height: 250px;
        object-fit: cover;
    }
    .card-img-bottom:hover{
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
