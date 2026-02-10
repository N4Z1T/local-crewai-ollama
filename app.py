import streamlit as st
import os
import sys
import re
from crewai import Agent, Task, Crew, Process, LLM

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Pasukan AI Universal - Polyglot",
    page_icon="🌍",
    layout="wide"
)

# --- 2. FUNGSI PEMBANTU (UPGRADED) ---
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

    def write(self, data):
        clean_data = self.colors.sub('', data)
        if clean_data.strip():
            self.buffer.append(clean_data)
            self.expander.code("\n".join(self.buffer[-15:]), language="text")

    def flush(self):
        pass

# Fungsi Pintar: Detect Bahasa & Kod
def extract_code_and_extension(text):
    # Regex untuk tangkap ```bahasa ... kod ... ```
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    if matches:
        # Ambil blok kod terakhir (biasanya yang paling lengkap)
        lang, code = matches[-1]
        lang = lang.lower().strip()
        
        # Mapping bahasa ke extension fail
        ext_map = {
            'python': 'py', 'py': 'py',
            'html': 'html',
            'css': 'css',
            'javascript': 'js', 'js': 'js',
            'cpp': 'cpp', 'c++': 'cpp', 'c': 'c',
            'java': 'java',
            'sql': 'sql',
            'json': 'json',
            'markdown': 'md',
            'bash': 'sh', 'sh': 'sh'
        }
        
        file_ext = ext_map.get(lang, 'txt') # Default .txt kalau tak kenal
        return code, file_ext, lang
    else:
        return "# Tiada kod dijumpai.", "txt", "text"

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("🎛️ Pusat Kawalan")
    
    st.subheader("1. Mod Operasi")
    mod_operasi = st.radio(
        "Pilih Jenis Misi:",
        ["✨ Jana Kod Baru", "🔍 Audit Kod Lama", "🗣️ Perbincangan (Debat)"],
    )
    
    st.divider()
    st.subheader("2. Tetapan Bahasa")
    bahasa_target = st.text_input("Bahasa Sasaran (Optional)", placeholder="Contoh: HTML, C++, Python...")
    
    model_name = st.text_input("Model Ollama", value="ollama/qwen3:8b")

    st.divider()
    st.subheader("3. Ahli Pasukan")
    with st.expander("Lihat Pasukan", expanded=True):
        if mod_operasi == "✨ Jana Kod Baru":
            st.info("🧑‍💻 **Engineer:** Tulis Kod (Polyglot)")
            st.warning("🕵️ **QA:** Semak Syntax")
        elif mod_operasi == "🔍 Audit Kod Lama":
            st.error("🕵️ **QA (Lead):** Cari Bug")
            st.info("🧑‍💻 **Engineer:** Fix Kod")
        else:
            st.info("🔵 **Optimis** vs 🔴 **Skeptik**")

# --- 4. UI UTAMA ---
st.title(f"🌍 Pasukan AI Universal: {mod_operasi}")

def main():
    
    # Input Logic
    if mod_operasi == "✨ Jana Kod Baru":
        placeholder_text = "Contoh: Buat landing page guna HTML & CSS..."
        if bahasa_target:
            placeholder_text = f"Contoh: Buat sistem login guna {bahasa_target}..."
        user_input = st.text_area("🎯 Masukkan Idea Projek:", height=100, placeholder=placeholder_text)
        btn_text = "🚀 JANA KOD"
        
    elif mod_operasi == "🔍 Audit Kod Lama":
        user_input = st.text_area("💻 Tampal Kod Anda (Apa shj bahasa):", height=200, placeholder="<html>... atau #include <iostream>...")
        btn_text = "🔍 AUDIT KOD"
        
    else: 
        user_input = st.text_area("🗣️ Topik Perbincangan:", height=100, placeholder="Contoh: React vs Vue?")
        btn_text = "🎙️ MULAKAN DEBAT"

    col1, col2 = st.columns([1, 5])
    with col1:
        start_btn = st.button(btn_text, type="primary", use_container_width=True)

    if start_btn and user_input:
        
        # --- MATIKAN INTERNET (Telemetry) ---
        os.environ["OPENAI_API_KEY"] = "NA"
        os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"
        os.environ["OTEL_SDK_DISABLED"] = "true"
        
        with st.status("🤖 Sedang Memproses...", expanded=True) as status:
            st.write("🔌 Menghubungkan ke Neural Network...")
            log_expander = st.expander("Log Terminal Live", expanded=True)
            
            try:
                my_llm = LLM(model=model_name, base_url="http://localhost:11434")

                # --- EJEN YANG LEBIH UNIVERSAL (TUKAR DARI 'PYTHON DEV' KE 'SOFTWARE ENGINEER') ---
                # Kita guna variable 'bahasa_target' untuk bagi konteks pada ejen
                konteks_bahasa = f"dalam bahasa {bahasa_target}" if bahasa_target else "dalam bahasa pengaturcaraan yang sesuai"

                engineer = Agent(
                    role='Senior Software Engineer',
                    goal=f'Menulis kod {konteks_bahasa} yang efisien, moden dan bersih.',
                    backstory="Anda pakar pengaturcaraan 'Polyglot'. Anda mahir C++, HTML, Python, JS, dan SQL. Anda ikut best practice industri.",
                    llm=my_llm, verbose=True
                )

                qa = Agent(
                    role='Code Quality Auditor',
                    goal='Mencari syntax error, bug logik, dan isu keselamatan.',
                    backstory="Anda sangat teliti. Anda boleh baca pelbagai bahasa pengaturcaraan dan cari kesalahan.",
                    llm=my_llm, verbose=True
                )

                writer = Agent(
                    role='Technical Writer',
                    goal='Menyediakan dokumentasi teknikal.',
                    backstory="Pakar dokumentasi yang menerangkan kod kompleks dengan bahasa mudah.",
                    llm=my_llm, verbose=True
                )
                
                # Ejen Debat (Kekal sama)
                optimis = Agent(role='The Optimist', goal='Menyokong idea.', backstory='Positif & Visionary.', llm=my_llm)
                skeptik = Agent(role='The Skeptic', goal='Mencari risiko.', backstory='Kritikal & Hati-hati.', llm=my_llm)
                moderator = Agent(role='Moderator', goal='Rumusan.', backstory='Neutral.', llm=my_llm)

                tasks_list = []
                
                # --- LOGIK TUGASAN ---
                if mod_operasi == "✨ Jana Kod Baru":
                    task1 = Task(description=f"Tulis kod lengkap untuk: {user_input}. Pastikan syntax betul.", expected_output="Blok Kod Lengkap.", agent=engineer)
                    task2 = Task(description="Semak kod tersebut.", expected_output="Kod yang disahkan.", agent=qa, context=[task1])
                    task3 = Task(description="Buat dokumentasi cara guna kod itu.", expected_output="Markdown.", agent=writer, context=[task2])
                    tasks_list = [task1, task2, task3]
                    crew = Crew(agents=[engineer, qa, writer], tasks=tasks_list, verbose=True)

                elif mod_operasi == "🔍 Audit Kod Lama":
                    task1 = Task(description=f"Analisa kod ini:\n```\n{user_input}\n```\nCari bug/error.", expected_output="Laporan Bug.", agent=qa)
                    task2 = Task(description="Baiki kod berdasarkan laporan QA.", expected_output="Kod Lengkap yang Dibaiki.", agent=engineer, context=[task1])
                    task3 = Task(description="Laporan akhir.", expected_output="Markdown.", agent=writer, context=[task2])
                    tasks_list = [task1, task2, task3]
                    crew = Crew(agents=[qa, engineer, writer], tasks=tasks_list, verbose=True)

                else: # Debat
                    task1 = Task(description=f"Kelebihan: {user_input}", expected_output="Poin Positif.", agent=optimis)
                    task2 = Task(description=f"Kekurangan/Risiko: {user_input}", expected_output="Poin Negatif.", agent=skeptik)
                    task3 = Task(description="Rumusan akhir.", expected_output="Laporan Debat.", agent=moderator, context=[task1, task2])
                    tasks_list = [task1, task2, task3]
                    crew = Crew(agents=[optimis, skeptik, moderator], tasks=tasks_list, verbose=True)

                # --- RUN ---
                sys.stdout = StreamToExpander(log_expander)
                result = crew.kickoff()
                sys.stdout = sys.__stdout__
                
                status.update(label="✅ Siap!", state="complete", expanded=False)

                # --- RESULT ---
                st.divider()
                
                if mod_operasi == "🗣️ Perbincangan (Debat)":
                     st.markdown(result)
                     st.download_button("💾 Simpan Rumusan (.md)", str(result), "rumusan.md")
                else:
                    # Guna fungsi pengesan bahasa baru
                    kod_bersih, file_ext, dikesan = extract_code_and_extension(str(result))
                    
                    st.success(f"Bahasa Dikesan: **{dikesan.upper()}** (Fail: `.{file_ext}`)")
                    
                    tab1, tab2 = st.tabs(["Laporan (.md)", f"Kod (. {file_ext})"])
                    
                    with tab1:
                        st.markdown(result)
                        st.download_button("💾 Download Laporan", str(result), "laporan.md")
                        
                    with tab2:
                        st.code(kod_bersih, language=dikesan if dikesan != 'txt' else None)
                        st.download_button(
                            label=f"⬇️ Muat Turun Kod (.{file_ext})",
                            data=kod_bersih,
                            file_name=f"projek_ai.{file_ext}",
                            mime="text/plain"
                        )

            except Exception as e:
                sys.stdout = sys.__stdout__
                st.error(f"Ralat: {e}")

if __name__ == "__main__":
    main()
