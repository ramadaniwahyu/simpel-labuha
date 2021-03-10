class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = True
	TESTING = False
	TEMPLATES_AUTO_RELOAD = True
	
	"""
	Database Connection
	"""
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user_db:Q1w2e3r4!!@192.168.20.1/simpel'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "AFSBAKFBAKBFAK09876543TNJQN!$@y(!$yGABV"
	CSRF_ENABLED = True
	
	UPLOAD_FOLDER = "uploads"
	ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

	# Flask-Dropzone config
	DROPZONE_SERVE_LOCAL=True
	DROPZONE_DEFAULT_MESSAGE = "Seret file kesini atau Klik disini untuk Upload File"
	DROPZONE_ALLOWED_FILE_CUSTOM=True
	DROPZONE_ALLOWED_FILE_TYPE='image/*, .jpeg, .jpg, .png, .pdf, .txt',
	DROPZONE_MAX_FILE_SIZE=5
	DROPZONE_MAX_FILES=60
	
	#Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
	#RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
	#RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
