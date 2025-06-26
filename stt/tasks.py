import os
import tempfile
from celery import shared_task
from django.conf import settings
from openai import OpenAI
from .models import STTConversion


client = OpenAI(api_key=settings.OPENAI_API_KEY)


@shared_task
def process_stt_conversion(conversion_id):
    try:
        conversion = STTConversion.objects.get(id=conversion_id)
        conversion.status = 'processing'
        conversion.save()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            conversion.audio_file.seek(0)
            temp_file.write(conversion.audio_file.read())
            temp_file.flush()

            with open(temp_file.name, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=conversion.language if conversion.language != 'en' else None
                )

            conversion.text = transcript.text
            conversion.status = 'completed'
            conversion.save()
            os.unlink(temp_file.name)

    except STTConversion.DoesNotExist:
        print(f"STT Conversion {conversion_id} not found")
    except Exception as e:
        try:
            conversion = STTConversion.objects.get(id=conversion_id)
            conversion.status = 'failed'
            conversion.error = str(e)
            conversion.save()
        except STTConversion.DoesNotExist:
            print(f"STT Conversion {conversion_id} not found during error handling")

        if 'temp_file' in locals():
            try:
                os.unlink(temp_file.name)
            except:
                pass
