<template>
  <div class="landing-page">
    <!-- COVER SECTION -->
    <section class="cover">
      <div class="cover-wrapper">
        <div class="topnew">
          <div class="logo">
            <a href="/">
              <img src="/img/logo.png" alt="Новый логотип" />
            </a>
          </div>
          <div class="zakazpopup">
            <a
                href="#"
                class="cli-button cli-button--primary cli-button--big"
                @click.prevent="showConsultation = true"
            >
              Консультация за наш счёт
            </a>
          </div>
        </div>

        <div
            class="cli-block__content cli-grid cli-block__content--cover"
            data-type="grid"
            data-title="Блок"
        >
          <div
              class="cli-block-title cli-block-title--gigantic cli-text-center cli-text-bold"
              v-html="`Получите <span style='color:#B71C1C'>индивидуальный разбор юриста</span> и инструкцию по списанию долгов бесплатно
            <div class='subtitle'>при сумме долга от <span style='color:#B71C1C; white-space:nowrap'>300 тыс. рублей</span></div>`"
          ></div>

          <div class="cli-block-subtitle cli-block-subtitle--big cli-text-center cli-text-regular">
            <div class="container-text">
              <div>97% клиентов успешно списали долги не приходя в офис</div>
              <div>Спасем вашу квартиру, машину и доход</div>
              <div>Остановим звонки коллекторов в день обращения</div>
            </div>
            <strong>Заполните </strong>
            <strong style="color:#B71C1C">БЕСПЛАТНУЮ</strong>
            <strong> анкету и узнайте о возможности списать ваши долги + </strong>
            <strong style="color:#B71C1C">получите инструкцию</strong>
            <strong> по списанию долгов</strong>
            <div class="litle-strong-title">
              Какие долги можно списать по закону
            </div>
          </div>

          <div class="utp">
            <div v-for="item in utpItems" :key="item.text" class="utp-item">
              <img :src="item.img" :alt="item.text" class="utp-item__icon" />
              <div class="utp-item__text">{{ item.text }}</div>
            </div>
          </div>

          <a href="#quiz-form" class="cli-block-icon cli-block-icon--big scroll-down">
            <svg width="24" height="24" viewBox="0 0 24 24">
              <path
                  fill="currentColor"
                  d="M12 13.8238L6.6325 9.52978C6.43843 9.37452 6.15525 9.40599 5.99999 9.60006C5.84474 9.79412 5.8762 10.0773 6.07027 10.2326L12 14.9763L17.9297 10.2326C18.1238 10.0773 18.1552 9.79412 18 9.60006C17.8447 9.40599 17.5616 9.37452 17.3675 9.52978L12 13.8238Z"
              />
            </svg>
          </a>
        </div>
      </div>
    </section>

    <!-- FORM / QUIZ SECTION -->
    <section id="quiz-form" class="cli-form-block">
      <div class="cli-block__content">
        <div class="start-cli-block">
          <div class="cli-block-title--large">
            Заполните анкету и получите решение
          </div>
        </div>
        <form @submit.prevent="onSubmit" class="cli-form">
          <fieldset class="cli-form__fieldset">
            <legend>Какие у Вас долги?</legend>
            <label v-for="opt in quiz1" :key="opt.value">
              <input
                  type="checkbox"
                  :value="opt.value"
                  v-model="form.quiz1"
                  @change="clickQuiz"
              />
              {{ opt.label }}
            </label>
          </fieldset>

          <fieldset class="cli-form__fieldset">
            <legend>Есть ли просрочки по выплатам?</legend>
            <label v-for="opt in quiz2" :key="opt.value">
              <input
                  type="radio"
                  name="delays"
                  :value="opt.value"
                  v-model="form.quiz2"
                  @change="clickQuiz"
              />
              {{ opt.label }}
            </label>
          </fieldset>

          <fieldset class="cli-form__fieldset">
            <legend>
              Какая сумма задолженности?
              (Автоматом списываем, если более 300 т.р.)
            </legend>
            <label v-for="opt in quiz3" :key="opt.value">
              <input
                  type="radio"
                  name="amount"
                  :value="opt.value"
                  v-model="form.quiz3"
                  required
              />
              {{ opt.label }}
            </label>
          </fieldset>

          <div class="phone-title">
            Введите номер, на который мы отправим результаты оценки Вашей ситуации
          </div>
          <div>
            <MaskInput
                v-model="phoneNumber"
                placeholder="Введите свой номер телефона для получения решения"
                mask="+7 (###) ###-##-##"
                class="cli-phone-input"
            />
          </div>

          <input type="hidden" name="utm_source" :value="utm.source" />
          <input type="hidden" name="utm_medium" :value="utm.medium" />
          <input type="hidden" name="utm_campaign" :value="utm.campaign" />
          <input type="hidden" name="utm_content" :value="utm.content" />
          <input type="hidden" name="utm_term" :value="utm.term" />

          <button type="submit" class="cli-button cli-button--primary cli-button--big">
            Получить решение
          </button>
          <div v-if="showNotEnough" class="form-not-enough">
            Извините, но мы не работаем с долгом ниже 300 т.р.
          </div>
        </form>
        <span class="span-on-footer">
          <p class="cli-block-description">
            После заполнения анкеты мы позвоним с номера +7 (924) 612-88-17 и предоставим бесплатную инструкцию, как поступить в вашей ситуации.
          </p>
        </span>
      </div>
    </section>

    <!-- REVIEWS SLIDER SECTION -->
    <section class="rewiews">
      <h2 class="reviews-title">Отзывы наших клиентов</h2>

      <Swiper
          :modules="[Pagination, Autoplay]"
          :slides-per-view="1"
          :space-between="0"
          pagination
          loop
          :autoplay="{ delay: 3000, disableOnInteraction: false }"
          class="reviews-swiper"
      >
        <SwiperSlide v-for="(review, idx) in reviews" :key="idx">
          <div class="review-slide">
            <div class="review-slide__img-wrapper">
              <img
                  :src="review.avatar"
                  :alt="`Фото ${review.name}`"
                  class="review-slide__img"
              />
            </div>
            <div class="review-slide__card">
              <h3 class="review-slide__title">{{ review.name }}</h3>
              <p class="review-slide__text">{{ review.text }}</p>
              <span class="review-slide__date">{{ review.date }}</span>
              <a
                  v-if="review.docLink"
                  :href="review.docLink"
                  class="review-slide__link"
                  target="_blank"
                  rel="noopener noreferrer"
              >
                Читать полностью
              </a>
            </div>
          </div>
        </SwiperSlide>
      </Swiper>
    </section>

    <!-- FOOTER SECTION -->
    <footer class="footer">
      <div class="footer-cont">
        <div class="cli-footer-logo">
          <img src="/img/logo-footer.png" alt="Новый логотип" />
        </div>
        <div class="cli-footer-logo__text">
        <strong>{{ site.name }}</strong><br />
        {{ site.ip }}<br /><br /><br />
        <a :href="`tel:${site.phoneInt}`" @click="clickPhone">{{ site.phone }}</a><br />
        <a :href="`tel:${site.phone2Int}`" @click="clickPhone">{{ site.phone2 }}</a>
      </div>
      <div class="footer_r">
        Адрес:<br />
        {{ site.addr }}<br /><br />
        {{ site.inn }}<br />
        {{ site.ogrn }}
      </div>
      </div>
    </footer>
    <div class="Privacy-Policy">
      <router-link to="/privacy-policy">
        Политика обработки персональных данных
      </router-link>
    </div>

    <!-- Craftum Watermark -->
    <div class="craftum-label" v-html="craftumSvg"></div>

    <!-- POPUP: уже отправили заявку -->
    <div class="modal sendFormPopup" :class="{ active: alreadySent }">
      <div class="modal-window">
        <button class="modal-close" @click="alreadySent = false">×</button>
        <div class="sendFormPopupBody">
          <h1>Вы уже оставили заявку.<br /><span>Скоро свяжемся  вами.</span></h1>
        </div>
      </div>
    </div>

    <!-- MODAL: Консультация -->
    <transition name="fade">
      <div
          class="modal-overlay"
          v-if="showConsultation"
          @click.self="closeConsultation"
      >
        <button class="modal-close" @click="closeConsultation"></button>
        <div class="modal-window">
          <div class="modal-title">
            <!-- Если пользователь ещё не отправил форму, показываем форму -->
            <template v-if="!showAlreadySentModal">
              Введите номер для бесплатной консультации
              <form @submit.prevent="onSubmitConsult">
                <div class="phone-title">
                  Введите номер, на который мы отправим результаты оценки
                  <span style="white-space: nowrap;">Вашей ситуации</span>
                </div>
                <div class="modal-input">
                  <MaskInput
                      v-model="consultPhone"
                      placeholder="Введите свой номер телефона для получения решения"
                      mask="+7 (###) ###-##-##"
                      class="cli-phone-input"
                      required
                  />
                </div>
                <div class="button-send">
                  <button
                      type="submit"
                      class="cli-button cli-button--primary cli-button--big"
                  >
                    Отправить и получить инструкцию
                  </button>
                </div>
              </form>
            </template>

            <!-- Если уже отправлено или только что отправили, показываем сообщение -->
            <template v-else>
              <div class="consult-thanks">
                <h3>Заявка принята</h3>
                <p>Спасибо! Мы получили ваш запрос и свяжемся с вами в ближайшее время.</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { useRouter } from 'vue-router';       // <-- добавили
  import { MaskInput } from "vue-3-mask";
  import { Swiper, SwiperSlide } from 'swiper/vue';
  import { Pagination, Autoplay } from 'swiper';
  import 'swiper/css';
  import 'swiper/css/navigation';
  import 'swiper/css/pagination';

  const router = useRouter();
  const showAlreadySentModal = ref(false);

  const utm = reactive({ source: '', medium: '', campaign: '', content: '', term: '' });
  function getParam(name) {
    const p = new URLSearchParams(location.search).get(name);
    if (p) {
      document.cookie = `${name}=${encodeURIComponent(p)};max-age=${3600*24*30};path=/`;
    }
    return decodeURIComponent((document.cookie.match(new RegExp(`(^| )${name}=([^;]+)`)) || [])[2] || '');
  }
  onMounted(() => {
    ['source','medium','campaign','content','term'].forEach(k => {
      utm[k] = getParam(`utm_${k}`) || '';
    });
  });

const quiz1 = [
  { value: 'Потребительский кредит(ы)', label: 'Потребительский кредит(ы)' },
  { value: 'Займ(ы) МФО', label: 'Займ(ы) МФО' },
  { value: 'ЖКХ', label: 'ЖКХ' },
  { value: 'Другие долги', label: 'Другие долги' },
];
const quiz2 = [
  { value: 'Да', label: 'Да' },
  { value: 'Нет', label: 'Нет' }
];
const quiz3 = [
  { value: 'Менее 300 т.р.', label: ' Менее 300 000 руб. ' },
  { value: 'Более 300 т.р.', label: '300 000 - 500 000 руб. ' },
  { value: 'Не знаю', label: ' Более 500 000 руб. ' }
];
const form = reactive({
  quiz1: ['Потребительский кредит(ы)'],
  quiz2: 'Да',
  quiz3: 'Более 300 т.р.',
  phone: ''
});
const showConsultation = ref(false);
const consultPhone     = ref('');

const phoneNumber = ref('');

const site = {
  name:      'ООО «ВАШ ЮРИСТЪ»',
  ip:        '664007, г. Иркутск, ул. Поленова, 1/1, оф. 213',
  phoneInt:  '83952716094', phone:  '+7 411 224-30-67',
  // phone2Int: '88006003823', phone2: '+7 411 224-30-67',
  addr:      '677005? г Якутск, \n' + 'ул Халтурина, д. 6/3, помещ. 61',
  inn:       'ИНН 1400034687',
  ogrn:      'КПП: 140001001'
};

const utpItems = [
  { img: '/img/cards.svg', text: 'По  кредитам' },
  { img: '/img/money.svg', text: 'Микрозаймы и МФО' },
  { img: '/img/driver.svg', text: 'Долги за ЖКХ' },
  { img: '/img/documents.svg', text: 'Долги по распискам' }
];

const craftumSvg = `<svg width="20" height="20" viewBox="0 0 20 20"><!-- … --></svg>`;

function clickQuiz() {
  if (!clickQuiz.done && window.ym) {
    window.ym(window.metrikaId, 'reachGoal', 'click_quiz');
    clickQuiz.done = true;
  }
}
function clickPhone() {
  if (!clickPhone.done && window.ym) {
    window.ym(window.metrikaId, 'reachGoal', 'click_phone_linck');
    clickPhone.done = true;
  }
}
  const showNotEnough = ref(false);
  const alreadySent = ref(false);

function onSubmit() {

  if (form.quiz3 === 'Менее 300 т.р.') {
    showNotEnough.value = true;
    return;
  }
  showNotEnough.value = false;

  if (document.cookie.includes('sendForm=true')) {
    alreadySent.value = true;
    return;
  }

  const data = new FormData();
  Object.entries(form).forEach(([k, v]) => data.append(k, v));
  Object.entries(utm).forEach(([k, v]) => data.append(`utm_${k}`, v));

  fetch('/send.php', { method: 'POST', body: data })
      .then(() => {
        window.ym && ym(102334874,'reachGoal','send_quiz');

        document.cookie = 'sendForm=true;max-age=' + (3600 * 24 * 180) + ';path=/';

        // Вместо window.location.href:
        router.push({ name: 'Result' }); // <-- программно переходим на маршрут "Result"
      })
      .catch(err => {
        console.error('Ошибка при отправке формы:', err);
        // здесь можно показать уведомление об ошибке
      });
}
  function scrollToForm() {
    document
        .getElementById('quiz-form')
        ?.scrollIntoView({ behavior: 'smooth' });
  }
  function closeConsultation() {
    showConsultation.value = false
    // при желании можно сбрасывать остальные флаги, но не обязательно
  }
  function onSubmitConsult() {
    // Цель Метрики
    window.ym && ym(102334874,'reachGoal','send_form');

    // Если уже отправлял — сразу показываем «спасибо»
    if (document.cookie.includes('consultSent=true')) {
      showAlreadySentModal.value = true
      return
    }

    // Собираем данные и отправляем
    const data = new FormData()
    data.append('phone', consultPhone.value)

    fetch('/send_consult.php', {
      method: 'POST',
      body: data,
    })
        .then(() => {
          // Ставим куку, чтобы не давать повторно отправить
          document.cookie = 'consultSent=true;max-age=' + 3600 * 24 * 180 + ';path=/'
          showAlreadySentModal.value = true
        })
        .catch((err) => {
          console.error('Ошибка при отправке запроса на консультацию:', err)
        })
  }

const reviews = ref([
  {
    avatar: '/img/VictorDolg.jpg',
    name: 'Машуков Виктор Александрович',
    date: '20 мая 2025',
    text: 'Срок списания: 6м 21д\nСумма долга: 1 016 868 руб.',
    docLink: '/docs/Victor.pdf',
  },
  {
    avatar: '/img/Aleksandr.jpg',
    name: 'Еникеев Александр Александрович',
    date: '15 мая 2025',
    text: 'Срок списания: 1г 7м 27д\nСумма долга: 349 407 руб.',
    docLink: '/docs/Aleksandr.pdf',
  },
  {
    avatar: '/img/Vladimir.jpg',
    name: 'Барашков Владимир Данилович',
    date: '10 мая 2025',
    text: 'Срок списания: 10м 26д\nСумма долга: 1 565 017 руб.',
    docLink: '/docs/Vladimir.pdf',
  },
  {
    avatar: '/img/Nadezhda.jpg',
    name: 'Шадрина Надежда Ивановна',
    date: '20 мая 2025',
    text: 'Срок списания: 5м 12д\nСумма долга: 666 506 руб.',
    docLink: '/docs/Nadezhda.pdf',
  },
  {
    avatar: '/img/Natalia.jpg',
    name: 'Сягина Наталья Витальевна',
    date: '15 мая 2025',
    text: 'Срок списания: 11м 29д\nСумма долга: 2 301 493 руб.',
    docLink: '/docs/Natalia.pdf',
  },
  {
    avatar: '/img/Drit-ian.jpg',
    name: 'Дрит Ян Вячеславович',
    date: '10 мая 2025',
    text: 'Срок списания: 1г 15д\nСумма долга: 5 632 460 руб.',
    docLink: '/docs/Ian.pdf',
  },
]);

  ['source','medium','campaign','content','term'].forEach(k => {
    utm[k] = getParam(`utm_${k}`);
  });
</script>

<style scoped>
:root {
  --text-size-gigantic: clamp(28px, 5vw, 64px);
  --text-size-large: clamp(20px, 4vw, 36px);
  --text-size-medium: clamp(16px, 3vw, 24px);
  --text-size-small: clamp(14px, 2.5vw, 18px);
  --sans-serif: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --primary-color: #6c63ff;
  --danger-color: #B71C1C;
  --container-padding: clamp(15px, 5vw, 40px);
}

*,
h1,h2,h3,h4,h5,h6,p {
  margin: 0; padding: 0; box-sizing: border-box;
  font-family: var(--sans-serif);
}

body {
  line-height: 1.6;
  color: #333;
  overflow-x: hidden;
}

.cover {
  position: relative;
  background: url('/img/most.png') center/cover no-repeat;
  display: flex; flex-direction: column;
  min-height: 100vh;
}
.cover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  z-index: 0;
}
.cover-wrapper {
  position: relative;
  z-index: 2;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.topnew {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
  height: 165px;
  gap: 1rem;
  padding: var(--container-padding);
}
.topnew .logo img {
  height: clamp(80px, 15vw, 130px);
  max-width: 100%;
  object-fit: contain;
}
.topnew > div {
  padding: 1em;
}
.topnew .zakazpopup a {
  padding: clamp(0.6rem, 2vw, 0.8rem) clamp(1rem, 3vw, 1.5rem);
  background: var(--primary-color);
  color: #fff;
  border-radius: 25px;
  font-weight: 600;
  text-decoration: none;
  font-size: var(--text-size-small);
  transition: all 0.3s ease;
  white-space: nowrap;
}
.topnew .zakazpopup a:hover {
  background: #5a52e6;
  transform: translateY(-2px);
}

.cli-block__content--cover {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  width: 100%;
  max-width: 1140px;
  padding: var(--container-padding);
  margin: 0 auto;
  gap: clamp(1.5rem, 4vw, 3rem);
}

.container-text {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  padding-bottom: 20px;
  font-weight: bold;
  width: 100%;
}
.container-text div {
  padding: 10px;
  text-align: center;
}
.cli-block__content--cover.cli-grid > * + * {
  margin-top: 2rem;
}
.litle-strong-title {
  font-size: var(--text-size-medium);
  margin-top: 30px;
  margin-bottom: 5px;
  font-weight: bold;
}
.cli-block-title--gigantic {
  font-size: clamp(2rem, 5vw, var(--text-size-gigantic));
  font-weight: bold;
  text-align: center;
  line-height: 1.2;
}

.start-cli-block {
  margin-top: 8px;
  margin-bottom: 16px;
  display: flex;
  font-weight: bold;
  text-align: center;
  font-size: var(--text-size-large);
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.cli-block-title--large {
  margin: auto;
}

.subtitle {
  font-size: var(--text-size-large);
  font-weight: 700;
  margin-top: 0.5rem;
  line-height: 1.2;
}
.cli-block-subtitle--big {
  text-align: center;
  max-width: 800px;
}

.utp {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: clamp(1rem, 3vw, 2rem);
  width: 100%;
  max-width: 600px;
}

.utp-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.utp-item__icon {
  width: clamp(40px, 8vw, 60px);
  height: clamp(40px, 8vw, 60px);
  margin-bottom: 0.5rem;
}

.utp-item__text {
  font-size: clamp(12px, 2.5vw, 14px);
  font-weight: bold;
  line-height: 1.3;
}

.scroll-down {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 2rem;
  color: var(--primary-color);
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.cli-form-block {
  background: #fff;
  padding: var(--container-padding);
}
.cli-block__content {
  max-width: 1140px;
  margin: 0 auto;
}
.cli-form__fieldset {
  margin-bottom: clamp(1.5rem, 4vw, 2rem);
  border: none;
}
.cli-form__fieldset legend {
  font-weight: 600;
  color: black;
  margin-bottom: 15px;
  font-size: var(--text-size-small);
  width: 100%;
}
.cli-form__fieldset input[type="checkbox"],
.cli-form__fieldset input[type="radio"] {
  width: clamp(16px, 4vw, 20px);
  height: clamp(16px, 4vw, 20px);
  margin-right: clamp(8px, 2vw, 12px);
  accent-color: var(--primary-color);
  cursor: pointer;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.cli-form__fieldset label {
  display: flex;
  align-items: flex-start;
  margin-bottom: 12px;
  cursor: pointer;
  font-size: var(--text-size-small);
  color: #333;
  font-weight: normal;
  transition: all 0.2s ease;
  padding: clamp(8px, 2vw, 12px);
  border-radius: 8px;
  line-height: 1.4;
}
.cli-form__fieldset label:hover {
  background-color: #f8f9fa;
}
.cli-form__fieldset input[type="radio"]:checked + span,
.cli-form__fieldset input[type="checkbox"]:checked + span {
  color: var(--primary-color);
  font-weight: 500;
}

.cli-form {
  max-width: 600px;
  margin: 0 auto;
  padding: clamp(15px, 4vw, 20px);
  font-family: var(--sans-serif);
}
.cli-form__fieldset input {
  margin-right: 0.5rem;
}
.cli-form input[type="tel"] {
  width: 100%;
  padding: 0.6rem;
  font-size: 1rem;
}

.cli-button--primary {
  width: 100%;
  padding: clamp(0.8rem, 3vw, 1rem);
  background: var(--primary-color);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: var(--text-size-small);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}
.cli-button--primary:hover {
  background: #5a52e6;
  transform: translateY(-2px);
}
.cli-button--secondary {
  background-color: #ccc;
  color: #212121;
  margin-top: 1rem;
}
.form-not-enough {
  color: red;
  text-align: center;
  margin-top: 0.5rem;
}
.cli-block-description {
  text-align: center;
  font-size: clamp(13px, 2.5vw, 15px);
  margin-top: 30px;
  margin-bottom: 20px;
  font-weight: 550;
  color: #666;
  line-height: 1.5;
}
.cli-phone-input {
  width: 100%;
  height: clamp(50px, 12vw, 58px);
  padding: 0 16px;
  font-size: var(--text-size-small);
  border-radius: 8px;
  outline: none;
  transition: border 0.3s;
  color: #000;
  background-color: #fff;
  border: 2px solid #ddd;
  box-sizing: border-box;
}
.cli-phone-input:focus {
  border-color: var(--primary-color);
}

.reviews {
  background-color: white;
  padding: var(--container-padding);
}
.reviews-wrapper {
  max-width: 1140px;
  margin: 0 auto;
}
.reviews-title {
  font-size: var(--text-size-large);
  text-align: center;
  font-weight: 700;
  margin-bottom: 2rem;
}
.reviews-swiper {
  position: relative;
  padding-bottom: 3rem; /* место для пагинации */
  overflow: hidden;
}
.review-slide {
  max-width: 360px;
  margin: 0 auto;
}
.review-slide__img-wrapper {
  position: relative;
  width: 100%;
  padding-top: 100%;
  overflow: hidden;
  border-radius: 12px 12px 0 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
.review-slide__img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.review-slide__card {
  background: #f9f9fb;
  padding: 1.25rem;
  border-radius: 0 0 12px 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  text-align: center;
}
.review-slide__title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}
.review-slide__text {
  font-size: 0.875rem;
  color: #555;
  line-height: 1.4;
  margin-bottom: 0.75rem;
  white-space: pre-line;
}
.review-slide__date {
  display: block;
  font-size: 0.875rem;
  color: #888;
  margin-bottom: 0.75rem;
}
.review-slide__link {
  display: inline-block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--primary-color);
  text-decoration: underline;
  transition: color 0.2s;
}
.review-slide__link:hover {
  color: #5a52e6;
}

/* Кнопки навигации Swiper: окружности с Unicode-стрелками */
.swiper-button-prev,
.swiper-button-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  background-color: rgba(0, 0, 0, 0.25);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
}
.swiper-button-prev {
  left: 0.5rem;
}
.swiper-button-next {
  right: 0.5rem;
}
/* Добавляем стрелки через псевдоэлемент ::after */
.swiper-button-prev::after {
  content: '◀';
  font-size: 20px;
  color: white;
}
.swiper-button-next::after {
  content: '▶';
  font-size: 20px;
  color: white;
}

/* Стили для пагинации (точек) */
.reviews-swiper .swiper-pagination {
  bottom: 0;
}

.footer a {
  color: var(--primary-color);
  text-decoration: none;
}
.footer a:hover {
  text-decoration: underline;
}
.footer {
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  background: #f8f8f8;
  padding: 2rem 1rem;
  font-size: 0.9rem;
}
.footer-cont {
  display: flex;
  grid-template-columns: min-content 1fr; /* либо 1fr 1fr, как нужно */
  align-items: center;
  gap: 2rem;
}
/* вместо ".footer .cli-footer-logo img" */
.footer_r {
  text-align: right;
  font-size: var(--text-size-small);
  line-height: 1.4;
}

/* Flex внутри левого столбца: картинка + текст */
.cli-footer-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.cli-footer-logo img {
  height: clamp(100px, 20vw, 200px);
  width: auto;
  object-fit: contain;
}

.cli-footer-logo__text h4 {
  margin: 0;
  line-height: 1.2;
}

.cli-footer-logo__text a {
  display: block;
  margin-top: 0.3rem;
  color: inherit;
  text-decoration: none;
  font-size: var(--text-size-small);
}
.Privacy-Policy{
  text-align: center;
  padding: 20px 0;
  background: #f8f8f8;
}
.craftum-label {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  z-index: 1000;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal, .modal-overlay {
  display: none;
}
.sendFormPopupBody{
  color: darkred;
  display: flex;
  justify-content: center;
}
.modal.sendFormPopup.active,
.modal-overlay {
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  inset: 0;
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  z-index: 2000;
}
.modal-title {
  text-align: center;
  font-size: var(--text-size-large);
  color: #bf1717;
  font-weight: 700;
  margin-bottom: 2rem;
  line-height: 1.3;
}
.modal-window {
  border-radius: 8px;
  max-width: 90%;
  width: 80%;
}
.modal-input {
  margin-bottom: 0.3rem;
}
.consult-thanks {
  text-align: center;
  font-size: var(--text-size-large);
}
.consult-thanks h3 {
  margin-bottom: 1rem;
  color: #bf1717;
}
.consult-thanks p {
  margin-bottom: 1.5rem;
  color: #212121;
}
.button-send {
  padding-bottom: 1rem;
}
.phone-title {
  color: #333;
  font-size: var(--text-size-small);
  font-weight: 750;
  margin-top: 2rem;
  text-align: center;
  line-height: 1.4;
}

.modal-close {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #f0f0f0;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: #666;
  transition: all 0.3s ease;
  width: 48px;
  height: 48px;
  --svg: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23000' d='M6.4 19L5 17.6l5.6-5.6L5 6.4L6.4 5l5.6 5.6L17.6 5L19 6.4L13.4 12l5.6 5.6l-1.4 1.4l-5.6-5.6z'/%3E%3C/svg%3E");
  background-color: currentColor;
  -webkit-mask-image: var(--svg);
  mask-image: var(--svg);
  -webkit-mask-repeat: no-repeat;
  mask-repeat: no-repeat;
}
.modal-close:hover {
  background: #e0e0e0;
  color: #333;
}

/* Плавное появление/скрытие */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .topnew {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  .topnew .zakазpopup {
    order: -1;
  }
  .container-text {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  .utp {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  .cli-form__fieldset label {
    align-items: flex-start;
    padding: 12px 8px;
  }
  .modal-window {
    margin: 20px;
    max-height: calc(100vh - 40px);
  }
}

@media (max-width: 480px) {
  .utp {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .utp-item {
    flex-direction: row;
    text-align: left;
    gap: 1rem;
  }
  .footer {
    grid-template-columns: 1fr;
    text-align: center;
  }
}
@media (max-width: 320px) {
  .utp {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .utp-item {
    flex-direction: row;
    text-align: left;
    gap: 1rem;
  }
  .footer {
    grid-template-columns: 1fr;
    text-align: center;
  }
}

@media (hover: none) and (pointer: coarse) {
  .cli-form__fieldset input[type="checkbox"],
  .cli-form__fieldset input[type="radio"] {
    width: 22px;
    height: 22px;
  }
  .cli-button--primary {
    padding: 1rem;
    font-size: 16px;
  }
  .modal-close {
    width: 44px;
    height: 44px;
    font-size: 20px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-down {
    animation: none;
  }
  * {
    transition: none !important;
  }
}
</style>
