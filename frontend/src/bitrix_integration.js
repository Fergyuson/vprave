/* 1. Константы веб‑хуков Bitrix24 */
const DOMAIN   = 'https://1pb.bitrix24.ru';
const TOKEN    = '670/1ilsmw0k19acjgrr';            // ID/KEY входящего веб‑хука
const API_URL = '/api/leads';


/* 2. Утилита чтения cookie (для UTM‑меток) */
function getCookie(name) {
    const matches = document.cookie.match(
        new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()\\[\]\\/+^])/g, '\\$1') + '=([^;]*)')
    );
    return matches ? decodeURIComponent(matches[1]) : '';
}

/* 3. Проверяем, есть ли лид с таким телефоном (точная проверка) */
export async function checkPhoneExists(phone) {
    let normalized = phone.replace(/\D/g, '');
    if (normalized.startsWith('8')) normalized = '7' + normalized.slice(1);

    const body = {
        entity_type: 'LEAD',
        type: 'PHONE',
        values: [normalized]
    };

    const FIND_URL = `${DOMAIN}/rest/${TOKEN}/crm.duplicate.findbycomm.json`;

    try {
        const r    = await fetch(FIND_URL, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(body)
        });
        const json = await r.json();

        if (json.error) {
            console.error('[Bitrix24 DUP]', json.error_description || json.error);
            return false;          // при ошибке не блокируем
        }

        return Array.isArray(json.result?.LEAD) &&
            json.result.LEAD.length > 0;
    } catch (err) {
        console.error('[Bitrix24 DUP] fetch failed:', err);
        return false;
    }
}

/* 4. Создаём новый лид */
export async function sendLeadToBitrix(fields) {
    const payload = {
        name:     fields.name,
        phone:    fields.phone,
        email:    fields.email || null,
        comment:  fields.comment || null,
        utm_source:  getCookie('utm_source')  || null,
        utm_medium:  getCookie('utm_medium')  || null,
        utm_campaign:getCookie('utm_campaign')|| null,
        utm_term:    getCookie('utm_term')    || null,
        utm_content: getCookie('utm_content') || null,
    };

    try {
        const r = await fetch(API_URL, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload),
        });
        const json = await r.json();
         if (!r.ok) console.error('[Backend ADD] 422 →', json.detail || json);
         else       console.log('[Backend ADD]', json);
    } catch (err) {
        console.error('[Backend ADD] fetch failed:', err);
    }
}


