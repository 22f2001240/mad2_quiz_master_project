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
import Quiz from '@/components/Quiz.vue'
import CreateQuestionQuiz from '@/components/CreateQuestionQuiz.vue'
import UpdateQuestion from '@/components/UpdateQuestion.vue'
import UpdateQuiz from '@/components/UpdateQuiz.vue'
import StudentDashboard from '@/components/StudentDashboard.vue'
import StudentSubject from '@/components/StudentSubject.vue'
import StudentChapter from '@/components/StudentChapter.vue'
import StudentQuiz from '@/components/StudentQuiz.vue'
import StudentCompletedQuizzes from '@/components/StudentCompletedQuizzes.vue'
import StudentCompletedQuizDetailes from '@/components/StudentCompletedQuizDetailes.vue'
import StudentAllQuizzes from '@/components/StudentAllQuizzes.vue'
import AdminFilter from '@/components/AdminFilter.vue'
import StudentFilter from '@/components/StudentFilter.vue'
import AdminSummary from '@/components/AdminSummary.vue'
import StudentSummery from '@/components/StudentSummery.vue'
import StudentProfile from '@/components/StudentProfile.vue'

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
    },
    {
      path : '/student-dashboard',
      name : 'student-dashboard',
      component : StudentDashboard
    },
    {
      path : '/student-subject/:subject_id',
      name : 'student-subject',
      component : StudentSubject
    },
    {
      path : '/student-chapter/:chapter_id',
      name : 'student-chapter',
      component : StudentChapter
    },
    {
      path : '/student-quiz/:quiz_id',
      name : 'student-quiz',
      component : StudentQuiz
    },
    {
      path : '/student-completed-quizzes',
      name : 'student-completed-quizzes',
      component : StudentCompletedQuizzes
    },
    {
      path : '/student-quiz-detailes/:quiz_id/:score_id',
      name : 'student-quiz-detailes',
      component : StudentCompletedQuizDetailes
    },
    {
      path : '/student-all-quizzes',
      name : 'student-all-quizzes',
      component : StudentAllQuizzes
    },
    {
      path : '/admin-filter',
      name : 'admin-filter',
      component : AdminFilter
    },
    {
      path : '/student-filter',
      name : 'student-filter',
      component : StudentFilter
    },
    {
      path : '/admin-summary',
      name : 'admin-summary',
      component : AdminSummary
    },
    {
      path : '/student-summary',
      name : 'student-summary',
      component : StudentSummery
    },
    {
      path : '/student-profile',
      name : 'student-profile',
      component : StudentProfile
    },
  ],
})

export default router
