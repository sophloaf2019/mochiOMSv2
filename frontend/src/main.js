import { createApp } from 'vue'; // Importing createApp from 'vue'
import App from './App.vue'; // Import your main App component
import router from './router'; // Import your router

const app = createApp(App); // Create the Vue app instance
app.use(router); // Use the router
app.mount('#app'); // Mount the app to the DOM
