import { createRouter, createWebHistory } from 'vue-router'; // Use named imports for Vue Router

const routes = [
    // Define your routes here
    { path: '/', component: () => import('./components/Home.vue') },
    { path: '/services', component: () => import('./components/Services.vue') },
];

const router = createRouter({
    history: createWebHistory(), // Set the history mode
    routes,
});

export default router; // Export the router instance
