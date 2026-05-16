"""
Turan SMS - Ana uygulama menüsü
Deprem iletişim sistemi ve To-Do List yönetimi
"""

from todo_manager import TodoManager


class TuranApp:
    """Ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulamayı başlat"""
        self.todo_manager = TodoManager()
    
    def display_menu(self):
        """Ana menüyü göster"""
        print("\n" + "="*50)
        print("🚨 TURAN SMS - Deprem İletişim Sistemi 🚨")
        print("="*50)
        print("\n1. To-Do List Yönetimi")
        print("2. SMS Gönderi")
        print("3. Acil Durum Bildirimi")
        print("4. Lokasyon Paylaş")
        print("5. Çıkış")
        print("-"*50)
    
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
    
    def run(self):
        """Uygulamayı çalıştır"""
        while True:
            self.display_menu()
            choice = input("Seçiminiz: ").strip()
            
            if choice == "1":
                self.handle_todo_menu()
            elif choice == "2":
                print("\n📱 SMS gönderme özelliği yakında gelecek!")
            elif choice == "3":
                print("\n🚨 Acil durum bildirimi özelliği yakında gelecek!")
            elif choice == "4":
                print("\n📍 Lokasyon paylaşma özelliği yakında gelecek!")
            elif choice == "5":
                print("\n👋 Çıkış yapılıyor... İyi günler!")
                break
            else:
                print("❌ Geçersiz seçim!")


if __name__ == "__main__":
    app = TuranApp()
    app.run()
