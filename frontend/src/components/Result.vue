<template>
  <div class="result-page">
    <!-- БЛОК 1: картинка (с анимацией, с градиентной маской внизу) -->
    <div class="logo-block">
      <img
          src="/img/logo_norm.png"
          alt="Логотип компании"
          class="logo-image"
      />
      <!-- Градиентная маска, «закрывающая» нижнюю часть картинки -->
      <div class="gradient-mask"></div>
    </div>

    <!-- БЛОК 2: остальной контент с эффектом fade-in -->
    <div class="content-block">
      <span class="thank-you">Спасибо за обращение!</span>
      <p class="result-text">
        Это компания ООО «Я ВПРАВЕ», ваш результат почти готов!<br>
        Вам поступит СМС-сообщение с подробностями. После этого с вами свяжется наш
        юрист на 2–5 минут для уточнения дальнейших шагов.
      </p>
      <p class="contact-phone">
        Телефон для срочной связи:
        <a class="phone-link" href="tel:+74954316699">8 (495) 431-66-99</a>
      </p>
      <router-link class="back-link" to="/">Вернуться на главную</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ResultPage'
}
</script>

<style scoped>
/* === ОБЩИЕ ПЕРЕМЕННЫЕ И ШРИФТЫ (по желанию) === */
:root {
  --primary-color: #42b983;       /* основной зелёный для кнопки */
  --primary-hover: #369566;       /* немного темнее для hover */
  --text-color: #333;             /* цвет основного текста */
  --bg-content: #f7f7f7;          /* фон контент-блока */
}

/* === КОНТЕЙНЕР ВСЕЙ СТРАНИЦЫ === */
.result-page {
  display: flex;
  flex-direction: column;
  margin: 0;
  padding: 0;
  width: 100%;
  overflow-x: hidden;
  background-color: #fff;
}

/* === БЛОК 1: ЛОГО-КАРТИНКА === */
.logo-block {
  position: relative;
  width: 100%;
  /* Ограничим высоту картины — например, до 60vh,
     чтобы при очень широких экранах картинка не получалась «гигантской». */
  height: 60vh;
  min-height: 300px;
  max-height: 600px;
  overflow: hidden;
  background-color: #ccc; /* паддинг-фон, пока картинка грузится */
}

/* Само изображение растягиваем по ширине, сохраняем пропорции */
.logo-image {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50%;
  height: auto;
  /* Смещаем картинку так, чтобы центр по вертикали совпадал с центром контейнера */
  transform: translate(-50%, -50%) scale(1);
  transform-origin: center center;
  object-fit: cover;
  object-position: center center;

  /* Добавим лёгкую анимацию «zoom-in» */
  animation: zoomIn 1.5s ease-out forwards;
}

/* Градиентная маска снизу:
   от прозрачного в центре (cверху mask), до фона конТЕНТ-блока (#f7f7f7) внизу. */
.gradient-mask {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 30%;
  /* фон плавно перекрывает нижние ~30% изображения, смешиваясь с цветом content-block */
  background: linear-gradient(
      to bottom,
      rgba(255, 255, 255, 0) 0%,        /* прозрачный сверху */
      var(--bg-content) 80%              /* цвет content-блока снизу */
  );
  pointer-events: none;
}

/* При необходимости можно добавить полупрозрачную тень-бэкграунд сверху */
.logo-block::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* Чуть затемняем верхнюю часть — создаём ощущение «глубины» */
  background: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.3) 0%,
      rgba(0, 0, 0, 0) 50%
  );
  pointer-events: none;
}

/* Анимация zoomIn для картинки */
@keyframes zoomIn {
  0% {
    transform: translate(-50%, -50%) scale(1.1);
    filter: brightness(0.9);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    filter: brightness(1);
  }
}

/* === БЛОК 2: КОНТЕНТ ПОД КАРТИНКОЙ === */
.content-block {
  position: relative;
  width: 100%;
  padding: 3rem 1rem;
  box-sizing: border-box;
  background-color: var(--bg-content);
  display: flex;
  flex-direction: column;
  align-items: center;

  /* Сразу скрыт, а потом появится через 0.5с */
  opacity: 0;
  animation: fadeInContent 1s ease-out 1s forwards;
}

/* fade-in анимация */
@keyframes fadeInContent {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Отступ снизу у последнего элемента, если понадобится */
.content-block > *:last-child {
  margin-bottom: 0;
}

/* === «Спасибо» (заголовок) === */
.thank-you {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1e3a1e;
  margin-bottom: 1rem;
  text-align: center;
  line-height: 1.2;
}

/* Текст «результата» === */
.result-text {
  max-width: 650px;
  margin: 0 0 2rem;
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--text-color);
  text-align: center;
}

/* Телефонный блок === */
.contact-phone {
  margin: 0 0 2rem;
  font-size: 1rem;
  color: var(--text-color);
  text-align: center;
}
.phone-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
}
.phone-link:hover {
  text-decoration: underline;
}

/* Кнопка «Вернуться на главную» === */
.back-link {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: var(--primary-color);
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 4px;
  text-decoration: none;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease, transform 0.2s ease;
}
.back-link:hover {
  background-color: var(--primary-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.12);
}
.back-link:active {
  transform: translateY(0);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
}
</style>
