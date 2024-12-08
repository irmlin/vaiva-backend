import os

STATIC_DIR = 'static/'
DOCUMENTS_DIR = os.path.join(STATIC_DIR, 'documents')
AUDIO_FOR_AVATAR_DIR = os.path.join(STATIC_DIR, 'audio_for_avatar')
AUDIO_FOR_VOICE_DIR = os.path.join(STATIC_DIR, 'audio_for_voice')
VIDEO_DIR = os.path.join(STATIC_DIR, 'video')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
ALLOWED_DOCUMENTS_EXTENSIONS = ['.doc', '.docx', '.txt', '.xls', '.xlsx', '.csv', '.tsv', 'ppt', 'pptx', '.pdf', '.json', '.md', '.html', '.log']
ALLOWED_AUDIO_EXTENSIONS = ['.wav', '.mp3']
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.png', '.jpeg']
ALLOWED_VIDEO_EXTENSIONS = ['.mp4']
AVATAR_SERVICE_URL = 'http://localhost:8003/generate-video'
SEND_MESSAGE_SERVICE_URL = 'http://localhost:8006/send-message'
EXTRACT_FEATURES_SERVICE_URL = 'http://localhost:8006/extract-features'
SPEECH_TO_TEXT_SERVICE_URL = 'http://localhost:8007/transcribe'
TEXT_TO_SPEECH_SERVICE_URL = 'http://localhost:8002/clone-voice'
