import streamlit as st
import os
import sys
import re
import time
from crewai import Agent, Task, Crew, Process, LLM

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Pasukan AI Qwen - Tempatan",
    page_icon="🤖",
    layout="wide"
)

# --- KELAS UNTUK TANGKAP LOG (HIJACK TERMINAL) ---
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]') # Regex untuk buang kod warna ANSI

    def write(self, data):
        # Bersihkan data dari kod warna terminal yang pelik
        clean_data = self.colors.sub('', data)
        if clean_data.strip():
            self.buffer.append(clean_data)
            # Update log di skrin (Join 10 baris terakhir supaya tak lag)
            self.expander.code("\n".join(self.buffer[-20:]), language="text")

    def flush(self):
        pass

# --- UI SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    model_name = st.text_input("Nama Model", value="ollama/qwen3:8b") # Pastikan match dengan model anda
    st.info("Pastikan Ollama sedang berjalan.")

# --- UI UTAMA ---
st.title("🇲🇾 Pasukan Pembangun AI (Offline)")
st.markdown("Sistem Multi-Agent dikuasakan oleh **Qwen 3 (8B)** & **CrewAI** pada RTX 3080.")

def main():
    # Input
    topik = st.text_area("Masukkan Tugasan / Topik Projek:", height=100, 
                         placeholder="Contoh: Buat satu skrip Python untuk analisa data saham guna Pandas...")

    col1, col2 = st.columns([1, 5])
    with col1:
        start_btn = st.button("🚀 MULA MISI", type="primary")

    if start_btn and topik:
        
        os.environ["OPENAI_API_KEY"] = "NA"
        
        # Ruang Log
        st.write("---")
        st.subheader("🧠 Log Pemikiran Ejen (Real-Time)")
        log_box = st.empty() # Kotak kosong untuk diisi nanti

        with st.spinner('Sedang menginisialisasi Ejen...'):
            try:
                # --- SETUP LLM ---
                my_llm = LLM(
                    model=model_name,
                    base_url="http://localhost:11434"
                )

                # --- DEFINISI EJEN ---
                coder = Agent(
                    role='Pembangun Perisian Kanan',
                    goal='Menulis skrip Python yang efisien dan bersih.',
                    backstory='Pakar Python yang mementingkan kod yang kemas. Wajib guna komen Bahasa Melayu.',
                    llm=my_llm,
                    verbose=True
                )

                qa = Agent(
                    role='Pemeriksa Kualiti (QA)',
                    goal='Mencari bug dan memastikan logik kod betul.',
                    backstory='Seorang yang teliti. Akan reject kod jika tiada komen Bahasa Melayu atau logik salah.',
                    llm=my_llm,
                    verbose=True
                )

                writer = Agent(
                    role='Penulis Teknikal',
                    goal='Menulis dokumentasi projek dalam format Markdown.',
                    backstory='Pakar menterjemah kod teknikal kepada Bahasa Melayu yang mudah difahami.',
                    llm=my_llm,
                    verbose=True
                )

                # --- DEFINISI TUGASAN ---
                task_code = Task(
                    description=f"Tulis kod Python lengkap untuk: {topik}. Sertakan komen BM.",
                    expected_output="Kod Python berfungsi.",
                    agent=coder
                )

                task_review = Task(
                    description="Semak kod tersebut. Pastikan tiada ralat logik. Berikan feedback dalam BM.",
                    expected_output="Kod yang disahkan LULUS.",
                    agent=qa,
                    context=[task_code]
                )

                task_doc = Task(
                    description="Bina fail dokumentasi Markdown (Tajuk, Penerangan, Kod, Cara Guna).",
                    expected_output="Format Markdown lengkap.",
                    agent=writer,
                    context=[task_review],
                    output_file="Laporan_Projek.md"
                )

                crew = Crew(
                    agents=[coder, qa, writer],
                    tasks=[task_code, task_review, task_doc],
                    verbose=True,
                    process=Process.sequential,
                    # memory=True, # Disable memory sekejap kalau tak install embedder lagi
                )

                # --- TEKNIK HIJACK TERMINAL ---
                # Simpan stdout asal
                original_stdout = sys.stdout
                
                # Tukar stdout kepada kotak Streamlit kita
                sys.stdout = StreamToExpander(log_box)

                try:
                    # Jalankan Crew
                    result = crew.kickoff(inputs={'topic': topik})
                except Exception as e:
                    st.error(f"Error semasa run: {e}")
                    result = "Gagal."
                finally:
                    # PULANGKAN BALIK stdout KE ASAL (PENTING!)
                    sys.stdout = original_stdout

                st.success("✅ Misi Selesai!")
                
                # --- PAPARAN HASIL ---
                st.divider()
                st.header("📄 Hasil Dokumentasi Akhir")
                
                tab1, tab2 = st.tabs(["Paparan Cantik", "Kod Mentah"])
                
                with tab1:
                    st.markdown(result)
                with tab2:
                    st.code(result)

            except Exception as e:
                st.error(f"Ralat Sistem: {e}")

if __name__ == "__main__":
    main()