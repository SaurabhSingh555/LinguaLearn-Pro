from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import time
import os
from gtts import gTTS
import base64

app = Flask(__name__)

# Dictionary to store country flag icons and language codes for TTS
flags = {
    "English": {"flag": "flags/uk.png", "code": "en"},
    "Hindi": {"flag": "flags/india.png", "code": "hi"},
    "French": {"flag": "flags/france.png", "code": "fr"},
    "Spanish": {"flag": "flags/spain.png", "code": "es"},
    "German": {"flag": "flags/germany.png", "code": "de"},
    "Chinese": {"flag": "flags/china.png", "code": "zh-CN"},
    "Japanese": {"flag": "flags/japan.png", "code": "ja"},
    "Russian": {"flag": "flags/russia.png", "code": "ru"},
}

@app.route('/')
def index():
    return render_template('index.html', flags=flags)

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    source_lang = data['source_lang']
    target_lang = data['target_lang']
    text = data['text']

    try:
        # Translation
        translator = GoogleTranslator(source=flags[source_lang]['code'], 
                                    target=flags[target_lang]['code'])
        translated_text = translator.translate(text)
        
        # Generate audio for translated text
        tts = gTTS(translated_text, lang=flags[target_lang]['code'])
        audio_path = f"static/audio/{time.time()}.mp3"
        tts.save(audio_path)
        
        with open(audio_path, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Clean up audio file
        os.remove(audio_path)
        
        time.sleep(1)  # Simulating processing time
        return jsonify({
            'translated_text': translated_text,
            'audio': audio_data
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    if not os.path.exists('static/audio'):
        os.makedirs('static/audio')
    
    # Render-compatible configuration
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False for production