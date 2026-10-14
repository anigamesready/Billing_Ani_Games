# Ani-Games Reseller v1.0.0 — GitHub build branch

Branch ini menyiapkan build APK reseller terpisah dari branch `main` dan ZIP Billing master.

- Workflow: `.github/workflows/build-reseller-apk.yml`
- UI paket: `reseller/ui-v1.0.0.tar.gz` (berisi `index.html` dan `admin-control.html`; workflow mengekstraknya ke WebView asset).
- Sumber Android awal diambil dari ZIP build v11.29.1 yang sudah ada pada repository ini.
- Setelah workflow berhasil, unduh artifact `Ani-Games-Reseller-v1.0.0-debug-apk` dari halaman Actions.
- Package ID terpisah: `com.anigames.reseller`. Label launcher: `Ani-Games Reseller`.
- UI login dan dashboard memakai `icon/logo.png`; ikon launcher Android tetap disertakan pada semua densitas.

Build ini menghasilkan **debug APK untuk pengujian**, bukan APK release yang ditandatangani dengan keystore distribusi. Uji login reseller, refresh status, tambah/edit rental, sinkronisasi PC, dan alarm pada perangkat fisik sebelum distribusi.
