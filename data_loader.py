"""
Data Loading and Preprocessing for Psych-101 Dataset
"""
import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Tuple, Optional

class DataLoader:
    def __init__(self):
        self.dataset = None
        self.processed_data = []
        self.psychology_concepts = {}
        
    def load_psych_dataset(self) -> bool:
        """Load Psych-101 dataset - using comprehensive fallback data"""
        print("Creating comprehensive psychology dataset...")
        self._create_comprehensive_data()
        return True
    
    def _create_comprehensive_data(self):
        """Create comprehensive psychology data that covers MORE topics and variations"""
        # Comprehensive psychology questions and answers - EXPANDED
        psychology_data = [
            # Classical/Operant Conditioning
            {
                'question': 'What is classical conditioning?',
                'answer': 'Classical conditioning is a learning process discovered by Ivan Pavlov where a neutral stimulus becomes associated with a meaningful stimulus, eventually triggering a conditioned response. For example, a bell (neutral stimulus) paired with food (meaningful stimulus) can eventually cause salivation (conditioned response) even without food.',
                'topic': 'Learning',
                'difficulty': 'basic'
            },
            {
                'question': 'What is operant conditioning?',
                'answer': 'Operant conditioning is a learning method developed by B.F. Skinner where behavior is modified through consequences. Positive reinforcement adds something pleasant, negative reinforcement removes something unpleasant, punishment decreases behavior likelihood.',
                'topic': 'Learning',
                'difficulty': 'basic'
            },
            {
                'question': 'How does reinforcement work?',
                'answer': 'Reinforcement increases the likelihood of a behavior being repeated. Positive reinforcement adds a pleasant stimulus (like praise or rewards), while negative reinforcement removes an unpleasant stimulus (like stopping annoying noise when you buckle your seatbelt).',
                'topic': 'Learning',
                'difficulty': 'basic'
            },
            {
                'question': 'What is punishment in psychology?',
                'answer': 'Punishment decreases the likelihood of a behavior being repeated. Positive punishment adds an unpleasant consequence (like a fine for speeding), while negative punishment removes something pleasant (like taking away video games).',
                'topic': 'Learning',
                'difficulty': 'basic'
            },
            
            # Memory
            {
                'question': 'How does memory work?',
                'answer': 'Memory involves three main processes: encoding (taking in information), storage (maintaining information over time), and retrieval (accessing stored information). Information typically moves from sensory memory to short-term memory to long-term memory through attention and rehearsal.',
                'topic': 'Memory',
                'difficulty': 'basic'
            },
            {
                'question': 'What is short-term memory?',
                'answer': 'Short-term memory is a temporary storage system that holds information for about 15-30 seconds with a limited capacity of 7±2 items. It acts as a workspace for conscious thinking and can be extended through rehearsal.',
                'topic': 'Memory',
                'difficulty': 'basic'
            },
            {
                'question': 'What is long-term memory?',
                'answer': 'Long-term memory is the permanent storage system with virtually unlimited capacity. It includes declarative memory (facts and events) and procedural memory (skills and habits). Information can be stored here indefinitely.',
                'topic': 'Memory',
                'difficulty': 'basic'
            },
            {
                'question': 'How does stress affect memory?',
                'answer': 'Moderate stress can enhance memory formation by releasing hormones like cortisol that improve attention and encoding. However, chronic or extreme stress impairs memory by damaging the hippocampus and interfering with retrieval processes.',
                'topic': 'Memory',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is forgetting?',
                'answer': 'Forgetting is the inability to retrieve previously stored information. It can result from decay over time, interference from other memories, retrieval failure, or motivated forgetting where painful memories are suppressed.',
                'topic': 'Memory',
                'difficulty': 'basic'
            },
            
            # Cognitive Psychology
            {
                'question': 'What is cognitive dissonance?',
                'answer': 'Cognitive dissonance is the mental discomfort experienced when holding contradictory beliefs, values, or attitudes simultaneously. People reduce this dissonance by changing their beliefs, acquiring new information, or reducing the importance of the conflicting cognitions.',
                'topic': 'Cognition',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What are cognitive biases?',
                'answer': 'Cognitive biases are systematic errors in thinking that affect decisions and judgments. Examples include confirmation bias (seeking confirming evidence), availability heuristic (overestimating memorable events), and anchoring bias (relying too heavily on first information received).',
                'topic': 'Cognitive Biases',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is confirmation bias?',
                'answer': 'Confirmation bias is the tendency to search for, interpret, and recall information that confirms pre-existing beliefs while ignoring contradictory evidence. This leads to flawed decision-making, polarized thinking, and resistance to changing opinions even when presented with strong opposing evidence.',
                'topic': 'Cognitive Biases',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is attention?',
                'answer': 'Attention is the cognitive process of selectively focusing on specific information while ignoring other stimuli. It has limited capacity and can be divided (multitasking), sustained (concentration), or selective (filtering). Attention is crucial for perception, memory, and learning.',
                'topic': 'Cognition',
                'difficulty': 'basic'
            },
            {
                'question': 'What is perception?',
                'answer': 'Perception is the process of organizing and interpreting sensory information to understand our environment. It involves both bottom-up processing (data-driven) and top-down processing (knowledge-driven), and can be influenced by expectations, culture, and past experiences.',
                'topic': 'Cognition',
                'difficulty': 'basic'
            },
            
            # Emotions
            {
                'question': 'What are the stages of grief?',
                'answer': 'According to Elisabeth Kübler-Ross, the five stages of grief are: Denial (refusing to accept the loss), Anger (frustration and rage), Bargaining (attempting to postpone the inevitable), Depression (sadness and despair), and Acceptance (coming to terms with the reality).',
                'topic': 'Emotion',
                'difficulty': 'basic'
            },
            {
                'question': 'What is the difference between anxiety and fear?',
                'answer': 'Fear is an immediate emotional response to a specific, identifiable threat that triggers fight-or-flight response. Anxiety is a more general, persistent feeling of apprehension about potential future threats, often without a specific identifiable source.',
                'topic': 'Emotion',
                'difficulty': 'basic'
            },
            {
                'question': 'What causes anxiety?',
                'answer': 'Anxiety can be caused by biological factors (genetics, brain chemistry), psychological factors (personality, thinking patterns), environmental factors (stress, trauma), or medical conditions. It often results from a combination of multiple factors rather than a single cause.',
                'topic': 'Emotion',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is depression?',
                'answer': 'Depression is a mood disorder characterized by persistent feelings of sadness, hopelessness, and loss of interest in activities. Symptoms include changes in sleep, appetite, energy, concentration, and may include thoughts of death or suicide. It affects how you think, feel, and behave.',
                'topic': 'Emotion',
                'difficulty': 'basic'
            },
            {
                'question': 'How do emotions work?',
                'answer': 'Emotions involve physiological arousal, cognitive interpretation, and behavioral expression. The limbic system, especially the amygdala, processes emotions quickly while the prefrontal cortex provides rational evaluation. Emotions serve adaptive functions like motivation and communication.',
                'topic': 'Emotion',
                'difficulty': 'intermediate'
            },
            
            # Motivation
            {
                'question': 'What is intrinsic motivation?',
                'answer': 'Intrinsic motivation is the drive to engage in activities for their inherent satisfaction rather than external rewards. It comes from internal factors like personal interest, enjoyment, curiosity, and the satisfaction of mastering new skills.',
                'topic': 'Motivation',
                'difficulty': 'basic'
            },
            {
                'question': 'What is extrinsic motivation?',
                'answer': 'Extrinsic motivation is the drive to perform activities to earn external rewards or avoid punishments. Examples include working for money, studying for grades, or exercising to lose weight rather than for enjoyment.',
                'topic': 'Motivation',
                'difficulty': 'basic'
            },
            {
                'question': 'What motivates human behavior?',
                'answer': 'Human behavior is motivated by basic needs (food, safety, belonging), psychological needs (autonomy, competence, relatedness), goals, values, emotions, and social influences. Motivation can be conscious or unconscious, and varies greatly between individuals.',
                'topic': 'Motivation',
                'difficulty': 'intermediate'
            },
            
            # Social Psychology
            {
                'question': 'What is social learning theory?',
                'answer': 'Social learning theory by Albert Bandura explains that people learn behaviors by observing others. The process includes attention to the model, retention of the observed behavior, reproduction of the behavior, and motivation to perform it. The famous Bobo doll experiment demonstrated this.',
                'topic': 'Learning',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is conformity?',
                'answer': 'Conformity is the tendency to adjust behavior, attitudes, or beliefs to match those of a group or social norm. It can result from normative influence (desire to be accepted) or informational influence (desire to be correct). Asch\'s line experiments famously demonstrated this.',
                'topic': 'Social Psychology',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is obedience?',
                'answer': 'Obedience is compliance with orders or instructions from an authority figure. Milgram\'s shock experiments showed that people will often obey authority even when it conflicts with their moral beliefs, highlighting the power of situational factors over personal disposition.',
                'topic': 'Social Psychology',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is groupthink?',
                'answer': 'Groupthink is a psychological phenomenon where the desire for group harmony results in poor decision-making. Members suppress dissent, fail to critically analyze alternatives, and isolate themselves from contrary opinions, leading to flawed judgments.',
                'topic': 'Social Psychology',
                'difficulty': 'advanced'
            },
            
            # Development
            {
                'question': 'What are Piaget stages of development?',
                'answer': 'Piaget identified four stages of cognitive development: Sensorimotor (0-2 years) with object permanence, Preoperational (2-7 years) with symbolic thinking, Concrete Operational (7-11 years) with logical thinking about concrete objects, and Formal Operational (11+ years) with abstract reasoning.',
                'topic': 'Development',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is attachment theory?',
                'answer': 'Attachment theory describes the emotional bonds between children and caregivers. Secure attachment develops when caregivers are responsive and consistent, while insecure attachment (anxious, avoidant, or disorganized) results from inconsistent or unresponsive caregiving.',
                'topic': 'Development',
                'difficulty': 'intermediate'
            },
            
            # Health Psychology
            {
                'question': 'What is the placebo effect?',
                'answer': 'The placebo effect occurs when a person experiences real improvement in symptoms after receiving an inactive treatment, simply because they believe it will help. This demonstrates the powerful connection between mind and body, and the role of expectation in healing.',
                'topic': 'Health Psychology',
                'difficulty': 'basic'
            },
            {
                'question': 'How does sleep affect learning?',
                'answer': 'Sleep plays a crucial role in memory consolidation, transferring information from short-term to long-term memory. During sleep, the brain strengthens neural connections formed during learning, clears metabolic waste, and integrates new information with existing knowledge.',
                'topic': 'Memory',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is stress?',
                'answer': 'Stress is the body\'s response to perceived threats or challenges. It involves physiological changes (increased heart rate, cortisol release) and psychological responses. While acute stress can be helpful, chronic stress can harm physical and mental health.',
                'topic': 'Health Psychology',
                'difficulty': 'basic'
            },
            
            # Personality
            {
                'question': 'What is personality?',
                'answer': 'Personality refers to characteristic patterns of thoughts, feelings, and behaviors that make a person unique. It\'s relatively stable over time and influences how people interact with their environment. Major theories include trait theories, psychodynamic theories, and humanistic approaches.',
                'topic': 'Personality',
                'difficulty': 'basic'
            },
            {
                'question': 'What are the Big Five personality traits?',
                'answer': 'The Big Five personality traits are: Openness (creativity, curiosity), Conscientiousness (organization, discipline), Extraversion (sociability, energy), Agreeableness (cooperation, trust), and Neuroticism (emotional instability, anxiety). These traits are relatively stable and predict behavior across situations.',
                'topic': 'Personality',
                'difficulty': 'intermediate'
            },
            
            # Therapy and Treatment
            {
                'question': 'What is cognitive behavioral therapy?',
                'answer': 'Cognitive Behavioral Therapy (CBT) is a form of psychotherapy that focuses on identifying and changing negative thought patterns and behaviors. It\'s based on the idea that thoughts, feelings, and behaviors are interconnected, and changing one can affect the others.',
                'topic': 'Therapy',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is psychoanalysis?',
                'answer': 'Psychoanalysis is a therapeutic approach developed by Sigmund Freud that focuses on unconscious conflicts and childhood experiences. It uses techniques like free association and dream analysis to bring unconscious material to consciousness and resolve psychological conflicts.',
                'topic': 'Therapy',
                'difficulty': 'intermediate'
            },
            
            # Research Methods
            {
                'question': 'What is the scientific method in psychology?',
                'answer': 'The scientific method in psychology involves systematic observation, hypothesis formation, experimental testing, and peer review. It includes controlled experiments, correlational studies, case studies, and naturalistic observation to understand behavior and mental processes objectively.',
                'topic': 'Research Methods',
                'difficulty': 'intermediate'
            },
            {
                'question': 'What is correlation vs causation?',
                'answer': 'Correlation means two variables are related or associated, but doesn\'t prove that one causes the other. Causation means one variable directly influences another. Many correlations are coincidental or due to third variables, so experiments are needed to establish causation.',
                'topic': 'Research Methods',
                'difficulty': 'intermediate'
            }
        ]
        
        # Convert to dataset-like structure
        class MockDataset:
            def __init__(self, data):
                self.data = {'train': data}
            def __getitem__(self, key):
                return self.data[key]
            def keys(self):
                return self.data.keys()
        
        self.dataset = MockDataset(psychology_data)
        print(f"Created dataset with {len(psychology_data)} psychology items")
    
    def preprocess_data(self) -> List[Dict]:
        """Preprocess the loaded data"""
        processed = []
        
        try:
            if 'train' in self.dataset.keys():
                data_split = self.dataset['train']
            else:
                data_split = list(self.dataset.values())[0]
            
            print(f"Processing {len(data_split)} items...")
            
            for i, item in enumerate(data_split):
                processed_item = self._process_item(item)
                if processed_item:
                    processed.append(processed_item)
                    if i < 3:  # Debug first few items
                        print(f"Processed item {i}: {processed_item['question'][:50]}...")
            
            self.processed_data = processed
            print(f"Successfully processed {len(processed)} items")
            
        except Exception as e:
            print(f"Error preprocessing data: {e}")
            import traceback
            traceback.print_exc()
        
        return processed
    
    def _process_item(self, item: Dict) -> Optional[Dict]:
        """Process individual data item with better concept extraction"""
        try:
            # Extract key information
            question = item.get('question', '')
            answer = item.get('answer', '')
            topic = item.get('topic', 'General')
            difficulty = item.get('difficulty', 'basic')
            
            if not question or not answer:
                print(f"Skipping item with missing question or answer")
                return None
            
            # Clean text
            question_clean = self._clean_text(question)
            answer_clean = self._clean_text(answer)
            
            # Extract concepts
            concepts = self._extract_concepts(question_clean + ' ' + answer_clean)
            
            # Tokenize
            question_tokens = self._tokenize(question_clean)
            answer_tokens = self._tokenize(answer_clean)
            
            result = {
                'question': question_clean,
                'answer': answer_clean,
                'topic': topic,
                'difficulty': difficulty,
                'concepts': concepts,
                'question_tokens': question_tokens,
                'answer_tokens': answer_tokens
            }
            
            return result
            
        except Exception as e:
            print(f"Error processing item: {e}")
            return None
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Preserve original text but clean minimally
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        if not text:
            return []
        
        # Split on whitespace and punctuation
        tokens = re.findall(r'\w+', text.lower())
        return tokens
    
    def _extract_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        if not text:
            return []
        
        # Key psychology terms
        psych_terms = [
            'classical', 'conditioning', 'operant', 'reinforcement', 'pavlov', 'skinner',
            'memory', 'learning', 'cognitive', 'dissonance', 'bias', 'stress',
            'anxiety', 'fear', 'grief', 'motivation', 'intrinsic', 'extrinsic',
            'behaviorism', 'placebo', 'social', 'theory', 'stages', 'sleep'
        ]
        
        found_concepts = []
        text_lower = text.lower()
        
        # Find psychology terms
        for term in psych_terms:
            if term in text_lower:
                found_concepts.append(term)
        
        # Add important words
        tokens = self._tokenize(text)
        for token in tokens:
            if (len(token) > 3 and 
                token not in found_concepts and 
                token not in ['this', 'that', 'they', 'them', 'their', 'with', 'from']):
                found_concepts.append(token)
        
        return list(set(found_concepts))[:15]  # Limit and deduplicate
    
    def get_stats(self) -> Dict:
        """Get dataset statistics"""
        if not self.processed_data:
            return {'total_items': 0}
        
        topics = [item['topic'] for item in self.processed_data]
        topic_counts = {topic: topics.count(topic) for topic in set(topics)}
        
        return {
            'total_items': len(self.processed_data),
            'topics': topic_counts,
            'sample_question': self.processed_data[0]['question'] if self.processed_data else None
        }