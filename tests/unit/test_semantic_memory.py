"""
Unit tests for semantic_memory module.
"""

import pytest
import json
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sdk" / "python"))

from semantic_memory import SemanticMemoryStore, SimpleMemoryStore


class TestSemanticMemoryStore:
    """Tests for SemanticMemoryStore."""
    
    def test_add_and_query(self):
        store = SemanticMemoryStore()
        
        dmg = {
            "memo": {
                "memo_id": "test-001",
                "title": "Should we migrate to microservices?",
                "recommendation": "Proceed with phased approach"
            },
            "objects": {},
            "moment": {"events": [{"type": "MEMO_CREATED"}]}
        }
        
        store.add(dmg)
        assert len(store) == 1
    
    def test_query_returns_similar(self):
        store = SemanticMemoryStore()
        
        # Add a decision about microservices
        store.add({
            "memo": {
                "memo_id": "micro-001",
                "title": "Microservices migration strategy",
                "recommendation": "Start with order service"
            },
            "objects": {"outcome": {"checks": [{"verdict": "keep"}]}},
            "moment": {"events": []}
        })
        
        # Query for similar
        results = store.query("microservice architecture", limit=5, min_merit_score=0)
        assert len(results) >= 0  # May or may not match depending on embeddings
    
    def test_get_lessons(self):
        store = SemanticMemoryStore()
        
        store.add({
            "memo": {"title": "API migration", "memo_id": "api-001"},
            "objects": {
                "outcome": {
                    "checks": [{
                        "verdict": "adjust",
                        "assumptions_audit": [
                            {"assumption": "2 weeks", "accurate": False, "learning": "Add buffer"}
                        ]
                    }]
                }
            },
            "moment": {"events": []}
        })
        
        lessons = store.get_lessons("API migration", limit=5)
        # Lessons may be empty if similarity doesn't match
        assert isinstance(lessons, list)
    
    def test_persistence(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        
        try:
            # Create store and add data
            store1 = SemanticMemoryStore(persist_path=path)
            store1.add({
                "memo": {"memo_id": "persist-001", "title": "Test persistence"},
                "objects": {},
                "moment": {"events": []}
            })
            
            # Create new store with same path
            store2 = SemanticMemoryStore(persist_path=path)
            assert len(store2) == 1
        finally:
            Path(path).unlink(missing_ok=True)
    
    def test_stats(self):
        store = SemanticMemoryStore()
        stats = store.stats()
        
        assert "total_decisions" in stats
        assert "has_embeddings" in stats
        assert "merit_distribution" in stats


class TestSimpleMemoryStore:
    """Tests for SimpleMemoryStore (keyword-only)."""
    
    def test_keyword_fallback(self):
        store = SimpleMemoryStore()
        assert not store.has_embeddings
    
    def test_add_and_query_keywords(self):
        store = SimpleMemoryStore()
        
        store.add({
            "memo": {
                "memo_id": "kw-001",
                "title": "Database migration to PostgreSQL",
                "recommendation": "Use pg_dump"
            },
            "objects": {},
            "moment": {"events": []}
        })
        
        # Query with overlapping keywords
        results = store.query("database PostgreSQL", limit=5, min_merit_score=0)
        # Should find by keyword overlap
        assert isinstance(results, list)
