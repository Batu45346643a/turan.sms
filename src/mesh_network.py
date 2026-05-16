"""
Mesh Network Modülü - Offline İletişim
Cihazlar arası doğrudan iletişim
"""

import json
from pathlib import Path
from datetime import datetime
import uuid


class MeshNode:
    """Mesh ağında bir düğüm (cihaz)"""
    
    def __init__(self, node_id=None, name=""):
        """
        MeshNode'u başlat
        
        Args:
            node_id (str): Düğüm kimliği (otomatik oluşturulur)
            name (str): Düğüm adı
        """
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.name = name
        self.is_online = True
        self.last_heartbeat = datetime.now().isoformat()
        self.neighbors = []  # Komşu düğümler
        self.incoming_messages = []
        self.outgoing_messages = []
    
    def to_dict(self):
        """Düğümü sözlüğe çevir"""
        return {
            "node_id": self.node_id,
            "name": self.name,
            "is_online": self.is_online,
            "last_heartbeat": self.last_heartbeat,
            "neighbors": self.neighbors
        }


class MeshNetwork:
    """Mesh ağı yönetimi"""
    
    def __init__(self, data_dir="data"):
        """MeshNetwork'ü başlat"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.mesh_file = self.data_dir / "mesh_network.json"
        self.messages_file = self.data_dir / "mesh_messages.json"
        
        self.nodes = {}  # Ağdaki tüm düğümler
        self.network_data = self._load_network()
        self.messages = self._load_messages()
    
    def _load_network(self):
        """Ağ verilerini yükle"""
        if self.mesh_file.exists():
            try:
                with open(self.mesh_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _load_messages(self):
        """Mesh mesajlarını yükle"""
        if self.messages_file.exists():
            try:
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_network(self):
        """Ağ verilerini kaydet"""
        try:
            with open(self.mesh_file, 'w', encoding='utf-8') as f:
                json.dump(self.network_data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def _save_messages(self):
        """Mesh mesajlarını kaydet"""
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def add_node(self, node_id, name=""):
        """
        Ağa yeni düğüm ekle
        
        Args:
            node_id (str): Düğüm kimliği
            name (str): Düğüm adı
        
        Returns:
            dict: Eklenen düğüm
        """
        node = {
            "node_id": node_id,
            "name": name,
            "is_online": True,
            "joined_at": datetime.now().isoformat(),
            "neighbors": []
        }
        
        self.network_data[node_id] = node
        self._save_network()
        return node
    
    def connect_nodes(self, node_id_1, node_id_2):
        """
        İki düğümü birbirine bağla
        
        Args:
            node_id_1 (str): İlk düğüm ID'si
            node_id_2 (str): İkinci düğüm ID'si
        
        Returns:
            bool: Başarılı mı
        """
        if node_id_1 not in self.network_data or node_id_2 not in self.network_data:
            return False
        
        # İkişer yönlü bağlantı yap
        if node_id_2 not in self.network_data[node_id_1]["neighbors"]:
            self.network_data[node_id_1]["neighbors"].append(node_id_2)
        
        if node_id_1 not in self.network_data[node_id_2]["neighbors"]:
            self.network_data[node_id_2]["neighbors"].append(node_id_1)
        
        self._save_network()
        return True
    
    def disconnect_nodes(self, node_id_1, node_id_2):
        """İki düğümün bağlantısını kes"""
        if node_id_1 not in self.network_data or node_id_2 not in self.network_data:
            return False
        
        self.network_data[node_id_1]["neighbors"].remove(node_id_2)
        self.network_data[node_id_2]["neighbors"].remove(node_id_1)
        
        self._save_network()
        return True
    
    def send_mesh_message(self, sender_id, recipient_id, message, message_type="text"):
        """
        Mesh ağında mesaj gönder
        
        Args:
            sender_id (str): Gönderici düğüm ID'si
            recipient_id (str): Alıcı düğüm ID'si
            message (str): Mesaj metni
            message_type (str): Mesaj türü (text, emergency, location, vb.)
        
        Returns:
            dict: Gönderilen mesaj
        """
        mesh_message = {
            "id": str(uuid.uuid4())[:8],
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message": message,
            "type": message_type,
            "sent_at": datetime.now().isoformat(),
            "delivered": False,
            "hops": 0,
            "route": [sender_id]
        }
        
        self.messages.append(mesh_message)
        self._save_messages()
        
        return mesh_message
    
    def route_message(self, message_id, current_node_id):
        """
        Mesajı ağda yönlendir (routing)
        
        Args:
            message_id (str): Mesaj ID'si
            current_node_id (str): Şu anki düğüm
        
        Returns:
            dict: Yönlendirme sonucu
        """
        message = None
        for msg in self.messages:
            if msg["id"] == message_id:
                message = msg
                break
        
        if not message:
            return {"success": False, "error": "Mesaj bulunamadı"}
        
        # Hedef bulundu mu?
        if message["recipient_id"] == current_node_id:
            message["delivered"] = True
            message["delivered_at"] = datetime.now().isoformat()
            self._save_messages()
            return {
                "success": True,
                "delivered": True,
                "message": "Mesaj hedefe ulaştı"
            }
        
        # Komşulara ilet
        current_node = self.network_data.get(current_node_id)
        if not current_node:
            return {"success": False, "error": "Düğüm bulunamadı"}
        
        # Mesajın zaten gittiği yolu kontrol et (döngüyü önle)
        if current_node_id in message["route"]:
            return {"success": False, "error": "Mesaj döngüsü"}
        
        message["route"].append(current_node_id)
        message["hops"] += 1
        self._save_messages()
        
        return {
            "success": True,
            "delivered": False,
            "next_nodes": current_node["neighbors"],
            "hops": message["hops"]
        }
    
    def get_network_topology(self):
        """Ağ topolojisini getir"""
        return {
            "total_nodes": len(self.network_data),
            "nodes": self.network_data,
            "total_messages": len(self.messages),
            "delivered_messages": len([m for m in self.messages if m["delivered"]])
        }
    
    def get_node_info(self, node_id):
        """Düğüm bilgisini getir"""
        return self.network_data.get(node_id)
    
    def set_node_status(self, node_id, is_online):
        """Düğümün durumunu ayarla (online/offline)"""
        if node_id in self.network_data:
            self.network_data[node_id]["is_online"] = is_online
            self.network_data[node_id]["last_heartbeat"] = datetime.now().isoformat()
            self._save_network()
            return True
        return False


class OfflineSync:
    """Çevrimdışı senkronizasyon"""
    
    def __init__(self, data_dir="data"):
        """OfflineSync'i başlat"""
        self.mesh_network = MeshNetwork(data_dir)
        self.data_dir = Path(data_dir)
        self.sync_queue_file = self.data_dir / "sync_queue.json"
        self.sync_queue = self._load_sync_queue()
    
    def _load_sync_queue(self):
        """Senkronizasyon kuyruğunu yükle"""
        if self.sync_queue_file.exists():
            try:
                with open(self.sync_queue_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_sync_queue(self):
        """Senkronizasyon kuyruğunu kaydet"""
        try:
            with open(self.sync_queue_file, 'w', encoding='utf-8') as f:
                json.dump(self.sync_queue, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def queue_for_sync(self, data_type, data, priority="normal"):
        """
        Veriyi senkronizasyon kuyruğuna ekle
        
        Args:
            data_type (str): Veri türü (todo, location, message, vb.)
            data (dict): Senkronize edilecek veri
            priority (str): Öncelik (low, normal, high)
        
        Returns:
            dict: Kuyruğa eklenen öğe
        """
        queue_item = {
            "id": str(uuid.uuid4())[:8],
            "type": data_type,
            "data": data,
            "priority": priority,
            "queued_at": datetime.now().isoformat(),
            "synced": False
        }
        
        self.sync_queue.append(queue_item)
        self._save_sync_queue()
        return queue_item
    
    def get_pending_syncs(self):
        """Beklemede olan senkronizasyonları getir"""
        return [item for item in self.sync_queue if not item["synced"]]
    
    def mark_synced(self, queue_item_id):
        """Öğeyi senkronize edildi olarak işaretle"""
        for item in self.sync_queue:
            if item["id"] == queue_item_id:
                item["synced"] = True
                item["synced_at"] = datetime.now().isoformat()
                self._save_sync_queue()
                return True
        return False
