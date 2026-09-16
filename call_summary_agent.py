#!/usr/bin/env python3
"""
Agente de Resumen de Llamadas
Transcribe audio con Whisper y genera resumen estructurado con Claude Opus 5.
"""

import sys
import argparse
import anthropic


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


def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """Transcribe audio using local Whisper model."""
    try:
        import whisper
    except ImportError:
        print(
            "\nError: Se requiere el paquete openai-whisper para transcribir audio.\n"
            "Instálalo con:\n"
            "  pip install openai-whisper\n\n"
            "Alternativa: usa --transcript para pasar una transcripción en texto."
        )
        sys.exit(1)

    print(f"⏳ Cargando modelo Whisper '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"🎙️  Transcribiendo: {audio_path}")
    result = model.transcribe(audio_path, verbose=False)

    transcript = result["text"].strip()
    word_count = len(transcript.split())
    print(f"✅ Transcripción completa ({word_count} palabras)\n")
    return transcript


def load_transcript_file(path: str) -> str:
    """Load transcript from a text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def summarize_call(transcript: str) -> None:
    """Stream a structured call summary from Claude Opus 5."""
    client = anthropic.Anthropic()

    print("⚡ Generando resumen con Claude Opus 5...\n")
    print("=" * 60)

    with client.messages.stream(
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
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)

    print("\n" + "=" * 60 + "\n")


def interactive_mode() -> str:
    """Prompt user for audio path or transcript paste."""
    print("🎙️  Agente de Resumen de Llamadas")
    print("-" * 40)
    print("1. Transcribir archivo de audio")
    print("2. Pegar transcripción en texto")
    print()

    choice = input("Elige una opción (1/2): ").strip()

    if choice == "1":
        audio_path = input("Ruta al archivo de audio: ").strip()
        whisper_model = input("Tamaño del modelo Whisper [base/small/medium/large] (Enter = base): ").strip() or "base"
        return transcribe_audio(audio_path, whisper_model)

    elif choice == "2":
        print("\nPega la transcripción y presiona Enter + Ctrl+D (Linux/Mac) o Ctrl+Z Enter (Windows):\n")
        lines = []
        try:
            while True:
                lines.append(input())
        except EOFError:
            pass
        return "\n".join(lines).strip()

    else:
        print("Opción no válida.")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agente de Resumen de Llamadas — transcribe audio y resume con Claude.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python call_summary_agent.py llamada.mp3
  python call_summary_agent.py llamada.wav --whisper-model small
  python call_summary_agent.py --transcript transcripcion.txt
        """,
    )
    parser.add_argument(
        "audio_file",
        nargs="?",
        help="Ruta al archivo de audio (mp3, mp4, wav, m4a, ogg, …)",
    )
    parser.add_argument(
        "--transcript",
        "-t",
        metavar="FILE",
        help="Archivo .txt con la transcripción ya hecha (omite Whisper)",
    )
    parser.add_argument(
        "--whisper-model",
        metavar="SIZE",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Tamaño del modelo Whisper: tiny/base/small/medium/large (default: base)",
    )

    args = parser.parse_args()

    if args.transcript:
        transcript = load_transcript_file(args.transcript)
        print(f"📄 Usando transcripción: {args.transcript}")
    elif args.audio_file:
        transcript = transcribe_audio(args.audio_file, args.whisper_model)
    else:
        transcript = interactive_mode()

    if not transcript:
        print("Error: no hay contenido para resumir.")
        sys.exit(1)

    summarize_call(transcript)


if __name__ == "__main__":
    main()
