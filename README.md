# 🎙️ Agente de Resumen de Llamadas

Transcribe audios y genera resúmenes ejecutivos automáticamente con **Claude Opus 5** + **Whisper**.

## ✨ Características

- 🎵 **Transcripción automática** — Convierte audio a texto localmente (sin costo)
- 📋 **Resumen estructurado** — Genera automáticamente:
  - Puntos importantes tratados
  - Conclusiones y decisiones
  - Siguientes pasos con responsables
- 🖥️ **Interfaz visual** — No necesitas abrir terminal
- 💾 **Descarga resultados** — Guarda el resumen como archivo

## 🚀 Cómo usar (sin terminal)

### Opción 1: Interfaz Web (Recomendado para no técnicos)

1. **Instala** (una única vez):
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecuta** la app web:
   ```bash
   streamlit run app.py
   ```

3. Se abrirá automáticamente en tu navegador. Luego:
   - Sube un archivo de audio, O
   - Pega la transcripción
   - Haz clic en "Generar Resumen"
   - Descarga el resultado 📥

### Opción 2: Línea de Comandos

```bash
# Con archivo de audio
python call_summary_agent.py llamada.mp3

# Con transcripción en texto
python call_summary_agent.py --transcript transcripcion.txt

# Modo interactivo
python call_summary_agent.py
```

## 📦 Requisitos

- **Python 3.7+** 
- **Internet** (para Claude API)
- **API Key de Anthropic** — [Obtén una gratis aquí](https://console.anthropic.com/)

## 🔧 Instalación Completa

### Windows (Lo más fácil)

1. Descarga e instala [Python 3.10+](https://www.python.org/downloads/)
   - ⚠️ Marca "Add Python to PATH"

2. Abre PowerShell o CMD en esta carpeta (clic derecho → "Abrir PowerShell aquí")

3. Instala las librerías:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura tu API key:
   ```bash
   $env:ANTHROPIC_API_KEY = "tu-clave-aqui"
   ```
   (Obten la clave en https://console.anthropic.com/api_keys)

5. ¡Ejecuta la app!
   ```bash
   streamlit run app.py
   ```

### Mac / Linux

```bash
# Instala Python si no lo tienes
brew install python3  # Mac

# Clona o descarga este repo
git clone https://github.com/caceved4-cloud/CallerSummary.git
cd CallerSummary

# Instala dependencias
pip3 install -r requirements.txt

# Configura API key
export ANTHROPIC_API_KEY="tu-clave-aqui"

# ¡Ejecuta!
streamlit run app.py
```

## 🎯 Qué Esperar

**Paso 1:** Sube un audio o pega una transcripción
```
📤 Subir Audio
   → Elige un archivo: llamada.mp3 ✓
```

**Paso 2:** Haz clic en "Generar Resumen"
```
⚡ Generando resumen con Claude...
```

**Paso 3:** Obtendrás algo como esto:
```
📋 Resumen de la Llamada

🎯 Puntos Importantes Tratados
- Presupuesto: Discusión sobre inversión Q4
- Timeline: Inicio en octubre, entrega en diciembre
- Responsables: María (gestión), Juan (técnico)

✅ Conclusiones
- Aprobado presupuesto de $50,000
- Proyecto inicia 1 de octubre

🚀 Siguientes Pasos
- Preparar documentación — María — 25 de sept
- Setup de ambiente — Juan — 28 de sept
```

**Paso 4:** Descarga el resumen como archivo .txt

## 📞 Formatos de Audio Soportados

- MP3 ✓
- WAV ✓
- M4A ✓
- OGG ✓
- MP4 ✓

## 🔐 Seguridad

- ✅ El audio se transcribe **localmente** (Whisper)
- ✅ Solo el texto se envía a Claude (encriptado)
- ✅ No se guardan conversaciones en servidores

## 🛠️ Solución de Problemas

### "Error: ModuleNotFoundError"
→ Falta instalar dependencias:
```bash
pip install -r requirements.txt
```

### "Error: ANTHROPIC_API_KEY not set"
→ Falta configurar tu clave API:
```bash
export ANTHROPIC_API_KEY="tu-clave-aqui"  # Mac/Linux
$env:ANTHROPIC_API_KEY = "tu-clave-aqui"  # Windows PowerShell
```

[Obtén tu API key gratis aquí](https://console.anthropic.com/api_keys)

### "Error al transcribir"
→ Descarga Whisper por primera vez (~150MB):
```bash
pip install --upgrade openai-whisper
```

## 📧 ¿Dudas?

1. Revisa que Python esté instalado: `python --version`
2. Verifica la API key en https://console.anthropic.com/
3. Intenta reinstalar: `pip install --upgrade -r requirements.txt`

---

**🤖 Hecho con Claude** | [API de Anthropic](https://www.anthropic.com)
