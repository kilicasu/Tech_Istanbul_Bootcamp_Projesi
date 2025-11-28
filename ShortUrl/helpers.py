import random
import string
# models.py’daki URL modelini import edeceksin.
from models import URL

def generate_short_code(len = 6):
    
    chars = string.ascii_letters + string.digits#rastgele seçilebilecek karakterler listesi
    while True:
        code =''.join(random.choices(chars, k = len)) # rastgele kısa URL kodu
        if not  URL.query.filter_by(short_url = code).first(): 
            return code




