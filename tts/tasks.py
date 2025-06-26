from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from openai import OpenAI
from .models import TTSConversion


client = OpenAI(api_key=settings.OPENAI_API_KEY)


@shared_task
def process_tts_conversion(conversion_id):
    try:
        conversion = TTSConversion.objects.get(id=conversion_id)
        conversion.status = 'processing'
        conversion.save()
        response = client.audio.speech.create(
            model="tts-1",
            voice=conversion.voice,
            input=conversion.text,
            speed=conversion.speed
        )
        audio_content = response.content
        file_name = f"tts_{conversion.id}.mp3"

        conversion.audio_file.save(
            file_name,
            ContentFile(audio_content),
            save=False
        )

        conversion.file_size = len(audio_content)
        conversion.status = 'completed'
        conversion.save()

    except TTSConversion.DoesNotExist:
        print(f"TTS Conversion {conversion_id} not found")
    except Exception as e:
        try:
            conversion = TTSConversion.objects.get(id=conversion_id)
            conversion.status = 'failed'
            conversion.error = str(e)
            conversion.save()
        except TTSConversion.DoesNotExist:
            print(f"TTS Conversion {conversion_id} not found during error handling")
