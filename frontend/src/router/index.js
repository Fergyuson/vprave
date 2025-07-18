// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/components/LandingPage.vue'
import Result      from '@/components/Result.vue'
import PrivacyPolicy from "@/components/privacy-policy.vue";

const routes = [
    {
        path: '/',
        name: 'Landing',
        component: LandingPage
    },
    {
        path: '/result',
        name: 'Result',
        component: Result
    },
    {
        path: '/privacy-policy',
        name: 'PrivacyPolicy',
        component: PrivacyPolicy
    }
]

const router = createRouter({
    history: createWebHistory(), // чистая история (без хэша)
    routes
})

export default router
