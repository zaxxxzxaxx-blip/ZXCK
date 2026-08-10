
# ZXCK PROJEK — WhatsApp Bot (Termux)

## 🔐 Login dashboard (rilis ini)
- Dashboard web (`/`, `/settings`, `/stats`, `/code`) sekarang **wajib login**
  pakai username + key. Keduanya dibuat **otomatis secara acak** saat bot
  pertama kali dijalankan — muncul sekali di terminal Termux, catat baik-baik.
  Kalau lupa, ketik `.dashboardinfo` di WhatsApp (khusus owner).
- Ganti kapan saja lewat WhatsApp: `.setdashboarduser [nama]` dan
  `.setdashboardkey [key]`.
- **Owner dapat notifikasi WhatsApp** setiap ada yang berhasil ATAU gagal
  login ke dashboard (kapan, dari IP mana). Matikan/nyalakan lewat
  `.loginnotif on` / `.loginnotif off`.
- **Owner bisa mematikan dashboard sepenuhnya** kapan pun lewat
  `.dashboardoff` (nyalakan lagi dengan `.dashboardon`) — semua akses,
  termasuk yang sudah login, langsung diblokir sampai dinyalakan lagi.
- Sesi login tersimpan di memori server (bukan file), otomatis kedaluwarsa
  12 jam, dan hilang total kalau bot direstart (harus login ulang — ini
  wajar & lebih aman daripada sesi permanen).
- Tema dashboard di-refresh (ungu-cyan neon, sesuai gaya "ZXCK PROJEK").

## 🛠️ Perbaikan besar (rilis sebelumnya)
- **PERBAIKAN UTAMA: bot berhenti merespon di chat pribadi & grup setelah reconnect.**
  Sebelumnya, listener pesan (`messages.upsert`) hanya dipasang SEKALI ke socket
  pertama saat bot baru nyala. Setiap kali WhatsApp memutus koneksi dan bot
  menyambung ulang otomatis (hal yang wajar & sering terjadi), Baileys membuat
  socket BARU — tapi listener lama masih menempel ke socket LAMA yang sudah
  mati. Akibatnya bot kelihatan "tersambung" di dashboard, tapi diam total,
  baik di chat pribadi maupun grup. Sekarang listener dipasang ulang ke setiap
  socket baru lewat `pasangHandler()` di `index.js` + `lib/connection.js`.
- **Fitur yang tadinya cuma pesan placeholder sekarang benar-benar jalan:**
  `.sticker` & `.toimage` (pakai ffmpeg, lihat `lib/media.js`), `.tebakangka`
  (game tebak angka beneran, ketik angka langsung tanpa prefix untuk
  menebak, `.nyerah` untuk berhenti), `.hitungmundur` (pengingat asli lewat
  timer), `.broadcast` (kirim ke semua chat yang pernah ngobrol dengan bot,
  lihat `lib/chats.js`, tetap dijeda anti-spam).
- **Halaman baru "Lihat Kode"** (`/code` di dashboard) — tombol per-berkas
  untuk melihat isi kode lewat browser tanpa perlu buka file manager;
  folder `session/` (kredensial WhatsApp) dan `web/cert/` (kunci HTTPS)
  sengaja TIDAK PERNAH ditampilkan di sana.
- Nomor owner sudah diisi di `config.js`.

## 🆕 Pembaruan sebelumnya
- **Owner sekarang bisa chat & pakai perintah** — sebelumnya pesan dari HP owner sendiri (chat pribadi ke diri sendiri) selalu diabaikan. Sekarang bot membedakan mana balasan otomatisnya sendiri vs pesan asli yang diketik owner (lihat `lib/anti-ban.js` fungsi `tandaiPesanBot`/`apakahPesanBot`).
- **Halaman Pengaturan** (`/settings` di dashboard web) — nyalakan/matikan fitur (respon di grup, respon di chat pribadi, auto-read, auto-typing, antilink, welcome) langsung dari browser, tanpa edit file.
- **Halaman Performa** (`/stats` di dashboard web) — uptime, jumlah pesan masuk, jumlah perintah dijalankan, pemakaian memori, dan perintah paling sering dipakai.
- **Menu beda tampilan**: owner ketik `.menu` dapat daftar teks lengkap; user biasa dapat tampilan bergambar (banner) dengan menu di caption.
- **Menu disensor di grup**: `.menu` di grup tidak lagi menampilkan daftar lengkap secara publik — bot balas singkat di grup lalu mengirim menu lengkap ke chat pribadi (DM) pengirim.
- **Perintah owner-only** (`broadcast`, `setbio`, `block`, `unblock`, `restart`, `join`, `antilink`, `welcome`) sekarang benar-benar ditolak kalau dipakai user biasa.
- Semua pengaturan tersimpan di `settings.json` (dibuat otomatis saat pertama jalan) dan langsung berlaku tanpa restart bot.


Bot WhatsApp pribadi berbasis [Baileys](https://github.com/WhiskeySockets/Baileys), dengan lebih dari 50 perintah, dashboard web (HTTP/HTTPS), dan tautan lewat **QR code** atau **kode pasangan (pairing code)**.

## ⚠️ Catatan jujur soal "anti banned"
Tidak ada bot pihak ketiga yang bisa **menjamin 100% tidak akan pernah dibanned** — Baileys memakai protokol tidak resmi, jadi risiko selalu ada, terutama kalau dipakai untuk spam/broadcast massal. Yang bisa dilakukan (dan sudah diterapkan di kode ini) adalah **menurunkan risiko**:
- Jeda antar pesan otomatis (`lib/anti-ban.js`)
- Batas jumlah pesan per menit
- Hindari broadcast ke banyak nomor sekaligus dalam waktu singkat
- Jangan spam join grup / add kontak asing
- Gunakan bot ini untuk keperluan pribadi/wajar, bukan spam massal

## 1. Instalasi di Termux
```bash
pkg update && pkg upgrade -y
pkg install -y nodejs-lts git openssl-tool
```

Pindahkan folder `zxck-projek` ini ke HP kamu (lewat kabel/USB, Google Drive, dll), lalu:
```bash
cd zxck-projek
npm install
```

## 2. Atur konfigurasi
Buka `config.js`, isi:
- `OWNER_NUMBER` — nomor WhatsApp kamu, format `62812xxxxxxx` (tanpa `+`, tanpa `0` di depan)
- `USE_PAIRING_CODE` — `true` untuk tautan pakai kode 8 digit, `false` untuk tautan pakai QR

## 3. Menjalankan bot
```bash
npm start
```
- Nomor akan **divalidasi dulu** (format, panjang digit) sebelum kode pasangan diminta — kalau salah format, bot akan minta kamu memasukkan ulang.
- Kalau `USE_PAIRING_CODE = true`: kode 8 digit akan muncul di terminal **dan** di dashboard web. Buka WhatsApp di HP kamu → **Perangkat Tertaut** → **Tautkan dengan nomor telepon** → masukkan kode tersebut.
- Kalau `USE_PAIRING_CODE = false`: QR code akan muncul di terminal **dan** di dashboard web. Scan dengan WhatsApp → **Perangkat Tertaut** → **Tautkan Perangkat**.
- Sesi login tersimpan di folder `session/` — sekali tertaut, tidak perlu tautkan ulang setiap buka bot (kecuali logout manual).

## 4. Dashboard web
Setelah `npm start`, buka di browser HP/laptop kamu:
```
http://localhost:3000
```
Tampilan menunjukkan status koneksi, QR/kode pasangan secara live, dan nomor yang tertaut.

### Mengaktifkan HTTPS
Karena sertifikat HTTPS asli butuh domain, untuk pemakaian lokal buat sertifikat self-signed:
```bash
mkdir -p web/cert
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout web/cert/key.pem -out web/cert/cert.pem -days 365 \
  -subj "/CN=localhost"
```
Jalankan ulang `npm start` — dashboard HTTPS aktif di `https://localhost:3001` (browser akan menampilkan peringatan "not secure" karena sertifikat self-signed, itu wajar untuk pemakaian lokal — klik "Lanjutkan/Advanced → Proceed").

Kalau kamu punya domain asli dan ingin sertifikat sah (Let's Encrypt), pakai `certbot` lalu arahkan `keyPath`/`certPath` di `web/server.js` ke sertifikat tersebut.

## 5. Fitur (50+)
Semua perintah pakai awalan `.` (bisa diganti di `config.js` → `PREFIX`). Ketik `.menu` di chat manapun setelah bot tertaut untuk melihat daftar lengkap — dibagi kategori: Umum, Admin Grup, Teks & Konversi, Hiburan, Utilitas, dan Owner. Daftar lengkap juga ada di `commands/index.js`.

Beberapa fitur (sticker/toimage) butuh `ffmpeg` terpasang:
```bash
pkg install ffmpeg
```

## 6. Struktur folder
```
zxck-projek/
├── index.js           # entry point
├── config.js           # pengaturan bot
├── lib/
│   ├── connection.js    # koneksi WA (QR & pairing code + validasi nomor)
│   └── anti-ban.js       # antrian & jeda kirim pesan
├── commands/
│   └── index.js          # semua 50+ perintah
├── web/
│   ├── server.js          # dashboard HTTP/HTTPS
│   └── cert/                # taruh key.pem & cert.pem di sini
├── public/
│   ├── index.html, style.css, app.js, logo.svg
└── session/             # sesi login WhatsApp (jangan dibagikan ke orang lain!)
```

## 7. Keamanan
- **Jangan pernah membagikan folder `session/`** ke siapa pun — isinya setara akses penuh ke akun WhatsApp kamu.
- Bot ini untuk keperluan pribadi. Jangan dipakai untuk spam, penipuan, atau mengganggu orang lain.
