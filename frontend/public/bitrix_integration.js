// bitrix_integration.js
// ────────────────────────────────────────
// 1) Утилита для чтения cookie
// ────────────────────────────────────────
function getCookie(name) {
    const m = document.cookie.match(
        new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)')
    );
    return m ? decodeURIComponent(m[1]) : '';
}

// ────────────────────────────────────────
// 2) URL входящего веб‑хука Bitrix24 + метод
// ────────────────────────────────────────
const BITRIX_WEBHOOK =
    'https://1pb.bitrix24.ru/rest/670/1ilsmw0k19acjgrr/crm.lead.add.json';

// ────────────────────────────────────────
// 3) Глобальная функция отправки лида
//    (можно вызвать из Vue: window.sendLeadToBitrix(...))
// ────────────────────────────────────────
async function sendLeadToBitrix(name, phone) {
    // Формируем объект "fields"
    const fields = {
        NAME: name,
        PHONE: [{ VALUE: phone, VALUE_TYPE: 'WORK' }],
        SOURCE_ID: '30',
        UTM_SOURCE:   getCookie('utm_source'),
        UTM_MEDIUM:   getCookie('utm_medium'),
        UTM_CAMPAIGN: getCookie('utm_campaign'),
        UTM_CONTENT:  getCookie('utm_content'),
        UTM_TERM:     getCookie('utm_term')
    };

    // Отправляем POST‑запрос
    try {
        const r = await fetch(BITRIX_WEBHOOK, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ fields })
        });
        const data = await r.json();
        if (data.error) {
            console.error('Bitrix24 error:', data.error_description || data.error);
        } else {
            console.log('Lead created, ID =', data.result);
        }
    } catch (err) {
        console.error('Fetch to Bitrix24 failed:', err);
    }
}

// ────────────────────────────────────────
// 4) Пример: автоматический вызов на форме
// ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('lead-form'); // ← замените на реальный ID
    if (!form) return;

    form.addEventListener('submit', e => {
        e.preventDefault();
        const name  = form.querySelector('input[name=name]').value || '';
        const phone = form.querySelector('input[name=phone]').value;
        sendLeadToBitrix(name, phone);
    });
});

// Делаем функцию доступной глобально для Vue‑компонента
window.sendLeadToBitrix = sendLeadToBitrix;
