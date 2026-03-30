# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **Clarissa Dhea Allisya** \
SUNet ID: **2410817220023** \
Citations: **Semgrep, Claude Haiku 4.5 (via VS Code), dan Gemini**

This assignment took me about **3** hours to do. 


## Brief findings overview 
> Semgrep mendeteksi total **39 findings** dalam project ini, yang terbagi menjadi dua kategori utama: **Supply Chain Vulnerabilities (SCA)** seperti CVE pada PyYAML (CVE-2020-14343), requests, dan Werkzeug yang memerlukan dependency upgrades, serta **Code Vulnerabilities (SAST)** yang mencakup XSS, SQL Injection, Command Injection, dan Path Traversal. Saya fokus pada **3 kerentanan paling krusial** yang berdampak langsung pada keamanan eksekusi aplikasi, mengabaikan beberapa noisy rules atau temuan Supply Chain tingkat rendah yang tidak menghalangi eksekusi.

## Fix #1
a. File and line(s)
> `week6/frontend/app.js`, **line 14**

b. Rule/category Semgrep flagged
> `javascript.browser.security.insecure-document-method.insecure-document-method`

c. Brief risk description
> Penggunaan `innerHTML` dengan variabel yang tidak divalidasi memungkinkan penyerang mengeksekusi payload skrip berbahaya (Cross-Site Scripting/XSS). Data dari API backend dapat mengandung tag HTML atau JavaScript yang dieksekusi oleh browser.

d. Your change (short code diff or explanation, AI coding tool usage)
> Saya meminta AI untuk mengganti penggunaan `innerHTML` dengan metode DOM yang aman. Perubahan mengganti string template dengan pemanggilan eksplisit: membuat elemen `<strong>`, mengisi `textContent` untuk title, dan menggunakan `createTextNode()` untuk content, kemudian menggabungkannya dengan `appendChild()`.

e. Why this mitigates the issue
> Penggunaan `textContent` memaksa browser untuk merender input secara ketat sebagai teks biasa (sanitized DOM writes), sehingga mencegah tag HTML dan skrip tereksekusi. `createTextNode()` juga tidak melakukan parsing HTML pada konten yang disematkan.

## Fix #2
a. File and line(s)
> `week6/backend/app/routers/notes.py`, **line 112**

b. Rule/category Semgrep flagged
> `python.fastapi.os.tainted-os-command-stdlib-fastapi-secure-default`

c. Brief risk description
> Fungsi `subprocess.run()` menggunakan argumen `shell=True` dengan input dinamis (`cmd`) yang tidak divalidasi, sehingga memungkinkan Command Injection. Peretas dapat merangkai perintah tambahan menggunakan operator shell seperti `&&` atau `;` untuk mengeksekusi kode OS sewenang-wenang (Remote Code Execution).

d. Your change (short code diff or explanation, AI coding tool usage)
> Saya meminta AI untuk menjadikan kode ini "secure by default". AI menghapus parameter `shell=True` (menjadi default `False`) dan menggunakan `shlex.split(cmd)` untuk memecah string input menjadi list argumen individual, sehingga input hanya diterima sebagai program name + arguments, bukan sebagai shell command.

e. Why this mitigates the issue
> Tanpa shell system (`shell=False` adalah default), karakter meta-shell seperti `|`, `&&`, `;`, atau backticks tidak akan diinterpretasi oleh shell. Fungsi `shlex.split()` memastikan input hanya diurai sebagai argumen teks biasa yang aman, sehingga setiap elemen dari command string diperlakukan sebagai literal string, bukan dievaluasi dinamis.

## Fix #3
a. File and line(s)
> `week6/requirements.txt` (multiple dependencies updated)

b. Rule/category Semgrep flagged
> Supply Chain Vulnerabilities (SCA): `pyyaml` - CVE-2020-14343, dan beberapa findings SCA lainnya pada `requests`, `Werkzeug`, `Jinja2`, `pydantic`

c. Brief risk description
> Versi library yang usang memiliki kerentanan yang sudah diketahui. Khususnya, PyYAML 5.1 rentan terhadap **Remote Code Injection** (CVE-2020-14343) saat melakukan deserialisasi data yang tidak tepercaya. Library lain seperti Werkzeug, Jinja2, dan requests juga memiliki CVE yang belum di-patch di versi yang sedang digunakan.

d. Your change (short code diff or explanation, AI coding tool usage)
> Saya meminta AI untuk melakukan **dependency upgrades** sesuai rekomendasi Semgrep: PyYAML (5.1 → 5.4), Werkzeug (0.14.1 → 3.1.6), Jinja2 (2.10.1 → 3.1.6), requests (2.19.1 → 2.33.0), dan pydantic (1.5.1 → 2.4.0). Semua versi baru dipilih sesuai dengan versi minimum yang aman menurut Semgrep.

e. Why this mitigates the issue
> Memperbarui dependensi ke versi yang sudah di-patch akan langsung menutup celah keamanan pihak ketiga dari akarnya tanpa perlu mengubah logika aplikasi itu sendiri. CVE yang sudah diperbaiki di versi terbaru tidak lagi dapat dieksploitasi, sehingga mengurangi attack surface dari supply chain perspective.