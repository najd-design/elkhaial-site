// التحقّق من كود المشاهدة + تطبيق نافذة الـ 48 ساعة + توليد رابط Bunny موقّت
// يُستدعى من watch.html عبر: POST /.netlify/functions/verify-code  { code }

import { getStore } from '@netlify/blobs'
import { createHash } from 'node:crypto'

const WINDOW_MS = 48 * 60 * 60 * 1000 // 48 ساعة بالمللي ثانية
const MAX_USES = 5                    // أقصى عدد فتحات للكود
const LINK_TTL_SEC = 60 * 60          // رابط الفيديو الموقّت صالح ساعة وحدة

export default async (req) => {
  if (req.method !== 'POST') return json({ ok: false, reason: 'method' }, 405)

  let body
  try { body = await req.json() } catch { return json({ ok: false, reason: 'bad_request' }, 400) }

  const code = String(body.code || '').trim().toUpperCase()
  if (!code) return json({ ok: false, reason: 'empty' }, 400)

  const store = getStore('screening-codes')
  const record = await store.get(code, { type: 'json' })

  // كود غير موجود
  if (!record) return json({ ok: false, reason: 'invalid' })

  const now = Date.now()

  if (!record.activatedAt) {
    // أوّل استعمال → نفعّل نافذة الـ 48 ساعة ونعدّ الفتحة الأولى
    record.activatedAt = now
    record.uses = 1
    await store.setJSON(code, record)
  } else {
    // انتهت النافذة الزمنيّة؟
    if (now - record.activatedAt > WINDOW_MS) return json({ ok: false, reason: 'expired' })
    // خلص عدد الفتحات؟
    const uses = record.uses || 0
    if (uses >= MAX_USES) return json({ ok: false, reason: 'maxed' })
    record.uses = uses + 1
    await store.setJSON(code, record)
  }

  // الكود صالح → نولّد رابط Bunny موقّت (مقفول على الدومين من إعدادات Bunny)
  const url = signBunnyEmbed()
  if (!url) return json({ ok: false, reason: 'server_config' }, 500)

  const remainingMs = record.activatedAt + WINDOW_MS - now
  const remainingUses = MAX_USES - record.uses
  return json({ ok: true, url, remainingMs, remainingUses })
}

// توقيع رابط مشغّل Bunny Stream — Token Authentication
// الصيغة الرسميّة: token = SHA256(tokenKey + videoId + expires) — تحقّق منها بلوحة Bunny
function signBunnyEmbed() {
  const libraryId = process.env.BUNNY_LIBRARY_ID
  const videoId   = process.env.BUNNY_VIDEO_ID
  const tokenKey  = process.env.BUNNY_TOKEN_KEY
  if (!libraryId || !videoId || !tokenKey) return null

  const expires = Math.floor(Date.now() / 1000) + LINK_TTL_SEC
  const token = createHash('sha256').update(tokenKey + videoId + expires).digest('hex')
  return `https://iframe.mediadelivery.net/embed/${libraryId}/${videoId}?token=${token}&expires=${expires}&autoplay=true&preload=true`
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' }
  })
}
