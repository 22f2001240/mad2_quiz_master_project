<template>
    <div>
        <student-navbar/>
        <div class="container">
            <div class="filter-container">
                <span class="select-text">Select a category:</span>
                <div class="filter-buttons">
                    <button :class="{ active: activeFilter === 'subject' }" @click="filterBy('subjects')">
                        📚 Subjects
                    </button>
                    <button :class="{ active: activeFilter === 'quiz' }" @click="filterBy('quizzes')">
                        🎯 Quizzes
                    </button>
                </div>
            </div>

            <div class="search-container">
                <input v-model="searchQuery" class="search-input" :placeholder="`Search by ${activeFilter}`">
            </div>

            <!-- Filtered Results -->
            <table v-if="searchQuery && filteredCategoryItems.length" class="table-auto border-collapse  border border-gray-600">
                <thead>
                    <tr>
                        <th class="border border-gray-300 px-4 py-2">Name</th>
                        <template v-if="activeFilter=='subject'">
                            <th class="border border-gray-300 px-4 py-2">Description</th>
                            <th class="border border-gray-300 px-4 py-2">Available Chpaters</th>
                        </template>

                        <template v-if="activeFilter=='quiz'">
                            <th class="border border-gray-300 px-4 py-2">Level</th>
                            <th class="border border-gray-300 px-4 py-2">Date of Quiz</th>
                            <th class="border border-gray-300 px-4 py-2">Time of Quiz</th>
                            <th class="border border-gray-300 px-4 py-2">Time Duration</th>
                            <th class="border border-gray-300 px-4 py-2">Chapter Name</th>
                            <th class="border border-gray-300 px-4 py-2">Num of Questions</th>
                        </template>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="item in filteredCategoryItems" :key="item.id">
                        <td class="border border-gray-300 px-4 py-2">{{ item.name }}</td>
                        
                        <template v-if="activeFilter=='subject'">
                            <td class="border border-gray-300 px-4 py-2">{{ item.description || 'N/A' }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.chapters || 'N/A' }}</td>
                        </template>
                        
                        <template v-if="activeFilter=='quiz'">
                            <td class="border border-gray-300 px-4 py-2">{{ item.level || 'N/A' }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.date_of_quiz || 'N/A' }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.time_of_quiz || 0 }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.time_duration || 'Nill' }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.chapter_name  }}</td>
                            <td class="border border-gray-300 px-4 py-2">{{ item.num_questions  }}</td>
                        </template>
                        
                    </tr>
                </tbody>
                </table>

            <p v-if="searchQuery && filteredCategoryItems.length === 0">No matching results found.</p>
        </div>
    </div>
</template>

<script>
import StudentNavbar from './StudentNavbar.vue';
export default {
    components : {StudentNavbar},
    data() {
        return {
            subjects : [],
            users : [],
            quizzes : [],
            searchQuery : '',
            selectedCategory : [],
            activeFilter : 'subject',
        }
    },
    computed: {
        filteredCategoryItems() {
                let selectedCategoryItems = this.selectedCategory 
                if(this.searchQuery && this.activeFilter=='quiz'){
                    selectedCategoryItems = selectedCategoryItems.filter(item => 
                        item.name.toLowerCase().includes(this.searchQuery.toLowerCase()) && 
                        (item.num_questions>=5)
                    )
                }
                if(this.searchQuery && this.activeFilter=='subject'){
                    selectedCategoryItems = selectedCategoryItems.filter(item => 
                        item.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                    );
                }
                return selectedCategoryItems;
            }
    },
    methods : {
        async filterBy(category) {
            if (category == 'subjects') {
                this.selectedCategory = this.subjects
                this.activeFilter = 'subject'
            } 
            if (category == 'quizzes') {
                this.selectedCategory = this.quizzes
                this.activeFilter = 'quiz'
            }
            this.searchQuery = ''
        },

        async fetchSubjects() {
            try {
                const response = await fetch('/api/subject',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.subjects = result
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async fetchQuizzes() {
            try {
                const response = await fetch('/api/quiz',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.quizzes = result
                }
            } catch (error) {
                console.log(error.message)
            }
        },
        async fetchUsers() {
            try {
                const response = await fetch('/api/user',{
                    method : 'GET',
                    headers : {
                        'Content-Type' : 'application/json',
                        'Authorization' : `Bearer ${localStorage.getItem('adminToken')}`
                    }
                });
                const result = await response.json()
                if (!response.ok) {
                    alert(result.message)
                } else {
                    this.users = result
                }
            } catch (error) {
                console.log(error.message)
            }
        }
    },
    mounted() {
        this.fetchSubjects();
        this.fetchUsers();
        this.fetchQuizzes();
    }
}
</script>



<style scoped>
.container {
  max-width: 600px;
  margin: auto;
  text-align: center;
  margin-top: 15%;
}
.select-text{
    margin-right: 10px;
  font-weight: bold;
  font-size: 18px;
}
.filter-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;
}
.filter-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
button {
  padding: 8px 12px;
  margin: 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #ddd;
}
button.active {
  background-color: #007bff;
  color: white;
}

/* Search Input with Icon */
.search-container {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
}
.search-icon {
  position: absolute;
  left: 10px;
  font-size: 16px;
}
.search-input {
  width: 100%;
  padding: 8px 8px 8px 30px; /* Space for the icon */
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  padding: 5px;
  border-bottom: 1px solid #ddd;
}
p {
  color: red;
}
</style>