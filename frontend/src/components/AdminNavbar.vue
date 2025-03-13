<template>
    <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
        <div class="container-fluid d-flex align-items-center">
            <a class="navbar-brand" href="#">Quiz Master</a>
            <div class="ms-3">
                <router-link to="/admin-filter" class="custom-link" title="Filter by Category"> 🔍</router-link>
                <button title="menu" class="navbar-toggler ms-3" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
            </div>
            <div class="collapse navbar-collapse ms-3" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <router-link to="/admin-dashboard" class="nav-link active">Home</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link to="/admin-summary" class="nav-link">Summary</router-link>
                    </li>
                    <li class="nav-item"> 
                        <div @click="exportCSV" class="nav-link">Export CSV</div>
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
            localStorage.removeItem('adminToken')
            this.$router.push('/')
        },
        async exportCSV() {
            try {
                const response = await fetch('/api/quiz/export',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else{
                    alert(result.message)
                }
            } catch(error) {
                console.log(error.message)
            }
        }
    }
}
</script>

<style scoped>
.custom-link {
  text-decoration: none;
  color: inherit;
}
</style>
