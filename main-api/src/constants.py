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
AVATAR_SERVICE_URL = 'http://video-avatar-microservice:8002/generate-video'
SEND_MESSAGE_SERVICE_URL = 'http://chatbot-microservice:8006/send-message'