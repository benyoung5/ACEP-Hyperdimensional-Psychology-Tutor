"""
HDC Vector Storage and Retrieval System
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
import pickle
import os
from hdc_core import HDCCore

class VectorStore:
    def __init__(self, hdc_core: HDCCore, storage_path: str = "vector_store.pkl"):
        self.hdc = hdc_core
        self.storage_path = storage_path
        self.vectors = {}
        self.metadata = {}
        self.concept_index = {}
        self.topic_index = {}
        
        # Load existing storage if available
        self.load_storage()
    
    def store_data(self, data_items: List[Dict]) -> int:
        """Store processed data items as HDC vectors"""
        stored_count = 0
        
        for i, item in enumerate(data_items):
            try:
                # Generate unique key
                key = f"item_{i}_{hash(item.get('question', ''))}"
                
                # Create HDC representation
                vector = self._create_item_vector(item)
                
                # Store vector and metadata
                self.vectors[key] = vector
                self.metadata[key] = {
                    'question': item.get('question', ''),
                    'answer': item.get('answer', ''),
                    'topic': item.get('topic', 'General'),
                    'difficulty': item.get('difficulty', 'basic'),
                    'concepts': item.get('concepts', [])
                }
                
                # Update indices
                self._update_indices(key, item)
                
                stored_count += 1
                
            except Exception as e:
                print(f"Error storing item {i}: {e}")
        
        # Save to disk
        self.save_storage()
        print(f"Stored {stored_count} items in vector store")
        
        return stored_count
    
    def _create_item_vector(self, item: Dict) -> np.ndarray:
        """Create HDC vector representation of an item"""
        vectors_to_bundle = []
        
        # Encode question
        if item.get('question'):
            question_tokens = item.get('question_tokens', item['question'].split())
            question_vector = self.hdc.encode_sequence(question_tokens)
            vectors_to_bundle.append(question_vector)
        
        # Encode answer
        if item.get('answer'):
            answer_tokens = item.get('answer_tokens', item['answer'].split())
            answer_vector = self.hdc.encode_sequence(answer_tokens)
            vectors_to_bundle.append(answer_vector)
        
        # Encode concepts
        if item.get('concepts'):
            concept_vectors = []
            for concept in item['concepts']:
                concept_vec = self.hdc.create_concept_vector(concept)
                concept_vectors.append(concept_vec)
            
            if concept_vectors:
                bundled_concepts = self.hdc.bundle(concept_vectors)
                vectors_to_bundle.append(bundled_concepts)
        
        # Encode topic
        if item.get('topic'):
            topic_vector = self.hdc.create_concept_vector(f"topic_{item['topic']}")
            vectors_to_bundle.append(topic_vector)
        
        # Encode difficulty
        if item.get('difficulty'):
            difficulty_vector = self.hdc.create_concept_vector(f"difficulty_{item['difficulty']}")
            vectors_to_bundle.append(difficulty_vector)
        
        # Bundle all vectors
        if vectors_to_bundle:
            return self.hdc.bundle(vectors_to_bundle)
        else:
            return np.zeros(self.hdc.dim)
    
    def _update_indices(self, key: str, item: Dict):
        """Update concept and topic indices"""
        # Update concept index
        for concept in item.get('concepts', []):
            if concept not in self.concept_index:
                self.concept_index[concept] = []
            self.concept_index[concept].append(key)
        
        # Update topic index
        topic = item.get('topic', 'General')
        if topic not in self.topic_index:
            self.topic_index[topic] = []
        self.topic_index[topic].append(key)
    
    def search_similar(self, query_vector: np.ndarray, top_k: int = 5, 
                      threshold: float = 0.1) -> List[Tuple[str, float, Dict]]:
        """Search for similar vectors with improved threshold"""
        results = []
        
        for key, stored_vector in self.vectors.items():
            # Try both similarity measures
            hamming_sim = self.hdc.hamming_similarity(query_vector, stored_vector)
            cosine_sim = self.hdc.similarity(query_vector, stored_vector)
            
            # Use the better of the two similarities
            similarity = max(hamming_sim, (cosine_sim + 1) / 2)  # Normalize cosine to [0,1]
            
            if similarity >= threshold:
                metadata = self.metadata.get(key, {})
                results.append((key, similarity, metadata))
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]
    
    def search_by_concepts(self, concepts: List[str], top_k: int = 5) -> List[Dict]:
        """Search by specific concepts"""
        matching_keys = set()
        
        for concept in concepts:
            if concept in self.concept_index:
                matching_keys.update(self.concept_index[concept])
        
        results = []
        for key in matching_keys:
            if key in self.metadata:
                metadata = self.metadata[key].copy()
                metadata['key'] = key
                results.append(metadata)
        
        return results[:top_k]
    
    def search_by_topic(self, topic: str) -> List[Dict]:
        """Search by topic"""
        if topic not in self.topic_index:
            return []
        
        results = []
        for key in self.topic_index[topic]:
            if key in self.metadata:
                metadata = self.metadata[key].copy()
                metadata['key'] = key
                results.append(metadata)
        
        return results
    
    def create_query_vector(self, query: str) -> np.ndarray:
        """Create HDC vector for a query with improved encoding"""
        query_tokens = query.lower().split()
        
        # Clean tokens
        cleaned_tokens = []
        for token in query_tokens:
            # Remove punctuation and keep only alphabetic characters
            clean_token = ''.join(c for c in token if c.isalpha())
            if len(clean_token) > 2:  # Only keep tokens longer than 2 characters
                cleaned_tokens.append(clean_token)
        
        if not cleaned_tokens:
            cleaned_tokens = ['general', 'query']  # Fallback
        
        return self.hdc.encode_sequence(cleaned_tokens)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        return {
            'total_vectors': len(self.vectors),
            'total_concepts': len(self.concept_index),
            'total_topics': len(self.topic_index),
            'topics': list(self.topic_index.keys()),
            'top_concepts': sorted(self.concept_index.keys())[:20]
        }
    
    def save_storage(self):
        """Save vector store to disk"""
        try:
            storage_data = {
                'vectors': self.vectors,
                'metadata': self.metadata,
                'concept_index': self.concept_index,
                'topic_index': self.topic_index
            }
            
            with open(self.storage_path, 'wb') as f:
                pickle.dump(storage_data, f)
                
        except Exception as e:
            print(f"Error saving storage: {e}")
    
    def load_storage(self):
        """Load vector store from disk"""
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'rb') as f:
                    storage_data = pickle.load(f)
                
                self.vectors = storage_data.get('vectors', {})
                self.metadata = storage_data.get('metadata', {})
                self.concept_index = storage_data.get('concept_index', {})
                self.topic_index = storage_data.get('topic_index', {})
                
                print(f"Loaded {len(self.vectors)} vectors from storage")
                
        except Exception as e:
            print(f"Error loading storage: {e}")
    
    def clear_storage(self):
        """Clear all stored data"""
        self.vectors.clear()
        self.metadata.clear()
        self.concept_index.clear()
        self.topic_index.clear()
        
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
        
        print("Storage cleared")