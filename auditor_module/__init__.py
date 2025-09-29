from flask import Blueprint

#Blueprint'i tanımlıyoruz.
auditor_bp = Blueprint('auditor', __name__)

#Rotanın doğru çalışması için views dosyasını burada import ediyoruz.
from . import views