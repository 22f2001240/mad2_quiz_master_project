<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex align-items-center">
            <a class="navbar-brand" href="#">Quiz Master</a>
            <div class="ms-3">
                <router-link to="/student-filter" class="custom-link" title="Filter by Category"> 🔍</router-link>
                <button title="menu" class="navbar-toggler ms-3" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            <div class="collapse navbar-collapse ms-3" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <router-link to="/student-dashboard" class="nav-link active">Home</router-link>
                        </li>
                        <li class="nav-item">
                            <router-link to="/student-completed-quizzes" class="nav-link">Completed Quizzes</router-link>
                        </li>
                        <li class="nav-item"> 
                            <router-link to="/student-all-quizzes" class="nav-link">All Upcoming Quizzes</router-link>
                        </li>
                        <li class="nav-item"> 
                            <router-link to="/student-summary" class="nav-link">Summary</router-link>
                        </li>
                    </ul><br>
                    <button class="btn btn-outline-light me-2" @click="logout">Logout</button>
                </div>
        </div>
    </nav>
</template>

<script>
export default {
    methods : {
        logout : function(){
            localStorage.removeItem('userToken')
            this.$router.push('/')
        },
    }
}
</script>

<style scoped>
.custom-link {
  text-decoration: none;
  color: inherit;
}
</style>