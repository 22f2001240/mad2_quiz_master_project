<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Quiz Master</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link to="/admin-dashboard" class="nav-link active">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/student-completed-quizzes" class="nav-link">Completed Quizzes</router-link>
                    </li>
                    <li class="nav-item"> 
                        <router-link to="/create-quiz" class="nav-link">Create new quiz</router-link>
                    </li>
                </ul>
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
