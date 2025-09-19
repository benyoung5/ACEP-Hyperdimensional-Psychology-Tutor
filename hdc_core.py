"""
Core Hyperdimensional Computing Operations
"""
import numpy as np
import torch
from typing import Dict, List, Tuple, Optional
import random

class HDCCore:
    def __init__(self, dim: int = 10000, device: str = "cpu"):
        """
        Initialize HDC with specified dimensions
        """
        self.dim = dim
        self.device = device
        self.concept_vectors = {}
        self.memory_bank = {}
        
    def generate_random_vector(self, seed: Optional[int] = None) -> np.ndarray:
        """Generate a random bipolar hypervector"""
        if seed:
            np.random.seed(seed)
        return np.random.choice([-1, 1], size=self.dim)
    
    def bind(self, vec1: np.ndarray, vec2: np.ndarray) -> np.ndarray:
        """Bind two vectors using element-wise multiplication"""
        return vec1 * vec2
    
    def bundle(self, vectors: List[np.ndarray]) -> np.ndarray:
        """Bundle multiple vectors using element-wise addition and thresholding"""
        if not vectors:
            return np.zeros(self.dim)
        
        result = np.sum(vectors, axis=0)
        # Threshold to maintain bipolar nature
        return np.where(result > 0, 1, -1)
    
    def permute(self, vec: np.ndarray, shift: int = 1) -> np.ndarray:
        """Permute vector by circular shift"""
        return np.roll(vec, shift)
    
    def similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        if np.allclose(vec1, 0) or np.allclose(vec2, 0):
            return 0.0
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
    
    def hamming_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate normalized Hamming similarity"""
        if len(vec1) != len(vec2):
            return 0.0
        
        # For bipolar vectors, similarity is the fraction of matching elements
        matches = np.sum(vec1 == vec2)
        total = len(vec1)
        return matches / total
    
    def create_concept_vector(self, concept: str, seed: Optional[int] = None) -> np.ndarray:
        """Create or retrieve a concept vector"""
        if concept in self.concept_vectors:
            return self.concept_vectors[concept]
        
        # Use concept hash as seed for reproducibility
        if seed is None:
            seed = hash(concept) % (2**32)
        
        vector = self.generate_random_vector(seed)
        self.concept_vectors[concept] = vector
        return vector
    
    def encode_sequence(self, sequence: List[str]) -> np.ndarray:
        """Encode a sequence using position binding"""
        if not sequence:
            return np.zeros(self.dim)
        
        encoded_items = []
        for i, item in enumerate(sequence):
            item_vector = self.create_concept_vector(item)
            position_vector = self.create_concept_vector(f"pos_{i}")
            encoded_items.append(self.bind(item_vector, position_vector))
        
        return self.bundle(encoded_items)
    
    def encode_relations(self, relations: List[Tuple[str, str, str]]) -> np.ndarray:
        """Encode subject-predicate-object relations"""
        relation_vectors = []
        
        for subject, predicate, obj in relations:
            s_vec = self.create_concept_vector(subject)
            p_vec = self.create_concept_vector(predicate)
            o_vec = self.create_concept_vector(obj)
            
            # Encode as (subject * predicate) + (predicate * object)
            relation_vec = self.bundle([
                self.bind(s_vec, p_vec),
                self.bind(p_vec, o_vec)
            ])
            relation_vectors.append(relation_vec)
        
        return self.bundle(relation_vectors)
    
    def query_memory(self, query_vector: np.ndarray, threshold: float = 0.3) -> List[Tuple[str, float]]:
        """Query memory bank and return similar items"""
        results = []
        
        for key, stored_vector in self.memory_bank.items():
            similarity = self.hamming_similarity(query_vector, stored_vector)
            if similarity > threshold:
                results.append((key, similarity))
        
        return sorted(results, key=lambda x: x[1], reverse=True)
    
    def store_memory(self, key: str, vector: np.ndarray):
        """Store a vector in memory bank"""
        self.memory_bank[key] = vector
    
    def cleanup_memory(self, vector: np.ndarray, candidates: List[np.ndarray]) -> np.ndarray:
        """Clean up noisy vector using candidate vectors"""
        if not candidates:
            return vector
        
        best_match = candidates[0]
        best_similarity = self.hamming_similarity(vector, candidates[0])
        
        for candidate in candidates[1:]:
            sim = self.hamming_similarity(vector, candidate)
            if sim > best_similarity:
                best_similarity = sim
                best_match = candidate
        
        return best_match