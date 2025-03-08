import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/HomeLogin.vue'
import Signup from '@/components/Signup.vue'
import AdminDashboard from '@/components/AdminDashboard.vue'
import CreateSubject from '@/components/CreateSubject.vue'
import UpdateSubject from '@/components/UpdateSubject.vue'
import Subject from '@/components/Subject.vue'
import CreateChapter from '@/components/CreateChapter.vue'
import UpdateChapter from '@/components/UpdateChapter.vue'
import Chapter from '@/components/Chapter.vue'
import CreateQuiz from '@/components/CreateQuiz.vue'
import CreateQuestion from '@/components/CreateQuestion.vue'
import Quiz from '@/components/Quiz.vue'
import CreateQuestionQuiz from '@/components/CreateQuestionQuiz.vue'
import UpdateQuestion from '@/components/UpdateQuestion.vue'
import UpdateQuiz from '@/components/UpdateQuiz.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path : '/',
      name : 'home',
      component : Home,
    },
    {
      path : '/signup',
      name : "signup",
      component : Signup
    },
    {
      path : '/admin-dashboard',
      name : 'admin-dashboard',
      component : AdminDashboard
    },
    {
      path : '/admin-subject/create',
      name :'create-subject',
      component : CreateSubject
    },
    {
      path : '/admin-subject/update/:id',
      name : 'update-subject',
      component : UpdateSubject
    },
    {
      path : '/admin-subject/:id',
      name : 'admin-subject',
      component : Subject
    },
    {
      path : '/chapter-create/:subject_id/:subject_name',
      name : 'chapter-create',
      component : CreateChapter
    },
    {
      path : '/chapter-update/:subject_id/:subject_name/:chapter_id',
      name : 'chapter-update',
      component : UpdateChapter
    },
    {
      path : '/chapter/:chapter_id',
      name : 'chapter',
      component : Chapter
    },
    {
      path : '/create-quiz/:chapter_id/:chapter_name',
      name : 'create-quiz',
      component : CreateQuiz
    },
    {
      path : '/create-question/:chapter_id/:chapter_name/:quiz_id/:quiz_name',
      name : 'create-question',
      component : CreateQuestion
    },
    {
      path : '/quiz/:quiz_id',
      name : 'quiz',
      component : Quiz
    },
    {
      path : '/create-questions-quiz/:quiz_id',
      name : 'create-questions-quiz',
      component : CreateQuestionQuiz
    },
    {
      path : '/update-question-quiz/:question_id',
      name : 'update-question-quiz',
      component : UpdateQuestion
    },
    {
      path : '/update-quiz/:quiz_id',
      name : 'update-quiz',
      component : UpdateQuiz
    }
  ],
})

export default router
