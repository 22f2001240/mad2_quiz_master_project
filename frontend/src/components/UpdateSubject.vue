<template>
    <div class="mainContainer">
        <admin-navbar/>
        <div class="container" > 
            <h2 class="text-center">Update Subject</h2><br>
            <form @submit.prevent="updateSubject" >
                <div class="form-group">
                    <label for="name" >Name of Subject</label>
                    <input type="text" class="form-control" id="name" minlength="2" v-model="product.name" :placeholder="product.name" required>
                </div>
                <div class="form-group">
                    <label for="description">Description about the Subject </label>
                    <textarea type="text" class="form-control" id="description" v-model="product.description" :placeholder="product.description"> </textarea>
                </div><br>
                <button type="submit" >Update</button>
                <button @click="goBack" type="submit" >Go Back</button>
            </form>
            <p class="text-danger mt-3" v-if="errorMessage" >{{ errorMessage }}</p>
        </div>
    </div>   
</template>

<script>
import AdminNavbar from './AdminNavbar.vue'
export default{
  components: { AdminNavbar },
        data() {
            return {
                product : {
                    name : '',
                    description : ''
                },
                errorMessage : null,
            }
        },
        methods : {
            goBack() {
                this.$router.push('/admin-dashboard')
            },
            async updateSubject(){
                this.errorMessage = ''
                const payload = {
                    name : this.product.name,
                    description : this.product.description
                }
                try {
                    const response = await fetch(`/api/subject/${this.$route.params.id}`,{
                        method : 'PUT',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                        body : JSON.stringify(payload)
                    });
                    const result = await response.json()
                    if (!response.ok) {
                        this.errorMessage = result.message
                    } else {
                        alert(result.message)
                        this.$router.push('/admin-dashboard')
                    }
                } catch (error) {
                    console.log(error.message)
                }
            },
            async fetchSubject() {
                try {
                    const response = await fetch(`/api/subject/get/${this.$route.params.id}`,{
                        method : 'GET',
                        headers : {
                            'Content-Type' : 'application/json',
                            'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                        },
                    });
                    const result = await response.json()
                    if(!response.ok) {
                        alert(result.error)
                    } else {
                        this.product.name = result.name
                        this.product.description = result.description
                    }
                } catch(error){
                    console.log(error.message)
                }
            },
    },
    mounted() {
        this.fetchSubject();
        }
}
</script>

<style scoped>
p {
    font-size: 16px;
}
.mainContainer{
    background: rgb(5, 33, 49);
}
.container {
    background: rgb(136, 184, 199);
    padding: 3rem;
    border-radius: 10px;
    width: 500px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
    position: relative;
    top: 150px;
    font-weight: bold;
    font-size: 25px;
  }
  form label{
    font-size: 18px;
  }
  form input {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  form button {
    width: 100%;
    padding: 0.5rem;
    background: #000000;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: medium;
  }
  
  form button:hover {
    background: #313131;
  }
</style>