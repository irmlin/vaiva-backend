import os

STATIC_DIR = 'static/'
DOCUMENTS_DIR = os.path.join(STATIC_DIR, 'documents')
AUDIO_DIR = os.path.join(STATIC_DIR, 'audio')
VIDEO_DIR = os.path.join(STATIC_DIR, 'video')
IMAGES_DIR = os.path.join(STATIC_DIR, 'images')
AVATAR_SERVICE_URL = 'http://video-avatar-microservice:8002/generate-video'
SEND_MESSAGE_SERVICE_URL = 'http://chatbot-microservice:8006/send-message'