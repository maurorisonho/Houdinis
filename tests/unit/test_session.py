"""
Houdinis Framework - Unit Tests for Session Manager
Tests session creation, management, and lifecycle
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.session import Session, SessionManager


class TestSession:
    """Test Session dataclass"""
    
    def test_session_creation(self):
        """Test session is created with correct attributes"""
        data = {'key': 'value', 'result': 'success'}
        session = Session(
            id=1,
            session_type='quantum_exploit',
            target='192.168.1.1',
            status='active',
            created_at=datetime.now(),
            data=data
        )
        
        assert session.id == 1
        assert session.session_type == 'quantum_exploit'
        assert session.target == '192.168.1.1'
        assert session.status == 'active'
        assert session.data == data
        assert isinstance(session.created_at, datetime)
    
    def test_session_default_status(self):
        """Test session default status is set to active"""
        session = Session(
            id=1,
            session_type='test',
            target='target',
            status='',
            created_at=datetime.now(),
            data={}
        )
        
        assert session.status == 'active'


class TestSessionManager:
    """Test SessionManager functionality"""
    
    @pytest.fixture
    def manager(self):
        """Create SessionManager instance"""
        return SessionManager()
    
    def test_manager_initialization(self, manager):
        """Test session manager initializes correctly"""
        assert manager.sessions == {}
        assert manager.next_id == 1
    
    def test_create_session(self, manager):
        """Test creating a new session"""
        data = {'quantum_state': 'entangled'}
        session = manager.create_session(
            session_type='quantum_exploit',
            target='192.168.1.100',
            data=data
        )
        
        assert session.id == 1
        assert session.session_type == 'quantum_exploit'
        assert session.target == '192.168.1.100'
        assert session.status == 'active'
        assert session.data == data
        assert isinstance(session.created_at, datetime)
    
    def test_create_multiple_sessions(self, manager):
        """Test creating multiple sessions increments IDs"""
        session1 = manager.create_session('type1', 'target1', {})
        session2 = manager.create_session('type2', 'target2', {})
        session3 = manager.create_session('type3', 'target3', {})
        
        assert session1.id == 1
        assert session2.id == 2
        assert session3.id == 3
        assert manager.next_id == 4
    
    def test_get_session_exists(self, manager):
        """Test getting an existing session"""
        created = manager.create_session('test', 'target', {'key': 'value'})
        
        retrieved = manager.get_session(created.id)
        assert retrieved == created
        assert retrieved.data == {'key': 'value'}
    
    def test_get_session_not_exists(self, manager):
        """Test getting a non-existent session"""
        retrieved = manager.get_session(999)
        assert retrieved is None
    
    def test_get_sessions_empty(self, manager):
        """Test getting sessions when none exist"""
        sessions = manager.get_sessions()
        assert sessions == []
    
    def test_get_sessions_multiple(self, manager):
        """Test getting all sessions"""
        manager.create_session('type1', 'target1', {})
        manager.create_session('type2', 'target2', {})
        manager.create_session('type3', 'target3', {})
        
        sessions = manager.get_sessions()
        assert len(sessions) == 3
        assert all(isinstance(s, Session) for s in sessions)
    
    def test_kill_session_exists(self, manager):
        """Test killing an existing session"""
        session = manager.create_session('test', 'target', {})
        
        assert session.id in manager.sessions
        
        result = manager.kill_session(session.id)
        assert result is True
        assert session.id not in manager.sessions
    
    def test_kill_session_not_exists(self, manager):
        """Test killing a non-existent session"""
        result = manager.kill_session(999)
        assert result is False
    
    def test_kill_all_sessions(self, manager):
        """Test killing all sessions"""
        manager.create_session('type1', 'target1', {})
        manager.create_session('type2', 'target2', {})
        manager.create_session('type3', 'target3', {})
        
        assert len(manager.sessions) == 3
        
        count = manager.kill_all_sessions()
        assert count == 3
        assert len(manager.sessions) == 0
    
    def test_kill_all_sessions_empty(self, manager):
        """Test killing all sessions when none exist"""
        count = manager.kill_all_sessions()
        assert count == 0


@pytest.mark.unit
class TestSessionLifecycle:
    """Test session lifecycle management"""
    
    @pytest.fixture
    def manager(self):
        """Create SessionManager instance"""
        return SessionManager()
    
    def test_session_creation_to_deletion(self, manager):
        """Test complete session lifecycle"""
        # Create
        session = manager.create_session(
            'quantum_exploit',
            '192.168.1.1',
            {'factored_key': 'RSA-2048'}
        )
        
        assert session.status == 'active'
        assert len(manager.sessions) == 1
        
        # Retrieve
        retrieved = manager.get_session(session.id)
        assert retrieved == session
        
        # Delete
        killed = manager.kill_session(session.id)
        assert killed is True
        assert len(manager.sessions) == 0
    
    def test_multiple_sessions_independent(self, manager):
        """Test multiple sessions are independent"""
        session1 = manager.create_session('type1', 'target1', {'data1': 'value1'})
        session2 = manager.create_session('type2', 'target2', {'data2': 'value2'})
        
        # Kill session1
        manager.kill_session(session1.id)
        
        # Session2 should still exist
        assert manager.get_session(session2.id) is not None
        assert len(manager.sessions) == 1
    
    def test_session_data_isolation(self, manager):
        """Test session data is isolated"""
        data1 = {'shared_key': 'value1'}
        data2 = {'shared_key': 'value2'}
        
        session1 = manager.create_session('type1', 'target1', data1)
        session2 = manager.create_session('type2', 'target2', data2)
        
        # Modify data1
        data1['shared_key'] = 'modified'
        
        # Session2 data should be unchanged
        assert session2.data['shared_key'] == 'value2'


@pytest.mark.integration
class TestSessionTypes:
    """Test different session types"""
    
    @pytest.fixture
    def manager(self):
        """Create SessionManager instance"""
        return SessionManager()
    
    def test_quantum_exploit_session(self, manager):
        """Test quantum exploit session"""
        session = manager.create_session(
            'quantum_exploit',
            '192.168.1.1',
            {
                'algorithm': 'shor',
                'qubits': 15,
                'result': 'factored_n=15_factors=3x5'
            }
        )
        
        assert session.session_type == 'quantum_exploit'
        assert session.data['algorithm'] == 'shor'
    
    def test_crypto_break_session(self, manager):
        """Test cryptography break session"""
        session = manager.create_session(
            'crypto_break',
            'tls://example.com:443',
            {
                'protocol': 'TLS 1.2',
                'cipher': 'RSA-2048',
                'broken': True,
                'private_key': 'REDACTED'
            }
        )
        
        assert session.session_type == 'crypto_break'
        assert session.data['broken'] is True
    
    def test_shell_session(self, manager):
        """Test shell session"""
        session = manager.create_session(
            'shell',
            '10.0.0.5:22',
            {
                'protocol': 'SSH',
                'username': 'root',
                'method': 'quantum_key_recovery'
            }
        )
        
        assert session.session_type == 'shell'
        assert session.data['protocol'] == 'SSH'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
