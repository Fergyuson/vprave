// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { MaskInput } from 'vue-3-mask';

const app = createApp(App);

// Регистрируем глобальный компонент 'MaskInput'
app.component('MaskInput', MaskInput);

// Подключаем роутер к этому же экземпляру приложения
app.use(router);

// Монтируем единственный экземпляр
app.mount('#app')
