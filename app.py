#!/usr/bin/env python3
"""
Interfaz web para el Agente de Resumen de Llamadas
Usa Streamlit para una interfaz visual amigable
"""

import streamlit as st
import anthropic
import tempfile
import os

st.set_page_config(
    page_title="Resumen de Llamadas",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🎙️ Agente de Resumen de Llamadas")
st.markdown("Sube un audio o pega una transcripción para obtener un resumen estructurado")

SYSTEM_PROMPT = """Eres un asistente especializado en resumir llamadas y reuniones de negocios.
Analiza transcripciones y genera resúmenes ejecutivos claros, concisos y accionables.
Responde siempre en el mismo idioma de la transcripción."""

SUMMARY_TEMPLATE = """Analiza la siguiente transcripción y genera un resumen ejecutivo con este formato exacto:

## 📋 Resumen de la Llamada

### 🎯 Puntos Importantes Tratados
- [Tema 1: descripción breve del punto discutido]
- [Tema 2: ...]
- (uno por punto relevante)

### ✅ Conclusiones
- [Decisión o acuerdo alcanzado]
- [Resultado importante de la conversación]

### 🚀 Siguientes Pasos
- [Acción concreta] — Responsable: [nombre si se menciona] — Fecha: [fecha si se menciona]
- (una línea por acción)

Si no hay suficiente información para alguna sección, indícalo brevemente.

---
**Transcripción:**
{transcript}"""


def transcribe_audio(audio_file) -> str:
    """Transcribe audio using Whisper."""
    try:
        import whisper
    except ImportError:
        st.error("⚠️ Error: openai-whisper no está instalado")
        st.info("Por favor instala: `pip install openai-whisper`")
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_file.read())
        tmp_path = tmp.name

    try:
        with st.spinner("🎙️ Transcribiendo audio... (puede tomar un momento)"):
            model = whisper.load_model("base")
            result = model.transcribe(tmp_path, verbose=False)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)


def summarize_transcript(transcript: str) -> str:
    """Generate summary using Claude Opus 5."""
    client = anthropic.Anthropic()

    with st.spinner("⚡ Generando resumen con Claude..."):
        message = client.messages.create(
            model="claude-opus-5",
            max_tokens=4096,
            thinking={"type": "adaptive"},
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": SUMMARY_TEMPLATE.format(transcript=transcript),
                }
            ],
        )
    return message.content[0].text


# Interfaz
col1, col2 = st.columns(2)

with col1:
    st.subheader("📤 Subir Audio")
    audio_file = st.file_uploader(
        "Elige un archivo de audio",
        type=["mp3", "wav", "m4a", "ogg", "mp4"],
        help="Formatos soportados: MP3, WAV, M4A, OGG, MP4"
    )

with col2:
    st.subheader("✍️ O pega Transcripción")
    transcript_text = st.text_area(
        "Pega aquí la transcripción de la llamada",
        height=200,
        placeholder="Ej: Cliente: Hola, quería hablar sobre...\nEmpresa: Claro, adelante..."
    )

st.divider()

if st.button("🚀 Generar Resumen", use_container_width=True, type="primary"):
    transcript = None

    if audio_file:
        st.info("📥 Procesando archivo de audio...")
        transcript = transcribe_audio(audio_file)
        if transcript:
            st.success(f"✅ Audio transcrito ({len(transcript.split())} palabras)")
            with st.expander("Ver transcripción completa"):
                st.text(transcript)

    elif transcript_text:
        transcript = transcript_text
        st.success(f"✅ Usando transcripción ({len(transcript.split())} palabras)")

    else:
        st.error("❌ Por favor sube un audio o pega una transcripción")

    if transcript:
        st.divider()
        st.subheader("📋 Resumen Ejecutivo")

        try:
            summary = summarize_transcript(transcript)
            st.markdown(summary)

            st.divider()
            st.download_button(
                "📥 Descargar resumen como texto",
                data=summary,
                file_name="resumen_llamada.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"❌ Error al generar resumen: {str(e)}")
            st.info("Verifica que tu API key de Anthropic esté configurada en la variable `ANTHROPIC_API_KEY`")

st.divider()
st.markdown("""
### 💡 Consejos
- Los audios se procesan **localmente** con Whisper (sin enviar a servidores externos)
- El resumen se genera con **Claude Opus 5** para análisis profundo
- Formatos soportados: MP3, WAV, M4A, OGG, MP4
- Puedes descargar el resumen como archivo de texto

### 🔑 Configuración
Asegúrate de tener tu API key de Anthropic:
```bash
export ANTHROPIC_API_KEY="tu-clave-aqui"
```
""")
