<template>
    <div >
        <admin-navbar/>  
        <div class="container">
            <h1 class="text-center">Subjects</h1><br>
            <div class="row row-cols-1 row-cols-md-4 g-2 ">
                <div v-for="subject in subjects" :key="subject.id" class="col d-flex align-items-stretch">
                    <div class="card h-100 d-flex flex-column">
                        <router-link :to="'/admin-subject/'+subject.id">
                        <img class="card-img-top" :src="`/assets/${subject.name}.jpeg`" :alt="subject.name" @error="handleImageError">
                        </router-link>
                        <div class="card-body flex-grow-1 " style="height: 200px;">
                            <h5 class="card-title">{{ subject.name }}</h5>
                            <p class="card-text">{{ subject.description }}</p>
                        </div>
                        <ul v-for="chapter in subject.chapters" :key="chapter.id" class="list-group list-group-flush">
                            <li class="list-group-item">{{ chapter }}</li>
                        </ul>
                        <div class="card-footer d-flex justify-content-center gap-2">
                            <router-link :to="'/admin-subject/update/'+subject.id" type="submit"  class="btn btn-dark">Update</router-link>
                            <button type="button" @click="deleteSubject(subject.id)" class="btn btn-danger">Delete</button>
                        </div>
                    </div>
                </div>
                <div class="col-12 col-md-3 d-flex align-items-stretch ">
                    <div class="card h-100 w-100 d-flex flex-column new-card">
                        <div class="card-body d-flex flex-column justify-content-center align-items-center">
                            <h5 class="card-title">Add Subject</h5><br>
                            <router-link to="/admin-subject/create" type="submit" class="btn btn-dark">➕ </router-link>
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
            subject:{
                name:''
            },
            subjects : [],
            chapters : [],
        }
    },
    methods : {
        async fetchSubjects (){
            const response = await fetch('/api/subject',{
                method : 'GET',
                headers : {
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                }
            })
            .then((response)=> response.json())
            .then(data => {
                this.subjects = data;
            })
            .catch(error => {
                console.log(error)
            })
        },
        handleImageError(event) {
      event.target.src = "/assets/default.jpeg"; // Set fallback image if not found
    },
    async deleteSubject(id) {
        const isConfirmed = window.confirm("Are you sure you want to delete the subject?")
        if (!isConfirmed){
            return // Stop the function if the admin cancels the deletion
        }
        try{
            const response = await fetch(`/api/subject/${id}`,{
                method : 'DELETE',
                headers : {
                    'Content-Type' : 'application/json',
                    'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                }
            });
            const result = await response.json()
            if(!response.ok){
                alert(result.message)
            } else {
                alert(result.message)
                this.fetchSubjects()
            }
        } catch(error){
            
        }
    },
    },
    mounted(){
        this.fetchSubjects();
    },
    components : {
        AdminNavbar
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
