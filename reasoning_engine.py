"""
Human-like Reasoning Engine using HDC
"""
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from hdc_core import HDCCore
import re
import random

class ReasoningEngine:
    def __init__(self, hdc_core: HDCCore):
        self.hdc = hdc_core
        self.reasoning_patterns = {}
        self.context_memory = []
        self.confidence_threshold = 0.4
        
        # Initialize reasoning patterns
        self._init_reasoning_patterns()
        
    def _init_reasoning_patterns(self):
        """Initialize common reasoning patterns"""
        patterns = {
            'definition': ['what is', 'define', 'meaning of', 'explain'],
            'comparison': ['difference between', 'compare', 'versus', 'vs'],
            'causation': ['why does', 'what causes', 'reason for', 'because'],
            'process': ['how does', 'steps to', 'process of', 'mechanism'],
            'example': ['give example', 'for instance', 'such as', 'like'],
            'application': ['how to use', 'apply', 'practical', 'in practice'],
            'analysis': ['analyze', 'evaluate', 'assess', 'examine']
        }
        
        # Encode patterns as HDC vectors
        for pattern_type, phrases in patterns.items():
            pattern_vectors = []
            for phrase in phrases:
                phrase_vector = self.hdc.encode_sequence(phrase.split())
                pattern_vectors.append(phrase_vector)
            
            self.reasoning_patterns[pattern_type] = {
                'vectors': pattern_vectors,
                'combined': self.hdc.bundle(pattern_vectors)
            }
    
    def identify_reasoning_type(self, query: str) -> Tuple[str, float]:
        """Identify the type of reasoning required with better pattern matching"""
        query_lower = query.lower()
        
        # Direct pattern matching (more reliable than HDC for this)
        patterns = {
            'definition': ['what is', 'define', 'meaning of', 'explain what'],
            'comparison': ['difference between', 'compare', 'versus', 'vs', 'contrast'],
            'causation': ['why does', 'what causes', 'reason for', 'because', 'why'],
            'process': ['how does', 'how do', 'steps to', 'process of', 'mechanism'],
            'example': ['give example', 'examples of', 'for instance', 'such as'],
            'application': ['how to use', 'apply', 'practical', 'in practice'],
            'analysis': ['analyze', 'evaluate', 'assess', 'examine']
        }
        
        best_match = 'definition'  # Default to definition, not general
        best_score = 0
        
        for pattern_type, phrases in patterns.items():
            score = 0
            for phrase in phrases:
                if phrase in query_lower:
                    score += len(phrase.split())  # Longer phrases get higher scores
            
            if score > best_score:
                best_score = score
                best_match = pattern_type
        
        confidence = min(best_score / 10.0, 0.9)  # Convert to confidence
        
        print(f"[DEBUG] Query: '{query_lower}'")
        print(f"[DEBUG] Identified reasoning type: {best_match} (confidence: {confidence:.2f})")
        
        return best_match, confidence
    
    def reason_about_query(self, query: str, context_data: List[Dict]) -> Dict[str, Any]:
        """Main reasoning function with improved data handling"""
        # Identify reasoning type
        reasoning_type, confidence = self.identify_reasoning_type(query)
        
        # Extract key concepts from query
        query_concepts = self._extract_query_concepts(query)
        
        # Find relevant information - ensure we have the data
        relevant_info = context_data if context_data else []
        
        # If no relevant info found, try to get some from any available data
        if not relevant_info:
            # This should not happen if search is working properly
            print(f"Warning: No relevant info found for query: {query}")
        
        # Apply reasoning strategy with debugging
        reasoning_result = self._apply_reasoning_strategy(
            reasoning_type, query, query_concepts, relevant_info
        )
        
        # Generate human-like response
        response = self._generate_response(reasoning_result, reasoning_type)
        
        return {
            'response': response,
            'reasoning_type': reasoning_type,
            'confidence': reasoning_result.get('confidence', confidence),
            'concepts_used': query_concepts,
            'sources': relevant_info[:3],  # Top 3 sources
            'debug_info': {
                'relevant_info_count': len(relevant_info),
                'reasoning_result_type': reasoning_result.get('type', 'unknown')
            }
        }
    
    def _extract_query_concepts(self, query: str) -> List[str]:
        """Extract key concepts from the query"""
        # Simple concept extraction
        words = re.findall(r'\w+', query.lower())
        
        # Filter out common words
        stop_words = {'what', 'is', 'the', 'how', 'why', 'when', 'where', 
                     'can', 'does', 'do', 'are', 'a', 'an', 'and', 'or', 'but'}
        
        concepts = [word for word in words if len(word) > 2 and word not in stop_words]
        return concepts[:10]  # Limit to top 10 concepts
    
    def _find_relevant_information(self, concepts: List[str], context_data: List[Dict]) -> List[Dict]:
        """Find information relevant to the query concepts - REMOVED as we use context_data directly"""
        # This function is no longer needed since we pass context_data directly
        # but keeping for backward compatibility
        return context_data
    
    def _calculate_relevance(self, query_concepts: List[str], item: Dict) -> float:
        """Calculate relevance between query concepts and item"""
        item_concepts = item.get('concepts', [])
        item_text = (item.get('question', '') + ' ' + item.get('answer', '')).lower()
        
        # Direct concept overlap
        concept_overlap = len(set(query_concepts).intersection(set(item_concepts)))
        
        # Text-based similarity
        text_overlap = sum(1 for concept in query_concepts if concept in item_text)
        
        # Weighted score
        relevance = (concept_overlap * 2 + text_overlap) / (len(query_concepts) + 1)
        
        return min(relevance, 1.0)
    
    def _apply_reasoning_strategy(self, reasoning_type: str, query: str, 
                                concepts: List[str], relevant_info: List[Dict]) -> Dict:
        """Apply specific reasoning strategy - simplified and direct"""
        
        print(f"[REASONING] Type: {reasoning_type}, Info count: {len(relevant_info)}")
        
        if not relevant_info:
            return {
                'type': reasoning_type,
                'content': "I don't have enough information to answer your question. Please try rephrasing or asking about a different topic.",
                'confidence': 0.1
            }
        
        # Get the best answer available
        best_item = relevant_info[0]
        answer = best_item.get('answer', '').strip()
        
        print(f"[REASONING] Best answer preview: {answer[:100]}...")
        
        if not answer or len(answer) < 20:
            # Try other items
            for item in relevant_info[1:]:
                alt_answer = item.get('answer', '').strip()
                if alt_answer and len(alt_answer) >= 20:
                    answer = alt_answer
                    best_item = item
                    break
        
        if not answer or len(answer) < 20:
            return {
                'type': reasoning_type,
                'content': f"I found some information about your query, but it's not detailed enough. The topic relates to {best_item.get('topic', 'psychology')}.",
                'confidence': 0.2
            }
        
        # For all reasoning types, just return the best answer we have
        # The answer should be comprehensive enough to handle any reasoning type
        confidence = best_item.get('similarity', 0.5)
        
        # Adjust answer based on reasoning type
        if reasoning_type == 'example' and 'example' not in answer.lower():
            answer = f"Here's an example: {answer}"
        elif reasoning_type == 'comparison' and len(relevant_info) > 1:
            second_answer = relevant_info[1].get('answer', '')
            if second_answer and len(second_answer) > 20:
                answer = f"First aspect: {answer}\n\nSecond aspect: {second_answer}"
        
        return {
            'type': reasoning_type,
            'content': answer,
            'confidence': min(confidence + 0.2, 0.9)  # Boost confidence slightly
        }
    
    def _reason_definition(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for definition queries with comprehensive fallback"""
        print(f"[DEBUG] Definition reasoning - Info count: {len(info)}")
        
        if info:
            for i, item in enumerate(info):
                print(f"[DEBUG] Info {i}: {item.get('question', 'No question')[:50]}...")
                print(f"[DEBUG] Answer length: {len(item.get('answer', ''))}")
        
        if not info:
            print(f"[DEBUG] No info provided for concepts: {concepts}")
            return {
                'type': 'definition', 
                'content': f"I don't have specific information about {', '.join(concepts[:3])} in my current knowledge base. Could you try rephrasing your question?",
                'confidence': 0.2
            }
        
        # Get the best match
        best_match = info[0]
        answer = best_match.get('answer', '')
        
        print(f"[DEBUG] Best match answer preview: {answer[:100]}...")
        
        if answer and len(answer.strip()) > 10:
            print(f"[DEBUG] Using best match answer")
            return {
                'type': 'definition',
                'content': answer,
                'confidence': min(best_match.get('similarity', 0.7), 0.9)
            }
        
        # Fallback: try to find any good answer
        for item in info:
            answer = item.get('answer', '')
            if answer and len(answer.strip()) > 10:
                print(f"[DEBUG] Using fallback answer from item")
                return {
                    'type': 'definition',
                    'content': answer,
                    'confidence': 0.6
                }
        
        # Last resort
        print(f"[DEBUG] Using last resort response")
        return {
            'type': 'definition',
            'content': f"I found some information about {', '.join(concepts[:2])}, but the details are unclear. This appears to be related to {best_match.get('topic', 'psychology')}.",
            'confidence': 0.3
        }
    
    def _reason_comparison(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for comparison queries"""
        print(f"Comparison reasoning - Info count: {len(info)}")
        
        if len(info) < 2:
            if len(info) == 1:
                return {
                    'type': 'comparison', 
                    'content': f"I found information about one aspect: {info[0].get('answer', '')}\n\nHowever, I need more information to make a complete comparison.",
                    'confidence': 0.4
                }
            return {
                'type': 'comparison', 
                'content': "I need more information to make a comparison. Could you be more specific about what you'd like to compare?",
                'confidence': 0.2
            }
        
        # Find items related to different concepts
        comparison_text = f"Here's a comparison:\n\n"
        
        for i, item in enumerate(info[:2]):
            answer = item.get('answer', '')
            if answer:
                comparison_text += f"**Aspect {i+1}:** {answer}\n\n"
        
        return {
            'type': 'comparison',
            'content': comparison_text,
            'confidence': np.mean([item.get('similarity', 0.5) for item in info[:2]])
        }
    
    def _reason_causation(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for causation queries"""
        print(f"Causation reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'causation', 
                'content': f"I don't have specific information about the causes related to {', '.join(concepts[:3])}. Could you provide more context?",
                'confidence': 0.2
            }
        
        # Look for causal explanations
        causal_info = []
        for item in info:
            answer = item.get('answer', '')
            if answer and any(word in answer.lower() for word in ['because', 'cause', 'reason', 'due to', 'leads to', 'results in']):
                causal_info.append(answer)
        
        if causal_info:
            content = causal_info[0]
            confidence = 0.7
        else:
            # Use the best available answer even if it doesn't explicitly mention causation
            content = info[0].get('answer', '')
            confidence = 0.5
        
        if not content:
            content = f"This relates to {info[0].get('topic', 'psychology')}, but I need more specific information about the causal relationships."
            confidence = 0.3
        
        return {
            'type': 'causation',
            'content': content,
            'confidence': confidence
        }
    
    def _reason_process(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for process queries with better handling"""
        print(f"Process reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'process', 
                'content': f"I don't have specific information about the process related to {', '.join(concepts[:3])}. Could you provide more details?",
                'confidence': 0.2
            }
        
        # Look for process descriptions
        best_match = info[0]
        answer = best_match.get('answer', '')
        
        if answer and len(answer.strip()) > 10:
            return {
                'type': 'process',
                'content': answer,
                'confidence': best_match.get('similarity', 0.6)
            }
        
        return {
            'type': 'process',
            'content': f"This process relates to {best_match.get('topic', 'psychology')} but I need more specific information to explain the detailed steps.",
            'confidence': 0.3
        }
    
    def _reason_example(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for example queries with better responses"""
        print(f"Example reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'example', 
                'content': f"I don't have specific examples of {', '.join(concepts[:3])} in my knowledge base. Could you ask about a more specific topic?",
                'confidence': 0.2
            }
        
        # Generate examples based on available information
        examples = []
        for item in info[:3]:
            answer = item.get('answer', '')
            if answer and len(answer.strip()) > 10:
                # Extract or create example from the answer
                if 'example' in answer.lower() or 'such as' in answer.lower() or 'for instance' in answer.lower():
                    examples.append(answer)
                else:
                    # Use the answer as an example context
                    examples.append(f"In {item.get('topic', 'psychology')}: {answer}")
        
        if examples:
            if len(examples) == 1:
                content = f"Here's an example: {examples[0]}"
            else:
                content = f"Here are some examples:\n\n1. {examples[0]}"
                if len(examples) > 1:
                    content += f"\n\n2. {examples[1]}"
        else:
            content = f"While I have information about {', '.join(concepts[:2])}, I don't have specific examples readily available."
        
        return {
            'type': 'example',
            'content': content,
            'confidence': 0.6 if examples else 0.3
        }
    
    def _reason_application(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for application queries"""
        print(f"Application reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'application', 
                'content': f"I don't have specific information about practical applications of {', '.join(concepts[:3])}. Could you be more specific?",
                'confidence': 0.2
            }
        
        # Focus on practical aspects
        best_match = info[0]
        answer = best_match.get('answer', '')
        
        if answer and len(answer.strip()) > 10:
            application_text = f"Practical applications: {answer}"
            
            # Look for additional practical information
            for item in info[1:3]:
                additional_answer = item.get('answer', '')
                if additional_answer and 'practical' in additional_answer.lower() or 'apply' in additional_answer.lower():
                    application_text += f"\n\nAdditionally: {additional_answer}"
                    break
            
            return {
                'type': 'application',
                'content': application_text,
                'confidence': best_match.get('similarity', 0.6)
            }
        
        return {
            'type': 'application',
            'content': f"This relates to {best_match.get('topic', 'psychology')}, but I need more information about specific practical applications.",
            'confidence': 0.3
        }
    
    def _reason_analysis(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """Reasoning for analysis queries"""
        print(f"Analysis reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'analysis', 
                'content': f"I don't have enough information to provide an analysis of {', '.join(concepts[:3])}. Could you provide more context?",
                'confidence': 0.2
            }
        
        # Synthesize information from multiple sources
        analysis_parts = []
        
        for item in info[:3]:
            answer = item.get('answer', '')
            if answer and len(answer.strip()) > 10:
                analysis_parts.append(answer)
        
        if analysis_parts:
            if len(analysis_parts) == 1:
                analysis_text = f"Analysis: {analysis_parts[0]}"
            else:
                analysis_text = f"Analysis:\n\n"
                for i, part in enumerate(analysis_parts):
                    analysis_text += f"**Point {i+1}:** {part}\n\n"
            
            return {
                'type': 'analysis',
                'content': analysis_text,
                'confidence': np.mean([item.get('similarity', 0.5) for item in info[:len(analysis_parts)]])
            }
        
        return {
            'type': 'analysis',
            'content': f"I found some information related to {', '.join(concepts[:2])}, but need more details to provide a comprehensive analysis.",
            'confidence': 0.3
        }
    
    def _reason_general(self, query: str, concepts: List[str], info: List[Dict]) -> Dict:
        """General reasoning with robust fallback"""
        print(f"General reasoning - Info count: {len(info)}")
        
        if not info:
            return {
                'type': 'general', 
                'content': f"I don't have specific information about {', '.join(concepts[:3])} in my current knowledge base. Could you try rephrasing your question or asking about a related psychology topic?",
                'confidence': 0.2
            }
        
        # Use the best available information
        best_match = info[0]
        answer = best_match.get('answer', '')
        
        if answer and len(answer.strip()) > 10:
            return {
                'type': 'general',
                'content': answer,
                'confidence': best_match.get('similarity', 0.6)
            }
        
        # Try to find any usable answer from the results
        for item in info:
            answer = item.get('answer', '')
            if answer and len(answer.strip()) > 10:
                return {
                    'type': 'general',
                    'content': answer,
                    'confidence': item.get('similarity', 0.5)
                }
        
        return {
            'type': 'general',
            'content': f"I found some information related to {', '.join(concepts[:2])}, but the details are not clear enough to provide a complete answer. This topic relates to {best_match.get('topic', 'psychology')}.",
            'confidence': 0.3
        }
    
    def _generate_response(self, reasoning_result: Dict, reasoning_type: str) -> str:
        """Generate human-like response with improved formatting"""
        content = reasoning_result.get('content', 'I apologize, but I need more information to answer your question.')
        confidence = reasoning_result.get('confidence', 0.5)
        
        # Remove redundant prefixes and just return the content
        # The old system was adding confusing prefixes
        return content