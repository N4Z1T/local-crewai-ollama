import os
from crewai import Agent, Task, Crew, Process, LLM

# --- 1. KONFIGURASI SISTEM ---
# "Tipu" sistem supaya tidak cari OpenAI API Key
os.environ["OPENAI_API_KEY"] = "NA"

# Setup LLM ke Localhost (Ollama)
# Nota: Model 'llama3.1' (8B) biasanya lebih fasih BM berbanding 'llama3.2' (3B).
# Kalau PC anda kuat (RTX 3080), saya sarankan tukar "ollama/llama3.2" ke "ollama/llama3.1"
my_llm = LLM(
    model="ollama/qwen3:8b", 
    base_url="http://localhost:11434"
)

# --- 2. DEFINISI EJEN (DALAM BAHASA MELAYU) ---

# Ejen 1: Si Penulis Kod
jurutaip_kod = Agent(
    role='Pembangun Perisian Kanan (Python)',
    goal='Menulis skrip Python yang efisien berdasarkan topik: {topik}.',
    backstory='''
        Anda adalah pakar pengaturcaraan Python yang berpengalaman. 
        Anda sangat bangga dengan kemahiran anda.
        PENTING: Anda MESTI menulis semua penjelasan, komen (comments), dan dokumentasi dalam BAHASA MELAYU sepenuhnya.
        Hanya sintaks kod (seperti def, class, import) dibenarkan dalam Bahasa Inggeris.
    ''',
    llm=my_llm,
    verbose=True
)

# Ejen 2: Si Pemeriksa Kualiti (QA)
pemeriksa_kualiti = Agent(
    role='Pegawai Jaminan Kualiti (QA)',
    goal='Memastikan kod berfungsi, tiada bug, dan menepati piawaian industri.',
    backstory='''
        Anda seorang yang sangat teliti dan tegas. 
        Tugas anda adalah mencari kesalahan logik dalam kod.
        PENTING: Anda akan menolak (reject) kod jika Coder menggunakan Bahasa Inggeris dalam penjelasan.
        Kritikan anda mestilah membina dan dalam Bahasa Melayu.
    ''',
    llm=my_llm,
    verbose=True
)

# Ejen 3: Penulis Laporan
penulis_teknikal = Agent(
    role='Penulis Dokumentasi Teknikal',
    goal='Menghasilkan fail dokumentasi yang kemas dan mudah difahami orang awam.',
    backstory='''
        Anda pakar menterjemah istilah teknikal yang sukar kepada Bahasa Melayu yang mudah.
        Anda bertugas menyusun hasil kerja Coder dan QA menjadi satu laporan lengkap.
    ''',
    llm=my_llm,
    verbose=True
)

# --- 3. DEFINISI TUGASAN (TASKS) ---

tugasan_kod = Task(
    description='''
        Tulis satu skrip Python yang lengkap untuk menyelesaikan masalah: {topik}.
        Pastikan kod tersebut mempunyai 'comments' dalam Bahasa Melayu untuk setiap fungsi.
    ''',
    expected_output='Satu blok kod Python yang berfungsi sepenuhnya dengan komen Bahasa Melayu.',
    agent=jurutaip_kod
)

tugasan_review = Task(
    description='''
        Semak kod yang dihasilkan oleh Pembangun Perisian.
        Cari sebarang potensi ralat (bugs) atau kesalahan logik.
        Pastikan pembangun menggunakan komen dalam Bahasa Melayu.
        Jika ada salah, berikan arahan pembaikan.
    ''',
    expected_output='Laporan semakan kualiti dalam Bahasa Melayu dan kod yang telah disahkan LULUS.',
    agent=pemeriksa_kualiti,
    context=[tugasan_kod] # QA ambil kerja Coder
)

tugasan_laporan = Task(
    description='''
        Berdasarkan kod yang telah diluluskan, bina satu fail dokumentasi format Markdown (.md).
        Fail mesti mengandungi:
        1. Tajuk Projek
        2. Penerangan Masalah
        3. Cara Penggunaan (Tutorial ringkas)
        4. Kod Penuh
    ''',
    expected_output='Fail Markdown yang lengkap dalam Bahasa Melayu.',
    agent=penulis_teknikal,
    context=[tugasan_review], # Writer ambil hasil QA
    output_file='Laporan_Projek.md' # <--- NAMA FAIL OUTPUT
)

# --- 4. PASUKAN BERKUMPUL (CREW) ---

pasukan_ai = Crew(
    agents=[jurutaip_kod, pemeriksa_kualiti, penulis_teknikal],
    tasks=[tugasan_kod, tugasan_review, tugasan_laporan],
    process=Process.sequential, # Jalan ikut urutan: Kod -> QA -> Tulis
    verbose=True
)

# --- 5. JALANKAN MISI ---

if __name__ == "__main__":
    print("\n==============================================")
    print("   MEMULAKAN SISTEM EJEN AI (BAHASA MELAYU)   ")
    print("==============================================")
    
    # Masukkan topik anda di sini
    input_topik = "Satu program untuk analisa saham menggunakan Python"
    
    hasil = pasukan_ai.kickoff(inputs={'topik': input_topik})
    
    print("\n\n################################################")
    print("## MISI SELESAI! SILA SEMAK 'Laporan_Projek.md' ##")
    print("################################################\n")
