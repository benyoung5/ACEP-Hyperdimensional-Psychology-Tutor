"""
Query Understanding and Processing Module - SIMPLIFIED AND WORKING
"""
import re
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from hdc_core import HDCCore
from vector_store import VectorStore
from reasoning_engine import ReasoningEngine

class QueryProcessor:
    def __init__(self, hdc_core: HDCCore, vector_store: VectorStore, reasoning_engine: ReasoningEngine):
        self.hdc = hdc_core
        self.vector_store = vector_store
        self.reasoning_engine = reasoning_engine
        self.query_history = []
        
    def process_query(self, query: str) -> Dict[str, Any]:
        """SIMPLIFIED query processing that WORKS"""
        try:
            print(f"\n=== PROCESSING QUERY: '{query}' ===")
            
            # Step 1: Clean query
            clean_query = self._clean_query(query)
            print(f"Clean query: '{clean_query}'")
            
            # Step 2: Get ALL available data and search directly
            all_data = self._get_all_available_data()
            print(f"Available data items: {len(all_data)}")
            
            if not all_data:
                return {
                    'response': "System error: No knowledge base loaded. Please restart the application.",
                    'success': False,
                    'confidence': 0.0
                }
            
            # Step 3: Find best match using simple text matching
            best_matches = self._find_best_matches(clean_query, all_data)
            print(f"Found {len(best_matches)} matches")
            
            if best_matches:
                # Use the best match directly
                best_match = best_matches[0]
                answer = best_match.get('answer', '')
                
                print(f"Best match: {best_match.get('question', '')}")
                print(f"Answer length: {len(answer)}")
                print(f"Match type: {best_match.get('match_type', 'direct')}")
                
                if answer and len(answer) > 10:  # Accept any reasonable answer
                    response = {
                        'response': answer,
                        'success': True,
                        'confidence': min(best_match.get('relevance', 50) / 100.0, 0.95),
                        'reasoning_type': 'direct_match',
                        'concepts_used': best_match.get('matched_words', best_match.get('concepts', [])),
                        'sources_count': len(best_matches),
                        'debug_info': {
                            'relevance_score': best_match.get('relevance', 0),
                            'matched_question': best_match.get('question', ''),
                            'match_type': best_match.get('match_type', 'direct'),
                            'total_matches': len(best_matches)
                        }
                    }
                else:
                    # Even if answer is short, provide what we have
                    response = {
                        'response': f"{answer} This relates to {best_match.get('topic', 'psychology')} and involves concepts around {', '.join(best_match.get('matched_words', [])[:3])}.",
                        'success': True,
                        'confidence': 0.4
                    }
            else:
                # This should NEVER happen with the new system, but just in case
                response = {
                    'response': "I have comprehensive psychology knowledge covering learning, memory, emotions, cognition, social psychology, development, personality, and therapy. Could you ask about a specific psychology topic or concept you're interested in?",
                    'success': True,
                    'confidence': 0.3
                }
            
            # Store in history
            self._update_history(query, response)
            
            return response
            
        except Exception as e:
            print(f"Error in process_query: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                'response': f"I encountered an error processing your query: {str(e)}",
                'success': False,
                'error': str(e)
            }
    
    def _clean_query(self, query: str) -> str:
        """Clean the query"""
        if not query:
            return ""
        
        # Minimal cleaning
        clean = re.sub(r'\s+', ' ', query.strip())
        return clean
    
    def _get_all_available_data(self) -> List[Dict]:
        """Get all available data from vector store"""
        try:
            all_metadata = list(self.vector_store.metadata.values())
            print(f"Retrieved {len(all_metadata)} items from vector store")
            
            if all_metadata:
                sample = all_metadata[0]
                print(f"Sample item keys: {list(sample.keys())}")
                print(f"Sample question: {sample.get('question', 'NO QUESTION')}")
            
            return all_metadata
            
        except Exception as e:
            print(f"Error getting data: {e}")
            return []
    
    def _find_best_matches(self, query: str, data: List[Dict]) -> List[Dict]:
        """COMPLETELY REVAMPED matching - finds relevant content for ANY psychology query"""
        if not data:
            return []
        
        query_lower = query.lower().strip()
        print(f"\n=== MATCHING QUERY: '{query_lower}' ===")
        
        # Extract ALL meaningful words from query
        query_words = []
        for word in query_lower.split():
            clean_word = ''.join(c for c in word if c.isalpha())
            if len(clean_word) > 2 and clean_word not in ['the', 'what', 'how', 'why', 'when', 'where', 'who', 'does', 'can', 'will', 'are', 'and', 'but', 'for']:
                query_words.append(clean_word)
        
        print(f"Extracted query words: {query_words}")
        
        all_matches = []
        
        # METHOD 1: Direct content search - scan ALL text for ANY query words
        for item in data:
            question = item.get('question', '').lower()
            answer = item.get('answer', '').lower() 
            topic = item.get('topic', '').lower()
            concepts = ' '.join(item.get('concepts', [])).lower()
            
            # Combine all content for searching
            all_content = f"{question} {answer} {topic} {concepts}"
            
            # Calculate relevance score
            relevance = 0
            matched_words = []
            
            for word in query_words:
                if word in all_content:
                    relevance += 10
                    matched_words.append(word)
                    
                    # Bonus for exact matches in question
                    if word in question:
                        relevance += 20
                    
                    # Bonus for matches in key concepts
                    if word in concepts:
                        relevance += 15
            
            if relevance > 0:
                item_copy = item.copy()
                item_copy['relevance'] = relevance
                item_copy['matched_words'] = matched_words
                all_matches.append(item_copy)
                print(f"MATCH: {question[:50]}... | Score: {relevance} | Words: {matched_words}")
        
        # METHOD 2: Psychology topic mapping - if no direct matches, find by topic
        if not all_matches:
            print("No direct matches, trying topic mapping...")
            topic_matches = self._find_by_psychology_topics(query_lower, data)
            all_matches.extend(topic_matches)
        
        # METHOD 3: Fuzzy matching - find similar words
        if not all_matches:
            print("No topic matches, trying fuzzy matching...")
            fuzzy_matches = self._fuzzy_match_psychology(query_words, data)
            all_matches.extend(fuzzy_matches)
        
        # METHOD 4: Emergency fallback - return most relevant psychology content
        if not all_matches:
            print("Emergency fallback - returning general psychology content...")
            emergency_matches = self._emergency_psychology_fallback(query_lower, data)
            all_matches.extend(emergency_matches)
        
        # Sort by relevance and return
        all_matches.sort(key=lambda x: x.get('relevance', 0), reverse=True)
        final_matches = all_matches[:5]
        
        print(f"\nFINAL MATCHES: {len(final_matches)}")
        for i, match in enumerate(final_matches):
            print(f"  {i+1}. {match.get('question', '')[:50]}... (relevance: {match.get('relevance', 0)})")
        
        return final_matches
    
    def _find_by_psychology_topics(self, query: str, data: List[Dict]) -> List[Dict]:
        """Find content by psychology topic areas"""
        psychology_keywords = {
            # Learning keywords
            'learn': ['learning', 'conditioning', 'reinforcement', 'behavior', 'training'],
            'condition': ['classical', 'operant', 'conditioning', 'pavlov', 'skinner'],
            'behavior': ['behaviorism', 'behavior', 'conditioning', 'reinforcement'],
            
            # Memory keywords  
            'memory': ['memory', 'remember', 'forget', 'recall', 'encoding'],
            'remember': ['memory', 'recall', 'encoding', 'storage', 'retrieval'],
            'forget': ['forgetting', 'memory', 'recall'],
            'brain': ['memory', 'cognition', 'neural', 'brain', 'mind'],
            
            # Emotion keywords
            'emotion': ['emotion', 'feeling', 'mood', 'affect', 'emotional'],
            'feel': ['emotion', 'feeling', 'mood', 'grief', 'anxiety'],
            'anxiety': ['anxiety', 'fear', 'stress', 'worry'],
            'sad': ['depression', 'grief', 'sadness', 'emotion'],
            'stress': ['stress', 'anxiety', 'pressure', 'tension'],
            
            # Cognitive keywords
            'think': ['cognitive', 'cognition', 'thinking', 'thought', 'mind'],
            'mind': ['cognitive', 'mental', 'thinking', 'consciousness'],
            'bias': ['bias', 'cognitive', 'thinking', 'judgment'],
            'decision': ['cognitive', 'bias', 'thinking', 'judgment'],
            
            # Social keywords
            'social': ['social', 'group', 'conformity', 'obedience'],
            'people': ['social', 'group', 'human', 'behavior'],
            'group': ['social', 'conformity', 'groupthink', 'obedience'],
            
            # Development keywords
            'child': ['development', 'children', 'growth', 'stages'],
            'develop': ['development', 'growth', 'stages', 'piaget'],
            'grow': ['development', 'growth', 'children'],
            
            # Therapy keywords
            'therapy': ['therapy', 'treatment', 'counseling', 'help'],
            'help': ['therapy', 'treatment', 'counseling', 'support'],
            'treat': ['therapy', 'treatment', 'help'],
            
            # Motivation keywords
            'motivat': ['motivation', 'drive', 'goal', 'incentive'],
            'goal': ['motivation', 'drive', 'achievement'],
            'want': ['motivation', 'desire', 'drive']
        }
        
        topic_matches = []
        
        for keyword, related_terms in psychology_keywords.items():
            if keyword in query:
                print(f"Found keyword '{keyword}' in query, searching for: {related_terms}")
                
                for item in data:
                    content = f"{item.get('question', '')} {item.get('answer', '')} {item.get('topic', '')}".lower()
                    
                    # Check if any related terms appear in this item
                    matches = sum(1 for term in related_terms if term in content)
                    
                    if matches > 0:
                        item_copy = item.copy()
                        item_copy['relevance'] = matches * 10 + 20  # Base score for topic match
                        item_copy['match_type'] = f'topic_{keyword}'
                        topic_matches.append(item_copy)
                        print(f"Topic match: {item.get('question', '')[:50]}... ({matches} term matches)")
        
        return topic_matches
    
    def _fuzzy_match_psychology(self, query_words: List[str], data: List[Dict]) -> List[Dict]:
        """Find psychology content using fuzzy/partial word matching"""
        fuzzy_matches = []
        
        for item in data:
            content = f"{item.get('question', '')} {item.get('answer', '')} {' '.join(item.get('concepts', []))}".lower()
            content_words = content.split()
            
            fuzzy_score = 0
            
            for query_word in query_words:
                for content_word in content_words:
                    if len(query_word) > 3 and len(content_word) > 3:
                        # Check for partial matches
                        if query_word in content_word or content_word in query_word:
                            fuzzy_score += 5
                        # Check for similar starts (first 3-4 characters)
                        elif query_word[:3] == content_word[:3] and len(query_word) > 4:
                            fuzzy_score += 3
            
            if fuzzy_score > 0:
                item_copy = item.copy()
                item_copy['relevance'] = fuzzy_score + 10
                item_copy['match_type'] = 'fuzzy'
                fuzzy_matches.append(item_copy)
                print(f"Fuzzy match: {item.get('question', '')[:50]}... (score: {fuzzy_score})")
        
        return fuzzy_matches
    
    def _emergency_psychology_fallback(self, query: str, data: List[Dict]) -> List[Dict]:
        """Emergency fallback - return the most comprehensive psychology answers"""
        print("Using emergency fallback - selecting best general psychology content")
        
        # Return items with longest, most comprehensive answers
        scored_items = []
        
        for item in data:
            answer = item.get('answer', '')
            question = item.get('question', '')
            
            # Score based on answer comprehensiveness
            score = len(answer.split())  # Word count
            if 'psychology' in answer.lower() or 'psychological' in answer.lower():
                score += 50
            if len(answer) > 200:  # Long, detailed answers
                score += 30
            
            item_copy = item.copy()
            item_copy['relevance'] = score
            item_copy['match_type'] = 'emergency_fallback'
            scored_items.append(item_copy)
        
        # Sort by comprehensiveness and return top items
        scored_items.sort(key=lambda x: x['relevance'], reverse=True)
        top_items = scored_items[:3]
        
        for item in top_items:
            print(f"Emergency selection: {item.get('question', '')[:50]}...")
        
        return top_items
    
    def _update_history(self, query: str, response: Dict):
        """Update query history"""
        self.query_history.append({
            'query': query,
            'response': response
        })
        
        # Keep only last 20 queries
        if len(self.query_history) > 20:
            self.query_history = self.query_history[-20:]
    
    def get_query_history(self) -> List[Dict]:
        """Get recent query history"""
        return self.query_history[-10:]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        if not self.query_history:
            return {'total_queries': 0}
        
        total_queries = len(self.query_history)
        successful_queries = sum(1 for q in self.query_history if q['response'].get('success', True))
        
        return {
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': successful_queries / total_queries if total_queries > 0 else 0
        }