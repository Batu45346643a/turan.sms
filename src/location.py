"""
Lokasyon Yönetimi Modülü
"""

import json
from pathlib import Path
from datetime import datetime


class LocationManager:
    """Kullanıcı lokasyonlarını yönet"""
    
    def __init__(self, data_dir="data"):
        """LocationManager'ı başlat"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.locations_file = self.data_dir / "locations.json"
        self.locations = self._load_locations()
    
    def _load_locations(self):
        """Dosyadan lokasyonları yükle"""
        if self.locations_file.exists():
            try:
                with open(self.locations_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_locations(self):
        """Lokasyonları dosyaya kaydet"""
        try:
            with open(self.locations_file, 'w', encoding='utf-8') as f:
                json.dump(self.locations, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def add_user_location(self, user_id, latitude, longitude, address=""):
        """
        Kullanıcı konumunu kaydet
        
        Args:
            user_id (str): Kullanıcı ID'si
            latitude (float): Enlem
            longitude (float): Boylam
            address (str): Adres (isteğe bağlı)
        
        Returns:
            dict: Kaydedilen lokasyon
        """
        location = {
            "user_id": user_id,
            "latitude": float(latitude),
            "longitude": float(longitude),
            "address": address,
            "timestamp": datetime.now().isoformat(),
            "accurate": True
        }
        
        self.locations[user_id] = location
        self._save_locations()
        return location
    
    def get_user_location(self, user_id):
        """
        Kullanıcının konumunu getir
        
        Args:
            user_id (str): Kullanıcı ID'si
        
        Returns:
            dict: Lokasyon bilgisi
        """
        return self.locations.get(user_id)
    
    def get_all_locations(self):
        """Tüm konumları getir"""
        return self.locations
    
    def delete_location(self, user_id):
        """
        Konumu sil
        
        Args:
            user_id (str): Kullanıcı ID'si
        
        Returns:
            bool: Başarılı mı
        """
        if user_id in self.locations:
            del self.locations[user_id]
            self._save_locations()
            return True
        return False
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        """
        İki nokta arasındaki mesafeyi hesapla (Haversine formülü)
        
        Args:
            lat1, lon1: Birinci noktanın koordinatları
            lat2, lon2: İkinci noktanın koordinatları
        
        Returns:
            float: Mesafe (kilometre)
        """
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371  # Dünya yarıçapı (km)
        
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        distance = R * c
        
        return round(distance, 2)
    
    def find_nearby_users(self, user_id, radius_km=5):
        """
        Yakındaki kullanıcıları bul
        
        Args:
            user_id (str): Referans kullanıcı ID'si
            radius_km (float): Arama yarıçapı (km)
        
        Returns:
            list: Yakındaki kullanıcılar
        """
        user_location = self.get_user_location(user_id)
        if not user_location:
            return []
        
        nearby = []
        user_lat = user_location["latitude"]
        user_lon = user_location["longitude"]
        
        for other_id, other_location in self.locations.items():
            if other_id == user_id:
                continue
            
            distance = self.calculate_distance(
                user_lat, user_lon,
                other_location["latitude"],
                other_location["longitude"]
            )
            
            if distance <= radius_km:
                nearby.append({
                    "user_id": other_id,
                    "distance_km": distance,
                    "address": other_location["address"],
                    "timestamp": other_location["timestamp"]
                })
        
        return sorted(nearby, key=lambda x: x["distance_km"])
    
    def share_location_with_contacts(self, user_id, contact_ids, message=""):
        """
        Konumu kişilerle paylaş
        
        Args:
            user_id (str): Kullanıcı ID'si
            contact_ids (list): Kişi ID'leri
            message (str): İsteğe bağlı mesaj
        
        Returns:
            dict: Paylaşım sonucu
        """
        location = self.get_user_location(user_id)
        if not location:
            return {
                "success": False,
                "error": "Konum bilgisi bulunamadı"
            }
        
        # Paylaşılan konumları kaydet
        shared_data = {
            "shared_by": user_id,
            "shared_with": contact_ids,
            "location": location,
            "message": message,
            "shared_at": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "shared_data": shared_data,
            "recipients_count": len(contact_ids)
        }


class EmergencySOS:
    """Acil durum SOS sistemi"""
    
    def __init__(self, data_dir="data"):
        """EmergencySOS'u başlat"""
        self.location_manager = LocationManager(data_dir)
        self.data_dir = Path(data_dir)
        self.sos_file = self.data_dir / "sos_alerts.json"
        self.sos_alerts = self._load_alerts()
    
    def _load_alerts(self):
        """SOS uyarılarını yükle"""
        if self.sos_file.exists():
            try:
                with open(self.sos_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_alerts(self):
        """SOS uyarılarını kaydet"""
        try:
            with open(self.sos_file, 'w', encoding='utf-8') as f:
                json.dump(self.sos_alerts, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def trigger_sos(self, user_id, reason="Acil Durum", nearby_radius=5):
        """
        SOS tetikle
        
        Args:
            user_id (str): Kullanıcı ID'si
            reason (str): SOS sebebi
            nearby_radius (float): Yakındaki kişi arama yarıçapı (km)
        
        Returns:
            dict: SOS sonucu
        """
        user_location = self.location_manager.get_user_location(user_id)
        if not user_location:
            return {
                "success": False,
                "error": "Konum bilgisi bulunamadı. Önce konumunuzu kaydedin."
            }
        
        # Yakındaki kullanıcıları bul
        nearby_users = self.location_manager.find_nearby_users(user_id, nearby_radius)
        
        sos_alert = {
            "id": len(self.sos_alerts) + 1,
            "user_id": user_id,
            "reason": reason,
            "location": user_location,
            "nearby_users": nearby_users,
            "triggered_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.sos_alerts.append(sos_alert)
        self._save_alerts()
        
        return {
            "success": True,
            "sos_id": sos_alert["id"],
            "alert": sos_alert,
            "nearby_users_count": len(nearby_users)
        }
    
    def get_sos_alert(self, sos_id):
        """SOS uyarısını getir"""
        for alert in self.sos_alerts:
            if alert["id"] == sos_id:
                return alert
        return None
    
    def cancel_sos(self, sos_id):
        """SOS uyarısını iptal et"""
        for alert in self.sos_alerts:
            if alert["id"] == sos_id:
                alert["status"] = "cancelled"
                alert["cancelled_at"] = datetime.now().isoformat()
                self._save_alerts()
                return True
        return False
    
    def get_active_sos_alerts(self):
        """Aktif SOS uyarılarını getir"""
        return [alert for alert in self.sos_alerts if alert["status"] == "active"]
