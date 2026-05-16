"""
SMS Gönderme Modülü - Twilio API ile
"""

import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()


class SMSHandler:
    """SMS gönderme ve alma işlemleri"""
    
    def __init__(self):
        """SMSHandler'ı başlat"""
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.from_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        
        # Twilio client kontrolü
        try:
            from twilio.rest import Client
            self.client = Client(self.account_sid, self.auth_token) if self.account_sid else None
        except ImportError:
            self.client = None
            print("⚠️  Twilio kütüphanesi yüklü değil. SMS özellikleri sınırlı olacak.")
    
    def is_configured(self):
        """SMS servisi yapılandırılmış mı?"""
        return bool(self.account_sid and self.auth_token and self.from_number and self.client)
    
    def send_sms(self, to_number, message):
        """
        SMS gönder
        
        Args:
            to_number (str): Alıcı telefon numarası (+90 formatında)
            message (str): Gönderilecek mesaj
        
        Returns:
            dict: Gönderme sonucu
        """
        if not self.is_configured():
            return {
                "success": False,
                "error": "SMS servisi yapılandırılmamış. .env dosyasını kontrol edin.",
                "message_id": None
            }
        
        try:
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            return {
                "success": True,
                "message_id": message_obj.sid,
                "status": message_obj.status,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message_id": None
            }
    
    def send_bulk_sms(self, recipients, message):
        """
        Toplu SMS gönder
        
        Args:
            recipients (list): Alıcı numaraları listesi
            message (str): Gönderilecek mesaj
        
        Returns:
            dict: Gönderme özeti
        """
        results = {
            "total": len(recipients),
            "sent": 0,
            "failed": 0,
            "details": []
        }
        
        for recipient in recipients:
            result = self.send_sms(recipient, message)
            if result["success"]:
                results["sent"] += 1
            else:
                results["failed"] += 1
            
            results["details"].append({
                "recipient": recipient,
                "success": result["success"],
                "message_id": result["message_id"],
                "error": result["error"]
            })
        
        return results
    
    def get_sms_status(self, message_id):
        """
        SMS durumunu kontrol et
        
        Args:
            message_id (str): Mesaj ID'si
        
        Returns:
            str: Mesaj durumu
        """
        if not self.is_configured():
            return "Yapılandırılmamış"
        
        try:
            message = self.client.messages(message_id).fetch()
            return message.status
        except Exception as e:
            return f"Hata: {e}"


class EmergencyNotifier:
    """Acil durum bildirimleri"""
    
    def __init__(self):
        """EmergencyNotifier'ı başlat"""
        self.sms_handler = SMSHandler()
        self.emergency_contacts = []
    
    def add_emergency_contact(self, name, phone_number):
        """
        Acil durum kişisi ekle
        
        Args:
            name (str): Kişi adı
            phone_number (str): Telefon numarası
        """
        contact = {
            "name": name,
            "phone": phone_number
        }
        self.emergency_contacts.append(contact)
        return contact
    
    def send_emergency_alert(self, message, location=None):
        """
        Acil durum uyarısı gönder
        
        Args:
            message (str): Uyarı mesajı
            location (str): Lokasyon bilgisi (isteğe bağlı)
        
        Returns:
            dict: Gönderme sonucu
        """
        if not self.emergency_contacts:
            return {
                "success": False,
                "error": "Acil durum kişileri tanımlanmamış",
                "sent_count": 0
            }
        
        # Lokasyon bilgisini ekle
        full_message = f"🚨 ACİL DURUM: {message}"
        if location:
            full_message += f"\n📍 Lokasyon: {location}"
        
        # Tüm acil durum kişilerine SMS gönder
        recipients = [contact["phone"] for contact in self.emergency_contacts]
        results = self.sms_handler.send_bulk_sms(recipients, full_message)
        
        return {
            "success": results["failed"] == 0,
            "sent_count": results["sent"],
            "failed_count": results["failed"],
            "details": results["details"]
        }
    
    def send_earthquake_alert(self, magnitude, location, depth):
        """
        Deprem uyarısı gönder
        
        Args:
            magnitude (float): Deprem şiddeti (Richter)
            location (str): Deprem yeri
            depth (str): Derinlik (km)
        
        Returns:
            dict: Gönderme sonucu
        """
        message = f"DEPREM UYARISI!\nŞiddet: {magnitude} Richter\nYer: {location}\nDerinlik: {depth}"
        return self.send_emergency_alert(message, location)
    
    def list_emergency_contacts(self):
        """Acil durum kişilerini listele"""
        return self.emergency_contacts
    
    def remove_emergency_contact(self, phone_number):
        """
        Acil durum kişisi sil
        
        Args:
            phone_number (str): Telefon numarası
        
        Returns:
            bool: Başarılı mı
        """
        for i, contact in enumerate(self.emergency_contacts):
            if contact["phone"] == phone_number:
                self.emergency_contacts.pop(i)
                return True
        return False
