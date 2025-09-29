from flask import Blueprint

#Log Analiz ve Raprolama modülü Blueprint'ini tanımlıyoruz.

log_bp = Blueprint('logs', __name__, template_folder = 'templates')

#Rota tanımlarını içe aktar

from . import views