from flask import current_app

import easypost as easypost_api

easypost_api.api_key = current_app.config['EASY_POST_API_KEY']
