"""
To-Do List yöneticisinin testleri
"""

import pytest
import json
from pathlib import Path
import tempfile
import shutil

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from todo_manager import TodoManager


class TestTodoManager:
    """TodoManager sınıfı testleri"""
    
    @pytest.fixture
    def temp_dir(self):
        """Geçici dizin oluştur"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def todo_manager(self, temp_dir):
        """TodoManager örneği oluştur"""
        return TodoManager(data_dir=temp_dir)
    
    def test_add_todo(self, todo_manager):
        """Görev ekleme testı"""
        todo = todo_manager.add_todo("Test Görev", "Test açıklaması", "high")
        
        assert todo is not None
        assert todo["title"] == "Test Görev"
        assert todo["description"] == "Test açıklaması"
        assert todo["priority"] == "high"
        assert todo["completed"] is False
    
    def test_add_empty_todo(self, todo_manager):
        """Boş görev ekleme testı"""
        todo = todo_manager.add_todo("", "Açıklama")
        assert todo is None
    
    def test_get_all_todos(self, todo_manager):
        """Tüm görevleri getirme testı"""
        todo_manager.add_todo("Görev 1")
        todo_manager.add_todo("Görev 2")
        
        todos = todo_manager.get_all_todos()
        assert len(todos) == 2
    
    def test_get_todo(self, todo_manager):
        """Belirli görev getirme testı"""
        todo1 = todo_manager.add_todo("Görev 1")
        todo2 = todo_manager.get_todo(todo1["id"])
        
        assert todo1["id"] == todo2["id"]
        assert todo1["title"] == todo2["title"]
    
    def test_update_todo(self, todo_manager):
        """Görev güncelleme testı"""
        todo = todo_manager.add_todo("Eski Başlık")
        updated = todo_manager.update_todo(todo["id"], title="Yeni Başlık")
        
        assert updated["title"] == "Yeni Başlık"
    
    def test_complete_todo(self, todo_manager):
        """Görev tamamlama testı"""
        todo = todo_manager.add_todo("Tamamlanacak Görev")
        completed = todo_manager.complete_todo(todo["id"])
        
        assert completed["completed"] is True
        assert completed["completed_at"] is not None
    
    def test_uncomplete_todo(self, todo_manager):
        """Görev tamamlanmış olarak işaretini kaldırma testı"""
        todo = todo_manager.add_todo("Görev")
        todo_manager.complete_todo(todo["id"])
        uncompleted = todo_manager.uncomplete_todo(todo["id"])
        
        assert uncompleted["completed"] is False
        assert uncompleted["completed_at"] is None
    
    def test_delete_todo(self, todo_manager):
        """Görev silme testı"""
        todo = todo_manager.add_todo("Silinecek Görev")
        result = todo_manager.delete_todo(todo["id"])
        
        assert result is True
        assert len(todo_manager.get_all_todos()) == 0
    
    def test_get_pending_todos(self, todo_manager):
        """Beklemede olan görevleri getirme testı"""
        todo1 = todo_manager.add_todo("Görev 1")
        todo2 = todo_manager.add_todo("Görev 2")
        todo_manager.complete_todo(todo1["id"])
        
        pending = todo_manager.get_pending_todos()
        assert len(pending) == 1
        assert pending[0]["id"] == todo2["id"]
    
    def test_get_completed_todos(self, todo_manager):
        """Tamamlanmış görevleri getirme testı"""
        todo1 = todo_manager.add_todo("Görev 1")
        todo2 = todo_manager.add_todo("Görev 2")
        todo_manager.complete_todo(todo1["id"])
        
        completed = todo_manager.get_completed_todos()
        assert len(completed) == 1
        assert completed[0]["id"] == todo1["id"]
    
    def test_get_todos_by_priority(self, todo_manager):
        """Önceliklere göre görevleri getirme testı"""
        todo_manager.add_todo("Düşük Öncelik", priority="low")
        todo_manager.add_todo("Yüksek Öncelik 1", priority="high")
        todo_manager.add_todo("Yüksek Öncelik 2", priority="high")
        
        high_priority = todo_manager.get_todos_by_priority("high")
        assert len(high_priority) == 2
    
    def test_clear_completed(self, todo_manager):
        """Tamamlanmış görevleri temizleme testı"""
        todo1 = todo_manager.add_todo("Görev 1")
        todo2 = todo_manager.add_todo("Görev 2")
        todo_manager.complete_todo(todo1["id"])
        
        cleared = todo_manager.clear_completed()
        assert cleared == 1
        assert len(todo_manager.get_all_todos()) == 1
    
    def test_get_stats(self, todo_manager):
        """İstatistikler getirme testı"""
        todo1 = todo_manager.add_todo("Görev 1")
        todo2 = todo_manager.add_todo("Görev 2")
        todo3 = todo_manager.add_todo("Görev 3")
        
        todo_manager.complete_todo(todo1["id"])
        todo_manager.complete_todo(todo2["id"])
        
        stats = todo_manager.get_stats()
        assert stats["total"] == 3
        assert stats["completed"] == 2
        assert stats["pending"] == 1
        assert stats["completion_percentage"] == pytest.approx(66.67, 0.1)
    
    def test_persistence(self, temp_dir):
        """Veri kalıcılığı testı"""
        manager1 = TodoManager(data_dir=temp_dir)
        manager1.add_todo("Kalıcı Görev")
        
        manager2 = TodoManager(data_dir=temp_dir)
        todos = manager2.get_all_todos()
        
        assert len(todos) == 1
        assert todos[0]["title"] == "Kalıcı Görev"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
