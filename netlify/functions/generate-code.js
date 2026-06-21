// توليد كود مشاهدة جديد — محمي بكلمة سرّ المدير
// يُستدعى من admin.html عبر: POST /.netlify/functions/generate-code  { password, label }

import { getStore } from '@netlify/blobs'
import { randomBytes } from 'node:crypto'

export default async (req) => {
  if (req.method !== 'POST') return json({ ok: false }, 405)

  let body
  try { body = await req.json() } catch { return json({ ok: false, reason: 'bad_request' }, 400) }

  // فحص كلمة سرّ المدير (محفوظة بإعدادات Netlify السرّيّة)
  if (!process.env.ADMIN_PASSWORD || body.password !== process.env.ADMIN_PASSWORD) {
    return json({ ok: false, reason: 'unauthorized' }, 401)
  }

  const code = makeCode()
  const store = getStore('screening-codes')
  await store.setJSON(code, {
    createdAt: Date.now(),
    activatedAt: null,                       // يُفعّل عند أوّل استعمال
    uses: 0,                                 // عدد الفتحات (الحدّ الأقصى 5)
    label: String(body.label || '').slice(0, 80) // اسم الشخص (للتذكّر)
  })

  return json({ ok: true, code })
}

// كود من 8 خانات، سهل القراءة (بدون أحرف/أرقام ملتبسة مثل O/0 و I/1)
function makeCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
  const b = randomBytes(8)
  let out = ''
  for (let i = 0; i < 8; i++) out += chars[b[i] % chars.length]
  return out.slice(0, 4) + '-' + out.slice(4) // مثال: K7P2-9XQM
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' }
  })
}
