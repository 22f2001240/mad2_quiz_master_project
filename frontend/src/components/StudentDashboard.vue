<template>
    <div>
        <student-navbar/>
        <div class="container">
            <h1 class="text-center">Test Your Skills</h1><br>
            <div class="row row-cols-1 row-cols-md-4 g-2 ">
                <div v-for="subject in subjects" :key="subject.id" class="col d-flex align-items-stretch">
                    <div class="card h-100 d-flex flex-column">
                        <router-link :to="'/student-subject/'+subject.id">
                        <img class="card-img-top" :src="`/assets/${subject.name}.jpeg`" :alt="subject.name" @error="handleImageError">
                        </router-link>
                        <div class="card-body flex-grow-1 " style="height: 200px;">
                            <h5 class="card-title">{{ subject.name }}</h5>
                            <p class="card-text">{{ subject.description }}</p>
                        </div>
                        <h5 v-if="subject.chapters.length > 0" class="text-center">Chapters</h5>
                        <ul v-for="chapter in subject.chapters" :key="chapter.id" class="list-group list-group-flush">
                            <li class="list-group-item">{{ chapter }}</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import StudentNavbar from './StudentNavbar.vue'
export default{
    components : {StudentNavbar},
    data() {
        return {
            subjects : [],
            errorMessage : ''
        }
    },
    methods: {
        async fetchSubjects() {
            try {
                const response = await fetch('/api/subject',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('userToken')}`
                    }
                });
                const result = await response.json();
                if (!response.ok) {
                    this.errorMessage = result.message;
                } else {
                    this.subjects = result;
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchSubjects();
    }
}
</script>

<style scoped>
    .container{
    margin-top: 50px;
    margin-bottom:50px;
    padding: 2rem;
    border-radius: 10px;
    position: relative;
    background-color: rgb(233, 238, 240);
    }
    img {
        width: 100%;
        height: 200px;
        object-fit: cover; 
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
</style>