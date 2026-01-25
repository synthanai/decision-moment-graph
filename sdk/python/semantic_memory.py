"""
Semantic Memory Store

Embedding-based memory retrieval for the ENRICH phase of RESOLVE.
Uses sentence transformers (if available) or falls back to keyword matching.

Usage:
    from semantic_memory import SemanticMemoryStore
    
    store = SemanticMemoryStore()
    store.add(dmg)
    
    similar = store.query("Should we migrate?", limit=5)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import json
import hashlib
from pathlib import Path

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_EMBEDDINGS = True
except Exception:
    # Falls back gracefully on ImportError, NumPy conflicts, or any other issue
    HAS_EMBEDDINGS = False


@dataclass
class StoredDecision:
    """A decision stored in memory with embedding."""
    dmg_id: str
    question: str
    recommendation: str
    merit_score: int
    outcome_success: Optional[bool]
    embedding: Optional[List[float]]
    created_at: str
    dmg: Dict[str, Any]
    lessons: List[str] = field(default_factory=list)


class SemanticMemoryStore:
    """
    Semantic memory store with embedding-based similarity search.
    
    Falls back to keyword matching if sentence-transformers not available.
    """
    
    DEFAULT_MODEL = "all-MiniLM-L6-v2"  # Fast, good quality
    
    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        persist_path: Optional[str] = None,
        similarity_threshold: float = 0.5
    ):
        self.persist_path = Path(persist_path) if persist_path else None
        self.similarity_threshold = similarity_threshold
        self.decisions: List[StoredDecision] = []
        
        # Initialize embedding model if available
        self.model = None
        if HAS_EMBEDDINGS:
            try:
                self.model = SentenceTransformer(model_name)
                self.has_embeddings = True
            except Exception as e:
                print(f"⚠️ Could not load embedding model: {e}")
                self.has_embeddings = False
        else:
            self.has_embeddings = False
        
        # Load persisted data
        if self.persist_path and self.persist_path.exists():
            self._load()
    
    def add(self, dmg: Dict[str, Any]) -> str:
        """
        Add a DMG to memory.
        
        Returns the generated ID.
        """
        memo = dmg.get("memo", {})
        objects = dmg.get("objects", {})
        
        # Generate ID
        dmg_id = memo.get("memo_id") or self._generate_id(memo.get("title", ""))
        
        # Extract question/recommendation
        question = memo.get("title", "")
        recommendation = memo.get("recommendation", memo.get("decision", ""))
        
        # Calculate merit score
        merit_score = dmg.get("merit_score", self._calculate_merit(dmg))
        
        # Determine outcome success
        outcome = objects.get("outcome", {})
        checks = outcome.get("checks", [])
        outcome_success = None
        if checks:
            latest = checks[-1]
            outcome_success = latest.get("verdict") in ("keep", "adjust")
        
        # Extract lessons
        lessons = self._extract_lessons(dmg)
        
        # Generate embedding
        embedding = None
        if self.has_embeddings:
            text = f"{question} {recommendation}"
            embedding = self.model.encode(text).tolist()
        
        # Create stored decision
        decision = StoredDecision(
            dmg_id=dmg_id,
            question=question,
            recommendation=recommendation,
            merit_score=merit_score,
            outcome_success=outcome_success,
            embedding=embedding,
            created_at=datetime.now().isoformat(),
            dmg=dmg,
            lessons=lessons
        )
        
        # Add to store (update if exists)
        existing_idx = next(
            (i for i, d in enumerate(self.decisions) if d.dmg_id == dmg_id),
            None
        )
        if existing_idx is not None:
            self.decisions[existing_idx] = decision
        else:
            self.decisions.append(decision)
        
        # Persist
        if self.persist_path:
            self._save()
        
        return dmg_id
    
    def query(
        self,
        question: str,
        limit: int = 5,
        min_merit_score: int = 3,
        domain: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query similar decisions from memory.
        
        Returns list of DMG dicts, most similar first.
        """
        if not self.decisions:
            return []
        
        # Filter by merit score
        candidates = [d for d in self.decisions if d.merit_score >= min_merit_score]
        
        if not candidates:
            return []
        
        # Rank by similarity
        if self.has_embeddings:
            ranked = self._rank_by_embedding(question, candidates)
        else:
            ranked = self._rank_by_keywords(question, candidates)
        
        # Filter by threshold and limit
        results = [
            d.dmg for d, score in ranked
            if score >= self.similarity_threshold
        ][:limit]
        
        return results
    
    def get_lessons(self, question: str, limit: int = 10) -> List[str]:
        """Get lessons learned from similar decisions."""
        similar = self.query(question, limit=5, min_merit_score=2)
        
        all_lessons = []
        for dmg in similar:
            lessons = self._extract_lessons(dmg)
            all_lessons.extend(lessons)
        
        return all_lessons[:limit]
    
    def _rank_by_embedding(
        self,
        question: str,
        candidates: List[StoredDecision]
    ) -> List[Tuple[StoredDecision, float]]:
        """Rank candidates by embedding similarity."""
        query_embedding = np.array(self.model.encode(question))
        
        scored = []
        for decision in candidates:
            if decision.embedding:
                candidate_embedding = np.array(decision.embedding)
                # Cosine similarity
                similarity = np.dot(query_embedding, candidate_embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(candidate_embedding)
                )
                scored.append((decision, float(similarity)))
            else:
                scored.append((decision, 0.0))
        
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _rank_by_keywords(
        self,
        question: str,
        candidates: List[StoredDecision]
    ) -> List[Tuple[StoredDecision, float]]:
        """Rank candidates by keyword overlap (fallback)."""
        query_words = set(question.lower().split())
        
        scored = []
        for decision in candidates:
            doc_words = set(f"{decision.question} {decision.recommendation}".lower().split())
            
            # Jaccard similarity
            intersection = len(query_words & doc_words)
            union = len(query_words | doc_words)
            similarity = intersection / union if union > 0 else 0.0
            
            scored.append((decision, similarity))
        
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def _calculate_merit(self, dmg: Dict[str, Any]) -> int:
        """Calculate MERIT score for a DMG."""
        score = 0
        objects = dmg.get("objects", {})
        memo = dmg.get("memo", {})
        moment = dmg.get("moment", {})
        
        # M: Measured
        if objects.get("outcome", {}).get("checks"):
            score += 1
        
        # E: Evidenced
        if objects.get("traces"):
            score += 1
        
        # R: Reversible
        doors = objects.get("doors", {})
        if doors.get("own", {}).get("name") and doors.get("ready"):
            score += 1
        
        # I: Inspectable
        events = moment.get("events", [])
        if events:
            score += 1
        
        # T: Traceable
        if len(events) > 1:
            score += 1
        
        return score
    
    def _extract_lessons(self, dmg: Dict[str, Any]) -> List[str]:
        """Extract lessons learned from outcome checks."""
        lessons = []
        objects = dmg.get("objects", {})
        outcome = objects.get("outcome", {})
        
        for check in outcome.get("checks", []):
            # From assumption audits
            for audit in check.get("assumptions_audit", []):
                if not audit.get("accurate", True):
                    learning = audit.get("learning", "")
                    if learning:
                        lessons.append(learning)
            
            # From vindicated dissents
            for audit in check.get("dissent_audit", []):
                if audit.get("vindicated", False):
                    note = audit.get("note", "")
                    if note:
                        lessons.append(f"Dissent validated: {note}")
        
        return lessons
    
    def _generate_id(self, title: str) -> str:
        """Generate unique ID from title and timestamp."""
        content = f"{title}{datetime.now().isoformat()}"
        return f"dmg-{hashlib.sha256(content.encode()).hexdigest()[:12]}"
    
    def _save(self):
        """Persist decisions to disk."""
        if not self.persist_path:
            return
        
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = []
        for d in self.decisions:
            data.append({
                "dmg_id": d.dmg_id,
                "question": d.question,
                "recommendation": d.recommendation,
                "merit_score": d.merit_score,
                "outcome_success": d.outcome_success,
                "embedding": d.embedding,
                "created_at": d.created_at,
                "lessons": d.lessons,
                "dmg": d.dmg
            })
        
        with open(self.persist_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load(self):
        """Load decisions from disk."""
        if not self.persist_path or not self.persist_path.exists():
            return
        
        try:
            with open(self.persist_path, 'r') as f:
                data = json.load(f)
            
            self.decisions = [
                StoredDecision(
                    dmg_id=d["dmg_id"],
                    question=d["question"],
                    recommendation=d["recommendation"],
                    merit_score=d["merit_score"],
                    outcome_success=d.get("outcome_success"),
                    embedding=d.get("embedding"),
                    created_at=d["created_at"],
                    lessons=d.get("lessons", []),
                    dmg=d["dmg"]
                )
                for d in data
            ]
        except Exception as e:
            print(f"⚠️ Could not load memory: {e}")
            self.decisions = []
    
    def __len__(self) -> int:
        return len(self.decisions)
    
    def stats(self) -> Dict[str, Any]:
        """Return memory statistics."""
        merit_dist = {}
        for d in self.decisions:
            merit_dist[d.merit_score] = merit_dist.get(d.merit_score, 0) + 1
        
        return {
            "total_decisions": len(self.decisions),
            "has_embeddings": self.has_embeddings,
            "merit_distribution": merit_dist,
            "total_lessons": sum(len(d.lessons) for d in self.decisions)
        }


# Convenience alias for simple memory store (keyword-based)
class SimpleMemoryStore(SemanticMemoryStore):
    """Simple keyword-based memory store without embeddings."""
    
    def __init__(self, persist_path: Optional[str] = None):
        super().__init__(persist_path=persist_path)
        self.has_embeddings = False  # Force keyword mode
        self.model = None


if __name__ == "__main__":
    # Demo
    store = SemanticMemoryStore()
    
    # Add sample decision
    sample_dmg = {
        "memo": {
            "memo_id": "test-001",
            "title": "Should we migrate to microservices?",
            "recommendation": "Proceed with phased approach",
            "ramp": {"level": 3}
        },
        "objects": {
            "outcome": {
                "checks": [
                    {
                        "verdict": "keep",
                        "assumptions_audit": [
                            {"assumption": "2 weeks", "accurate": False, "learning": "Add 100% buffer"}
                        ]
                    }
                ]
            }
        },
        "moment": {"events": [{"type": "MEMO_CREATED"}]}
    }
    
    store.add(sample_dmg)
    
    # Query
    results = store.query("microservice migration", limit=3)
    print(f"Found {len(results)} similar decisions")
    
    lessons = store.get_lessons("microservice migration")
    print(f"Lessons: {lessons}")
    
    print(f"Stats: {store.stats()}")
