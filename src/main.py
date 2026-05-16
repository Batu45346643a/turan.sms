"""
Turan SMS - Ana uygulama menüsü (Güncellenmiş)
Deprem iletişim sistemi: To-Do List, SMS, Acil Durum, Lokasyon, Mesh Network
"""

from todo_manager import TodoManager
from sms_handler import SMSHandler, EmergencyNotifier
from location import LocationManager, EmergencySOS
from mesh_network import MeshNetwork, OfflineSync


class TuranApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulamayı başlat"""
        self.todo_manager = TodoManager()
        self.sms_handler = SMSHandler()
        self.emergency_notifier = EmergencyNotifier()
        self.location_manager = LocationManager()
        self.sos = EmergencySOS()
        self.mesh_network = MeshNetwork()
        self.offline_sync = OfflineSync()
    
    def display_menu(self):
        """Ana menüyü göster"""
        print("\n" + "="*50)
        print("🚨 TURAN SMS - Deprem İletişim Sistemi 🚨")
        print("="*50)
        print("\n1. 📋 To-Do List Yönetimi")
        print("2. 📱 SMS Gönderi")
        print("3. 🚨 Acil Durum Bildirimleri")
        print("4. 📍 Lokasyon Yönetimi")
        print("5. 🌐 Mesh Network (Offline İletişim)")
        print("6. ℹ️  Sistem Bilgisi")
        print("7. 🔚 Çıkış")
        print("-"*50)
    
    # ==================== TO-DO LIST MENÜSÜ ====================
    def display_todo_menu(self):
        """To-Do List menüsünü göster"""
        print("\n" + "="*50)
        print("📋 TO-DO LIST YÖNETIMI")
        print("="*50)
        print("\n1. Görev Ekle")
        print("2. Tüm Görevleri Listele")
        print("3. Beklemede Olan Görevleri Listele")
        print("4. Tamamlanmış Görevleri Listele")
        print("5. Görev Tamamla")
        print("6. Görev Sil")
        print("7. Görev Güncelle")
        print("8. İstatistikler")
        print("9. Tamamlanmış Görevleri Temizle")
        print("0. Ana Menüye Dön")
        print("-"*50)
    
    def add_todo(self):
        """Yeni görev ekle"""
        print("\n📝 YENİ GÖREV EKLE")
        title = input("Görev başlığı: ").strip()
        if not title:
            print("❌ Başlık boş olamaz!")
            return
        
        description = input("Görev açıklaması (isteğe bağlı): ").strip()
        
        print("\nÖncelik Seviyesi:")
        print("1. Düşük (low)")
        print("2. Normal (normal) - Varsayılan")
        print("3. Yüksek (high)")
        priority_choice = input("Seçim (1-3): ").strip()
        
        priority_map = {"1": "low", "2": "normal", "3": "high"}
        priority = priority_map.get(priority_choice, "normal")
        
        todo = self.todo_manager.add_todo(title, description, priority)
        if todo:
            print(f"✅ Görev başarıyla eklendi! (ID: {todo['id']})")
        else:
            print("❌ Görev eklenemedi!")
    
    def list_todos(self, todos=None):
        """Görevleri listele"""
        if todos is None:
            todos = self.todo_manager.get_all_todos()
        
        if not todos:
            print("\n📭 Görev yok!")
            return
        
        print("\n" + "-"*70)
        print(f"{'ID':<4} {'Başlık':<25} {'Durumu':<12} {'Öncelik':<10}")
        print("-"*70)
        
        for todo in todos:
            status = "✅ Tamamlandı" if todo["completed"] else "⏳ Beklemede"
            priority_emoji = {"low": "🟢", "normal": "🟡", "high": "🔴"}
            priority_str = f"{priority_emoji.get(todo['priority'], '⚪')} {todo['priority']}"
            
            print(f"{todo['id']:<4} {todo['title']:<25} {status:<12} {priority_str:<10}")
            if todo['description']:
                print(f"     Açıklama: {todo['description']}")
        
        print("-"*70)
    
    def complete_todo(self):
        """Görev tamamla"""
        self.list_todos(self.todo_manager.get_pending_todos())
        
        try:
            todo_id = int(input("\nTamamlanacak görevin ID'si: "))
            if self.todo_manager.complete_todo(todo_id):
                print("✅ Görev tamamlandı!")
            else:
                print("❌ Görev bulunamadı!")
        except ValueError:
            print("❌ Geçersiz ID!")
    
    def delete_todo(self):
        """Görev sil"""
        self.list_todos()
        
        try:
            todo_id = int(input("\nSilinecek görevin ID'si: "))
            if self.todo_manager.delete_todo(todo_id):
                print("✅ Görev silindi!")
            else:
                print("❌ Görev bulunamadı!")
        except ValueError:
            print("❌ Geçersiz ID!")
    
    def update_todo(self):
        """Görev güncelle"""
        self.list_todos()
        
        try:
            todo_id = int(input("\nGüncellenecek görevin ID'si: "))
            todo = self.todo_manager.get_todo(todo_id)
            
            if not todo:
                print("❌ Görev bulunamadı!")
                return
            
            print(f"\nMevcut Başlık: {todo['title']}")
            new_title = input("Yeni başlık (boş bırakarak değiştirmeyin): ").strip()
            
            print(f"Mevcut Açıklama: {todo['description']}")
            new_description = input("Yeni açıklama (boş bırakarak değiştirmeyin): ").strip()
            
            print(f"Mevcut Öncelik: {todo['priority']}")
            new_priority = input("Yeni öncelik (boş bırakarak değiştirmeyin): ").strip()
            
            self.todo_manager.update_todo(
                todo_id,
                title=new_title if new_title else None,
                description=new_description if new_description else None,
                priority=new_priority if new_priority else None
            )
            print("✅ Görev güncellendi!")
        except ValueError:
            print("❌ Geçersiz ID!")
    
    def show_stats(self):
        """İstatistikleri göster"""
        stats = self.todo_manager.get_stats()
        print("\n" + "="*50)
        print("📊 GÖREV İSTATİSTİKLERİ")
        print("="*50)
        print(f"Toplam Görev: {stats['total']}")
        print(f"Tamamlanan: {stats['completed']}")
        print(f"Beklemede: {stats['pending']}")
        print(f"Tamamlama Oranı: {stats['completion_percentage']:.1f}%")
        print("="*50)
    
    def clear_completed(self):
        """Tamamlanmış görevleri temizle"""
        count = self.todo_manager.clear_completed()
        print(f"✅ {count} tamamlanmış görev silindi!")
    
    def handle_todo_menu(self):
        """To-Do List menüsünü yönet"""
        while True:
            self.display_todo_menu()
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.add_todo()
            elif choice == "2":
                self.list_todos()
            elif choice == "3":
                self.list_todos(self.todo_manager.get_pending_todos())
            elif choice == "4":
                self.list_todos(self.todo_manager.get_completed_todos())
            elif choice == "5":
                self.complete_todo()
            elif choice == "6":
                self.delete_todo()
            elif choice == "7":
                self.update_todo()
            elif choice == "8":
                self.show_stats()
            elif choice == "9":
                self.clear_completed()
            elif choice == "0":
                break
            else:
                print("❌ Geçersiz seçim!")
    
    # ==================== SMS MENÜSÜ ====================
    def handle_sms_menu(self):
        """SMS menüsünü yönet"""
        print("\n" + "="*50)
        print("📱 SMS GÖNDER")
        print("="*50)
        
        if not self.sms_handler.is_configured():
            print("\n⚠️  SMS servisi yapılandırılmamış!")
            print("Lütfen .env dosyasında Twilio ayarlarını yapın.")
            print("Şablon için .env.example dosyasına bakın.")
            return
        
        recipient = input("\nAlıcı telefon numarası (+90XXXXXXXXXX): ").strip()
        message = input("Mesaj metni: ").strip()
        
        if not recipient or not message:
            print("❌ Telefon numarası ve mesaj gerekli!")
            return
        
        print("\n📤 SMS gönderiyor...")
        result = self.sms_handler.send_sms(recipient, message)
        
        if result["success"]:
            print(f"✅ SMS başarıyla gönderildi!")
            print(f"Mesaj ID: {result['message_id']}")
            print(f"Durum: {result['status']}")
        else:
            print(f"❌ SMS gönderilemedi: {result['error']}")
    
    # ==================== ACİL DURUM MENÜSÜ ====================
    def handle_emergency_menu(self):
        """Acil durum menüsünü yönet"""
        while True:
            print("\n" + "="*50)
            print("🚨 ACİL DURUM YÖNETİMİ")
            print("="*50)
            print("\n1. Acil Durum Kişisi Ekle")
            print("2. Acil Durum Kişilerini Listele")
            print("3. Acil Durum Uyarısı Gönder")
            print("4. Deprem Uyarısı Gönder")
            print("5. Acil Durum Kişi Sil")
            print("0. Ana Menüye Dön")
            print("-"*50)
            
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.add_emergency_contact()
            elif choice == "2":
                self.list_emergency_contacts()
            elif choice == "3":
                self.send_emergency_alert()
            elif choice == "4":
                self.send_earthquake_alert()
            elif choice == "5":
                self.remove_emergency_contact()
            elif choice == "0":
                break
            else:
                print("❌ Geçersiz seçim!")
    
    def add_emergency_contact(self):
        """Acil durum kişisi ekle"""
        print("\n➕ ACİL DURUM KİŞİSİ EKLE")
        name = input("Kişi adı: ").strip()
        phone = input("Telefon numarası (+90XXXXXXXXXX): ").strip()
        
        if not name or not phone:
            print("❌ Ad ve telefon numarası gerekli!")
            return
        
        contact = self.emergency_notifier.add_emergency_contact(name, phone)
        print(f"✅ {name} acil durum kişilerine eklendi!")
    
    def list_emergency_contacts(self):
        """Acil durum kişilerini listele"""
        contacts = self.emergency_notifier.list_emergency_contacts()
        
        if not contacts:
            print("\n❌ Acil durum kişisi yok!")
            return
        
        print("\n" + "-"*50)
        print(f"{'Ad':<25} {'Telefon':<20}")
        print("-"*50)
        for contact in contacts:
            print(f"{contact['name']:<25} {contact['phone']:<20}")
        print("-"*50)
    
    def send_emergency_alert(self):
        """Acil durum uyarısı gönder"""
        print("\n🚨 ACİL DURUM UYARISI GÖNDER")
        message = input("Uyarı mesajı: ").strip()
        location = input("Lokasyon (isteğe bağlı): ").strip()
        
        if not message:
            print("❌ Mesaj gerekli!")
            return
        
        result = self.emergency_notifier.send_emergency_alert(message, location)
        
        print(f"\n✅ {result['sent_count']} kişiye uyarı gönderildi!")
        if result['failed_count'] > 0:
            print(f"⚠️  {result['failed_count']} kişiye gönderilemedi!")
    
    def send_earthquake_alert(self):
        """Deprem uyarısı gönder"""
        print("\n🌍 DEPREM UYARISI GÖNDER")
        try:
            magnitude = float(input("Deprem şiddeti (Richter): "))
            location = input("Deprem yeri: ").strip()
            depth = input("Derinlik (km): ").strip()
            
            result = self.emergency_notifier.send_earthquake_alert(magnitude, location, depth)
            
            print(f"\n✅ {result['sent_count']} kişiye deprem uyarısı gönderildi!")
        except ValueError:
            print("❌ Geçersiz değer!")
    
    def remove_emergency_contact(self):
        """Acil durum kişi sil"""
        self.list_emergency_contacts()
        phone = input("\nSilinecek kişinin telefon numarası: ").strip()
        
        if self.emergency_notifier.remove_emergency_contact(phone):
            print("✅ Kişi silindi!")
        else:
            print("❌ Kişi bulunamadı!")
    
    # ==================== LOKASYONMenüsü ====================
    def handle_location_menu(self):
        """Lokasyon menüsünü yönet"""
        while True:
            print("\n" + "="*50)
            print("📍 LOKASYON YÖNETİMİ")
            print("="*50)
            print("\n1. Konumunu Kaydet")
            print("2. Konumunu Göster")
            print("3. Yakındaki Kullanıcıları Bul")
            print("4. Tüm Konumları Görüntüle")
            print("5. SOS Tetikle")
            print("6. Aktif SOS Uyarılarını Görüntüle")
            print("0. Ana Menüye Dön")
            print("-"*50)
            
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.save_location()
            elif choice == "2":
                self.show_location()
            elif choice == "3":
                self.find_nearby_users()
            elif choice == "4":
                self.show_all_locations()
            elif choice == "5":
                self.trigger_sos()
            elif choice == "6":
                self.show_active_sos()
            elif choice == "0":
                break
            else:
                print("❌ Geçersiz seçim!")
    
    def save_location(self):
        """Konumu kaydet"""
        print("\n📍 KONUM KAYDET")
        try:
            user_id = input("Kullanıcı ID'si: ").strip()
            latitude = float(input("Enlem: "))
            longitude = float(input("Boylam: "))
            address = input("Adres (isteğe bağlı): ").strip()
            
            location = self.location_manager.add_user_location(user_id, latitude, longitude, address)
            print(f"✅ Konumunuz kaydedildi!")
            print(f"Koordinatlar: {latitude}, {longitude}")
        except ValueError:
            print("❌ Geçersiz koordinatlar!")
    
    def show_location(self):
        """Konumunu göster"""
        user_id = input("\nKullanıcı ID'si: ").strip()
        location = self.location_manager.get_user_location(user_id)
        
        if not location:
            print("❌ Konum bulunamadı!")
            return
        
        print("\n" + "-"*50)
        print(f"Kullanıcı: {location['user_id']}")
        print(f"Koordinatlar: {location['latitude']}, {location['longitude']}")
        print(f"Adres: {location['address']}")
        print(f"Zaman: {location['timestamp']}")
        print("-"*50)
    
    def find_nearby_users(self):
        """Yakındaki kullanıcıları bul"""
        user_id = input("\nKullanıcı ID'si: ").strip()
        try:
            radius = float(input("Arama yarıçapı (km, varsayılan 5): ") or "5")
        except ValueError:
            radius = 5
        
        nearby = self.location_manager.find_nearby_users(user_id, radius)
        
        if not nearby:
            print(f"❌ {radius}km içinde kimse yok!")
            return
        
        print("\n" + "-"*70)
        print(f"{'Kullanıcı':<15} {'Mesafe (km)':<15} {'Adres':<40}")
        print("-"*70)
        for user in nearby:
            print(f"{user['user_id']:<15} {user['distance_km']:<15} {user['address']:<40}")
        print("-"*70)
    
    def show_all_locations(self):
        """Tüm konumları göster"""
        locations = self.location_manager.get_all_locations()
        
        if not locations:
            print("\n❌ Konum yok!")
            return
        
        print("\n" + "-"*70)
        print(f"{'Kullanıcı':<15} {'Enlem':<15} {'Boylam':<15} {'Adres':<25}")
        print("-"*70)
        for user_id, location in locations.items():
            print(f"{user_id:<15} {location['latitude']:<15} {location['longitude']:<15} {location['address']:<25}")
        print("-"*70)
    
    def trigger_sos(self):
        """SOS tetikle"""
        print("\n🚨 SOS TETIKLE")
        user_id = input("Kullanıcı ID'si: ").strip()
        reason = input("SOS sebebi (isteğe bağlı): ").strip() or "Acil Durum"
        
        try:
            radius = float(input("Yakındaki kişi arama yarıçapı (km, varsayılan 5): ") or "5")
        except ValueError:
            radius = 5
        
        result = self.sos.trigger_sos(user_id, reason, radius)
        
        if result["success"]:
            print(f"\n✅ SOS tetiklendi!")
            print(f"SOS ID: {result['sos_id']}")
            print(f"Yakındaki {result['nearby_users_count']} kişiye bildirim gönderildi!")
        else:
            print(f"❌ SOS tetiklenemedi: {result['error']}")
    
    def show_active_sos(self):
        """Aktif SOS uyarılarını göster"""
        alerts = self.sos.get_active_sos_alerts()
        
        if not alerts:
            print("\n✅ Aktif SOS yok!")
            return
        
        print("\n" + "-"*70)
        print(f"{'SOS ID':<10} {'Kullanıcı':<15} {'Sebep':<25} {'Yakındakiler':<10}")
        print("-"*70)
        for alert in alerts:
            print(f"{alert['id']:<10} {alert['user_id']:<15} {alert['reason']:<25} {len(alert['nearby_users']):<10}")
        print("-"*70)
    
    # ==================== MESH NETWORK MENÜSÜ ====================
    def handle_mesh_menu(self):
        """Mesh Network menüsünü yönet"""
        while True:
            print("\n" + "="*50)
            print("🌐 MESH NETWORK (OFFLINE İLETİŞİM)")
            print("="*50)
            print("\n1. Yeni Düğüm Ekle")
            print("2. Düğümleri Bağla")
            print("3. Mesh Mesajı Gönder")
            print("4. Ağ Topolojisini Görüntüle")
            print("5. Çevrimdışı Senkronizasyon Kuyruğu")
            print("0. Ana Menüye Dön")
            print("-"*50)
            
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.add_mesh_node()
            elif choice == "2":
                self.connect_mesh_nodes()
            elif choice == "3":
                self.send_mesh_message()
            elif choice == "4":
                self.show_network_topology()
            elif choice == "5":
                self.show_sync_queue()
            elif choice == "0":
                break
            else:
                print("❌ Geçersiz seçim!")
    
    def add_mesh_node(self):
        """Mesh ağına yeni düğüm ekle"""
        print("\n🌐 YENİ DÜĞÜM EKLE")
        node_id = input("Düğüm ID'si (otomatik oluşturulabilir): ").strip() or f"node_{len(self.mesh_network.network_data)}"
        node_name = input("Düğüm adı: ").strip()
        
        node = self.mesh_network.add_node(node_id, node_name)
        print(f"✅ Düğüm eklendi: {node_id}")
    
    def connect_mesh_nodes(self):
        """İki düğümü bağla"""
        print("\n🔗 DÜĞÜMLERI BAĞLA")
        node1 = input("Birinci düğüm ID'si: ").strip()
        node2 = input("İkinci düğüm ID'si: ").strip()
        
        if self.mesh_network.connect_nodes(node1, node2):
            print(f"✅ {node1} ve {node2} bağlandı!")
        else:
            print("❌ Düğümler bulunamadı!")
    
    def send_mesh_message(self):
        """Mesh mesajı gönder"""
        print("\n📨 MESH MESAJI GÖNDER")
        sender = input("Gönderici düğüm ID'si: ").strip()
        recipient = input("Alıcı düğüm ID'si: ").strip()
        message = input("Mesaj: ").strip()
        msg_type = input("Mesaj türü (text/emergency/location): ").strip() or "text"
        
        msg = self.mesh_network.send_mesh_message(sender, recipient, message, msg_type)
        print(f"✅ Mesaj gönderildi! (ID: {msg['id']})")
    
    def show_network_topology(self):
        """Ağ topolojisini göster"""
        topology = self.mesh_network.get_network_topology()
        
        print("\n" + "="*50)
        print("🌐 AĞ TOPOLOJİSİ")
        print("="*50)
        print(f"Toplam Düğüm: {topology['total_nodes']}")
        print(f"Toplam Mesaj: {topology['total_messages']}")
        print(f"Teslim Edilen Mesajlar: {topology['delivered_messages']}")
        print("="*50)
        
        if topology['nodes']:
            print("\nDüğümler:")
            for node_id, node_info in topology['nodes'].items():
                print(f"  • {node_id} ({node_info['name']})")
                print(f"    Durum: {'🟢 Online' if node_info['is_online'] else '🔴 Offline'}")
                print(f"    Komşular: {', '.join(node_info['neighbors']) or 'Yok'}")
    
    def show_sync_queue(self):
        """Senkronizasyon kuyruğunu göster"""
        pending = self.offline_sync.get_pending_syncs()
        
        if not pending:
            print("\n✅ Senkronizasyon kuyruğu boş!")
            return
        
        print("\n" + "-"*70)
        print(f"{'ID':<10} {'Tür':<15} {'Öncelik':<10} {'Zaman':<20}")
        print("-"*70)
        for item in pending:
            print(f"{item['id']:<10} {item['type']:<15} {item['priority']:<10} {item['queued_at']:<20}")
        print("-"*70)
    
    # ==================== SİSTEM BİLGİSİ ====================
    def show_system_info(self):
        """Sistem bilgisini göster"""
        print("\n" + "="*50)
        print("ℹ️  SİSTEM BİLGİSİ")
        print("="*50)
        
        # To-Do List
        todo_stats = self.todo_manager.get_stats()
        print("\n📋 TO-DO LIST:")
        print(f"  • Toplam: {todo_stats['total']}")
        print(f"  • Tamamlanan: {todo_stats['completed']}")
        print(f"  • Beklemede: {todo_stats['pending']}")
        
        # SMS
        print("\n📱 SMS:")
        sms_status = "✅ Yapılandırılmış" if self.sms_handler.is_configured() else "❌ Yapılandırılmamış"
        print(f"  • Durum: {sms_status}")
        
        # Acil Durum
        contacts = self.emergency_notifier.list_emergency_contacts()
        print(f"\n🚨 ACİL DURUM:")
        print(f"  • Kişiler: {len(contacts)}")
        
        # Lokasyon
        locations = self.location_manager.get_all_locations()
        print(f"\n📍 LOKASYON:")
        print(f"  • Kaydedilen konumlar: {len(locations)}")
        
        # Mesh Network
        topology = self.mesh_network.get_network_topology()
        print(f"\n🌐 MESH NETWORK:")
        print(f"  • Düğümler: {topology['total_nodes']}")
        print(f"  • Mesajlar: {topology['total_messages']}")
        
        print("\n" + "="*50)
    
    # ==================== MAIN LOOP ====================
    def run(self):
        """Uygulamayı çalıştır"""
        while True:
            self.display_menu()
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.handle_todo_menu()
            elif choice == "2":
                self.handle_sms_menu()
            elif choice == "3":
                self.handle_emergency_menu()
            elif choice == "4":
                self.handle_location_menu()
            elif choice == "5":
                self.handle_mesh_menu()
            elif choice == "6":
                self.show_system_info()
            elif choice == "7":
                print("\n👋 Çıkış yapılıyor... İyi günler!")
                break
            else:
                print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    app = TuranApp()
    app.run()
