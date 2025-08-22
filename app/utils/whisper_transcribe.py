import ssl
import whisper



def transcribe_audio(filepath: str, language: str = None, task: str = "transcribe"):
    ssl._create_default_https_context = ssl._create_unverified_context

    model = whisper.load_model("small")
    # Options
    options = {"task": task}
    if language:
        options["language"] = language   # e.g. "hi" for Hindi, "ta" for Tamil
    
    result = model.transcribe(filepath, **options)
    return result["text"]
