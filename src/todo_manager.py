"""
To-Do List Manager - Lokal depolama ile görev yönetimi
"""

import json
import os
from datetime import datetime
from pathlib import Path


class TodoManager:
    """Görevleri yönetmek için sınıf"""
    
    def __init__(self, data_dir="data"):
        """
        TodoManager'ı başlat
        
        Args:
            data_dir (str): Veri dosyalarının saklanacağı dizin
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.todos_file = self.data_dir / "todos.json"
        self.todos = self._load_todos()
    
    def _load_todos(self):
        """Dosyadan görevleri yükle"""
        if self.todos_file.exists():
            try:
                with open(self.todos_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_todos(self):
        """Görevleri dosyaya kaydet"""
        try:
            with open(self.todos_file, 'w', encoding='utf-8') as f:
                json.dump(self.todos, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Hata: Görevler kaydedilemedi - {e}")
            return False
    
    def add_todo(self, title, description="", priority="normal"):
        """
        Yeni bir görev ekle
        
        Args:
            title (str): Görev başlığı
            description (str): Görev açıklaması
            priority (str): Öncelik seviyesi (low, normal, high)
        
        Returns:
            dict: Oluşturulan görev
        """
        if not title.strip():
            return None
        
        todo = {
            "id": len(self.todos) + 1,
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority.lower(),
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "completed_at": None
        }
        
        self.todos.append(todo)
        self._save_todos()
        return todo
    
    def get_all_todos(self):
        """Tüm görevleri getir"""
        return self.todos
    
    def get_todo(self, todo_id):
        """
        Belirli bir görev getir
        
        Args:
            todo_id (int): Görev ID'si
        
        Returns:
            dict: Görev
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                return todo
        return None
    
    def update_todo(self, todo_id, title=None, description=None, priority=None):
        """
        Görev güncelle
        
        Args:
            todo_id (int): Görev ID'si
            title (str): Yeni başlık
            description (str): Yeni açıklama
            priority (str): Yeni öncelik
        
        Returns:
            dict: Güncellenmiş görev
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                if title is not None:
                    todo["title"] = title.strip()
                if description is not None:
                    todo["description"] = description.strip()
                if priority is not None:
                    todo["priority"] = priority.lower()
                
                self._save_todos()
                return todo
        return None
    
    def complete_todo(self, todo_id):
        """
        Görev tamamla
        
        Args:
            todo_id (int): Görev ID'si
        
        Returns:
            dict: Tamamlanan görev
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                todo["completed_at"] = datetime.now().isoformat()
                self._save_todos()
                return todo
        return None
    
    def uncomplete_todo(self, todo_id):
        """
        Görev tamamlanmış olarak işaretini kaldır
        
        Args:
            todo_id (int): Görev ID'si
        
        Returns:
            dict: Güncellenen görev
        """
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = False
                todo["completed_at"] = None
                self._save_todos()
                return todo
        return None
    
    def delete_todo(self, todo_id):
        """
        Görev sil
        
        Args:
            todo_id (int): Görev ID'si
        
        Returns:
            bool: Başarılı mı
        """
        for i, todo in enumerate(self.todos):
            if todo["id"] == todo_id:
                self.todos.pop(i)
                self._save_todos()
                return True
        return False
    
    def get_pending_todos(self):
        """Tamamlanmamış görevleri getir"""
        return [t for t in self.todos if not t["completed"]]
    
    def get_completed_todos(self):
        """Tamamlanmış görevleri getir"""
        return [t for t in self.todos if t["completed"]]
    
    def get_todos_by_priority(self, priority):
        """
        Belirli önceliklerin görevlerini getir
        
        Args:
            priority (str): Öncelik seviyesi
        
        Returns:
            list: Görevler
        """
        return [t for t in self.todos if t["priority"] == priority.lower()]
    
    def clear_completed(self):
        """Tamamlanmış görevleri temizle"""
        original_count = len(self.todos)
        self.todos = [t for t in self.todos if not t["completed"]]
        self._save_todos()
        return original_count - len(self.todos)
    
    def get_stats(self):
        """Görev istatistikleri getir"""
        total = len(self.todos)
        completed = len(self.get_completed_todos())
        pending = len(self.get_pending_todos())
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_percentage": (completed / total * 100) if total > 0 else 0
        }
