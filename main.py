"""
HYPERCENTAUR SYSTEM 

"""
import streamlit as st
import re
import time
from typing import Dict, List, Any

# COMPREHENSIVE PSYCHOLOGY DATABASE - BUILT IN
PSYCHOLOGY_DB = [
    {
        'keywords': ['classical', 'conditioning', 'pavlov', 'bell', 'neutral', 'stimulus'],
        'question': 'What is classical conditioning?',
        'answer': 'Classical conditioning is a learning process discovered by Ivan Pavlov where a neutral stimulus becomes associated with a meaningful stimulus, eventually triggering a conditioned response. For example, a bell (neutral stimulus) paired with food (meaningful stimulus) can eventually cause salivation (conditioned response) even without food.',
        'topic': 'Learning'
    },
    {
        'keywords': ['operant', 'conditioning', 'skinner', 'reinforcement', 'punishment', 'behavior'],
        'question': 'What is operant conditioning?',
        'answer': 'Operant conditioning is a learning method developed by B.F. Skinner where behavior is modified through consequences. Positive reinforcement adds something pleasant, negative reinforcement removes something unpleasant, punishment decreases behavior likelihood.',
        'topic': 'Learning'
    },
    {
        'keywords': ['memory', 'remember', 'forget', 'recall', 'brain', 'encoding', 'storage'],
        'question': 'How does memory work?',
        'answer': 'Memory involves three main processes: encoding (taking in information), storage (maintaining information over time), and retrieval (accessing stored information). Information moves from sensory memory to short-term memory to long-term memory through attention and rehearsal.',
        'topic': 'Memory'
    },
    {
        'keywords': ['brain', 'work', 'function', 'neural', 'neuron', 'mind'],
        'question': 'How does the brain work?',
        'answer': 'The brain processes information through networks of neurons that communicate via electrical and chemical signals. Different brain regions specialize in functions like memory (hippocampus), emotions (amygdala), and reasoning (prefrontal cortex). Neural plasticity allows the brain to adapt and form new connections throughout life.',
        'topic': 'Neuroscience'
    },
    {
        'keywords': ['stress', 'affect', 'memory', 'cortisol', 'pressure'],
        'question': 'How does stress affect memory?',
        'answer': 'Moderate stress can enhance memory formation by releasing hormones like cortisol that improve attention and encoding. However, chronic or extreme stress impairs memory by damaging the hippocampus and interfering with retrieval processes.',
        'topic': 'Memory'
    },
    {
        'keywords': ['cognitive', 'dissonance', 'conflict', 'beliefs', 'contradiction'],
        'question': 'What is cognitive dissonance?',
        'answer': 'Cognitive dissonance is the mental discomfort experienced when holding contradictory beliefs, values, or attitudes simultaneously. People reduce this dissonance by changing their beliefs, acquiring new information, or reducing the importance of the conflicting cognitions.',
        'topic': 'Cognition'
    },
    {
        'keywords': ['anxiety', 'fear', 'difference', 'worry', 'panic'],
        'question': 'What is the difference between anxiety and fear?',
        'answer': 'Fear is an immediate emotional response to a specific, identifiable threat that triggers fight-or-flight response. Anxiety is a more general, persistent feeling of apprehension about potential future threats, often without a specific identifiable source.',
        'topic': 'Emotion'
    },
    {
        'keywords': ['depression', 'sad', 'sadness', 'mood', 'mental', 'illness'],
        'question': 'What is depression?',
        'answer': 'Depression is a mood disorder characterized by persistent feelings of sadness, hopelessness, and loss of interest in activities. Symptoms include changes in sleep, appetite, energy, concentration, and may include thoughts of death or suicide. It affects how you think, feel, and behave.',
        'topic': 'Mental Health'
    },
    {
        'keywords': ['grief', 'stages', 'loss', 'death', 'kubler', 'ross'],
        'question': 'What are the stages of grief?',
        'answer': 'According to Elisabeth Kübler-Ross, the five stages of grief are: Denial (refusing to accept the loss), Anger (frustration and rage), Bargaining (attempting to postpone the inevitable), Depression (sadness and despair), and Acceptance (coming to terms with the reality).',
        'topic': 'Emotion'
    },
    {
        'keywords': ['social', 'learning', 'theory', 'bandura', 'observation', 'modeling'],
        'question': 'What is social learning theory?',
        'answer': 'Social learning theory by Albert Bandura explains that people learn behaviors by observing others. The process includes attention to the model, retention of the observed behavior, reproduction of the behavior, and motivation to perform it. The famous Bobo doll experiment demonstrated this.',
        'topic': 'Learning'
    },
    {
        'keywords': ['motivation', 'intrinsic', 'extrinsic', 'drive', 'goal'],
        'question': 'What motivates human behavior?',
        'answer': 'Human behavior is motivated by basic needs (food, safety, belonging), psychological needs (autonomy, competence, relatedness), goals, values, emotions, and social influences. Intrinsic motivation comes from internal satisfaction while extrinsic motivation comes from external rewards.',
        'topic': 'Motivation'
    },
    {
        'keywords': ['people', 'group', 'groups', 'crowd', 'conform', 'conformity'],
        'question': 'Why do people conform in groups?',
        'answer': 'People conform in groups due to normative influence (desire to be accepted and avoid rejection) and informational influence (assuming the group knows better). This can lead to groupthink, where the desire for harmony results in poor decision-making and suppression of dissent.',
        'topic': 'Social Psychology'
    },
    {
        'keywords': ['children', 'learn', 'development', 'kids', 'child', 'piaget'],
        'question': 'How do children learn and develop?',
        'answer': 'Children learn through exploration, observation, and interaction with their environment. Piaget identified stages: sensorimotor (0-2), preoperational (2-7), concrete operational (7-11), and formal operational (11+). Development involves cognitive, emotional, social, and physical growth.',
        'topic': 'Development'
    },
    {
        'keywords': ['therapy', 'treatment', 'help', 'counseling', 'mental', 'health'],
        'question': 'How does therapy help mental health?',
        'answer': 'Therapy helps by providing a safe space to explore thoughts and feelings, teaching coping strategies, identifying negative patterns, and developing healthier behaviors. Different approaches include cognitive-behavioral therapy (CBT), psychodynamic therapy, and humanistic therapy.',
        'topic': 'Therapy'
    },
    {
        'keywords': ['attention', 'focus', 'concentrate', 'mind', 'cognitive'],
        'question': 'How does attention work?',
        'answer': 'Attention is the cognitive process of selectively focusing on specific information while filtering out irrelevant stimuli. It has limited capacity and can be divided, sustained, or selective. The brain\'s attention networks involve the prefrontal cortex and parietal regions.',
        'topic': 'Cognition'
    },
    {
        'keywords': ['bias', 'cognitive', 'thinking', 'errors', 'judgment'],
        'question': 'What are cognitive biases?',
        'answer': 'Cognitive biases are systematic errors in thinking that affect decisions and judgments. Examples include confirmation bias (seeking information that confirms beliefs), availability heuristic (overestimating memorable events), and anchoring bias (over-relying on first information received).',
        'topic': 'Cognition'
    },
    {
        'keywords': ['personality', 'traits', 'character', 'individual', 'differences'],
        'question': 'What shapes personality?',
        'answer': 'Personality is shaped by genetics (temperament), environment (family, culture, experiences), and the interaction between them. The Big Five traits (openness, conscientiousness, extraversion, agreeableness, neuroticism) represent major personality dimensions that remain relatively stable over time.',
        'topic': 'Personality'
    },
    {
        'keywords': ['sleep', 'learning', 'memory', 'consolidation', 'brain'],
        'question': 'How does sleep affect learning?',
        'answer': 'Sleep is crucial for memory consolidation, transferring information from short-term to long-term memory. During sleep, the brain strengthens neural connections formed during learning, clears metabolic waste, and integrates new information with existing knowledge.',
        'topic': 'Memory'
    },
    {
        'keywords': ['emotions', 'feel', 'feelings', 'emotional', 'mood'],
        'question': 'How do emotions work?',
        'answer': 'Emotions involve physiological arousal, cognitive interpretation, and behavioral expression. The limbic system, especially the amygdala, processes emotions quickly while the prefrontal cortex provides rational evaluation. Emotions serve adaptive functions like motivation, communication, and survival.',
        'topic': 'Emotion'
    },
    {
        'keywords': ['placebo', 'effect', 'mind', 'body', 'belief', 'expectation'],
        'question': 'What is the placebo effect?',
        'answer': 'The placebo effect occurs when a person experiences real improvement in symptoms after receiving an inactive treatment, simply because they believe it will help. This demonstrates the powerful connection between mind and body, and the role of expectation in healing.',
        'topic': 'Health Psychology'
    },
    # NEW ENTRIES - 15 MORE COMPREHENSIVE PSYCHOLOGY TOPICS
    {
        'keywords': ['freud', 'psychoanalysis', 'unconscious', 'ego', 'superego', 'id'],
        'question': 'What is Freudian psychoanalysis?',
        'answer': 'Freudian psychoanalysis is a therapeutic approach that explores unconscious conflicts and childhood experiences. Freud proposed that personality consists of three parts: the id (basic desires), ego (reality principle), and superego (moral conscience). Treatment involves techniques like free association and dream analysis to bring unconscious material to consciousness.',
        'topic': 'Psychoanalysis'
    },
    {
        'keywords': ['schizophrenia', 'psychosis', 'hallucinations', 'delusions', 'mental'],
        'question': 'What is schizophrenia?',
        'answer': 'Schizophrenia is a chronic mental disorder characterized by delusions, hallucinations, disorganized thinking, and abnormal motor behavior. It typically emerges in late teens or early twenties and affects about 1% of the population. Treatment involves antipsychotic medications and psychosocial interventions.',
        'topic': 'Mental Health'
    },
    {
        'keywords': ['autism', 'spectrum', 'disorder', 'communication', 'social', 'repetitive'],
        'question': 'What is autism spectrum disorder?',
        'answer': 'Autism spectrum disorder (ASD) is a developmental condition characterized by challenges in social communication, restricted interests, and repetitive behaviors. Symptoms range from mild to severe, hence the term "spectrum." Early intervention with behavioral and educational therapies can significantly improve outcomes.',
        'topic': 'Development'
    },
    {
        'keywords': ['ptsd', 'trauma', 'flashbacks', 'stress', 'disorder', 'war'],
        'question': 'What is PTSD?',
        'answer': 'Post-Traumatic Stress Disorder (PTSD) is a mental health condition triggered by experiencing or witnessing a terrifying event. Symptoms include flashbacks, nightmares, severe anxiety, and intrusive thoughts about the event. Treatment includes trauma-focused therapy and sometimes medication.',
        'topic': 'Mental Health'
    },
    {
        'keywords': ['addiction', 'substance', 'dependence', 'drugs', 'alcohol', 'brain'],
        'question': 'How does addiction affect the brain?',
        'answer': 'Addiction hijacks the brain\'s reward system, particularly affecting dopamine pathways in areas like the nucleus accumbens. Repeated substance use creates tolerance, requiring more to achieve the same effect. The brain adapts to the presence of substances, leading to withdrawal symptoms when use stops.',
        'topic': 'Neuroscience'
    },
    {
        'keywords': ['intelligence', 'iq', 'smart', 'cognitive', 'ability', 'test'],
        'question': 'What is intelligence and how is it measured?',
        'answer': 'Intelligence is the ability to learn, reason, solve problems, and adapt to new situations. It\'s commonly measured through IQ tests that assess various cognitive abilities. However, theories like Gardner\'s multiple intelligences suggest there are different types of intelligence beyond what traditional tests measure.',
        'topic': 'Cognition'
    },
    {
        'keywords': ['twins', 'nature', 'nurture', 'genetics', 'environment', 'behavior'],
        'question': 'What is the nature vs nurture debate?',
        'answer': 'The nature vs nurture debate examines whether human behavior is determined by genetics (nature) or environment (nurture). Twin studies show that most traits result from both genetic predispositions and environmental influences. Modern psychology recognizes that genes and environment interact in complex ways.',
        'topic': 'Development'
    },
    {
        'keywords': ['dreams', 'sleep', 'rem', 'unconscious', 'symbolism', 'freud'],
        'question': 'Why do we dream and what do dreams mean?',
        'answer': 'Dreams occur primarily during REM sleep and may serve functions like memory consolidation, emotional processing, and problem-solving. While Freud believed dreams revealed unconscious desires, modern research suggests they help the brain process information and experiences from waking life.',
        'topic': 'Sleep Psychology'
    },
    {
        'keywords': ['love', 'attachment', 'relationships', 'bonding', 'romantic', 'oxytocin'],
        'question': 'What is the psychology of love?',
        'answer': 'Love involves complex psychological and neurochemical processes. Attachment theory identifies different love styles based on early relationships. Neurochemically, love involves hormones like oxytocin, dopamine, and serotonin. Sternberg\'s triangular theory describes love as having three components: intimacy, passion, and commitment.',
        'topic': 'Social Psychology'
    },
    {
        'keywords': ['phobia', 'fear', 'irrational', 'panic', 'specific', 'treatment'],
        'question': 'What are phobias and how are they treated?',
        'answer': 'Phobias are irrational, intense fears of specific objects or situations that cause significant distress and avoidance. They often develop through classical conditioning or traumatic experiences. Treatment typically involves exposure therapy, where patients gradually face their fears in a controlled, safe environment.',
        'topic': 'Mental Health'
    },
    {
        'keywords': ['eating', 'disorder', 'anorexia', 'bulimia', 'food', 'body'],
        'question': 'What causes eating disorders?',
        'answer': 'Eating disorders like anorexia and bulimia result from complex interactions of genetic, psychological, and sociocultural factors. Risk factors include perfectionism, low self-esteem, trauma, cultural pressure for thinness, and family history. Treatment involves nutritional rehabilitation, therapy, and addressing underlying psychological issues.',
        'topic': 'Mental Health'
    },
    {
        'keywords': ['meditation', 'mindfulness', 'stress', 'reduction', 'brain', 'buddhism'],
        'question': 'How does meditation affect the brain?',
        'answer': 'Meditation produces measurable changes in brain structure and function. Regular practice increases gray matter in areas associated with attention and emotional regulation, while decreasing activity in the amygdala (fear center). It reduces stress hormones and promotes neuroplasticity.',
        'topic': 'Health Psychology'
    },
    {
        'keywords': ['color', 'psychology', 'perception', 'mood', 'behavior', 'influence'],
        'question': 'How do colors affect psychology and behavior?',
        'answer': 'Colors can influence mood, behavior, and physiological responses through both biological and learned associations. Red can increase arousal and urgency, blue promotes calmness and trust, while green is associated with nature and relaxation. Cultural factors also play a significant role in color perception.',
        'topic': 'Perception'
    },
    {
        'keywords': ['adolescence', 'teenager', 'puberty', 'development', 'brain', 'identity'],
        'question': 'What happens during adolescent development?',
        'answer': 'Adolescence involves dramatic physical, cognitive, and social changes. The teenage brain undergoes significant development, particularly in the prefrontal cortex responsible for decision-making. This period includes identity formation, increased risk-taking, emotional intensity, and developing independence from parents.',
        'topic': 'Development'
    },
    {
        'keywords': ['happiness', 'positive', 'psychology', 'wellbeing', 'life', 'satisfaction'],
        'question': 'What makes people happy according to psychology?',
        'answer': 'Positive psychology research shows happiness comes from multiple factors: positive relationships, engagement in meaningful activities, accomplishment, positive emotions, and meaning/purpose in life. Genetics accounts for about 50% of happiness, with circumstances and intentional activities making up the rest.',
        'topic': 'Positive Psychology'
    }
]

class SimpleHypercentaur:
    def __init__(self):
        self.query_history = []
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Simple but effective query processing"""
        if not query or len(query.strip()) < 3:
            return {
                'response': "Please ask a question about psychology, mental health, learning, memory, or human behavior.",
                'confidence': 0.1,
                'success': False
            }
        
        # Clean and extract keywords from query
        query_clean = query.lower().strip()
        query_words = self._extract_keywords(query_clean)
        
        print(f"Query: '{query_clean}'")
        print(f"Keywords: {query_words}")
        
        # Find best matching entry
        best_match = self._find_best_match(query_words)
        
        if best_match:
            response = {
                'response': best_match['answer'],
                'confidence': best_match['confidence'],
                'success': True,
                'topic': best_match['topic'],
                'matched_question': best_match['question'],
                'matched_keywords': best_match['matched_keywords']
            }
            
            # Store in history
            self.query_history.append({
                'query': query,
                'response': response
            })
            
            return response
        else:
            # This should rarely happen with our comprehensive database
            return {
                'response': "I have knowledge about psychology, learning, memory, emotions, cognition, social behavior, development, personality, and therapy. Could you ask about a specific topic in these areas?",
                'confidence': 0.2,
                'success': True
            }
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract meaningful keywords from query"""
        # Remove common words
        stop_words = {'what', 'is', 'how', 'does', 'do', 'why', 'when', 'where', 'who', 
                     'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                     'for', 'of', 'with', 'by', 'can', 'will', 'would', 'could', 'should'}
        
        # Extract words
        words = re.findall(r'\b\w+\b', query.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords
    
    def _find_best_match(self, query_keywords: List[str]) -> Dict[str, Any]:
        """Find the best matching psychology entry - FIXED TO ACTUALLY WORK"""
        best_score = 0
        best_entry = None
        
        print(f"\n=== MATCHING PROCESS ===")
        print(f"Query keywords: {query_keywords}")
        
        for i, entry in enumerate(PSYCHOLOGY_DB):
            score = 0
            matched_keywords = []
            
            print(f"\nChecking entry {i+1}: {entry['question']}")
            print(f"Entry keywords: {entry['keywords']}")
            
            # METHOD 1: Exact keyword matches (highest score)
            for query_kw in query_keywords:
                for entry_kw in entry['keywords']:
                    if query_kw.lower() == entry_kw.lower():
                        score += 20
                        matched_keywords.append(query_kw)
                        print(f"  EXACT match: '{query_kw}' = '{entry_kw}' (+20)")
            
            # METHOD 2: Partial keyword matches (medium score)
            for query_kw in query_keywords:
                for entry_kw in entry['keywords']:
                    if query_kw.lower() in entry_kw.lower() or entry_kw.lower() in query_kw.lower():
                        if query_kw not in matched_keywords:  # Don't double count
                            score += 10
                            matched_keywords.append(query_kw)
                            print(f"  PARTIAL match: '{query_kw}' ~ '{entry_kw}' (+10)")
            
            # METHOD 3: Question text matches (medium score)
            question_lower = entry['question'].lower()
            for query_kw in query_keywords:
                if query_kw.lower() in question_lower:
                    if query_kw not in matched_keywords:  # Don't double count
                        score += 8
                        matched_keywords.append(query_kw)
                        print(f"  QUESTION match: '{query_kw}' in question (+8)")
            
            # METHOD 4: Answer text matches (low score)
            answer_lower = entry['answer'].lower()
            for query_kw in query_keywords:
                if query_kw.lower() in answer_lower:
                    if query_kw not in matched_keywords:  # Don't double count
                        score += 3
                        matched_keywords.append(query_kw)
                        print(f"  ANSWER match: '{query_kw}' in answer (+3)")
            
            # Bonus for multiple matches
            if len(matched_keywords) > 1:
                bonus = len(matched_keywords) * 5
                score += bonus
                print(f"  MULTI-MATCH bonus: {len(matched_keywords)} matches (+{bonus})")
            
            print(f"  TOTAL SCORE: {score}")
            
            if score > best_score:
                best_score = score
                best_entry = {
                    'question': entry['question'],
                    'answer': entry['answer'],
                    'topic': entry['topic'],
                    'confidence': min(score / 30.0, 0.95),  # Convert to confidence (max 0.95)
                    'matched_keywords': list(set(matched_keywords)),  # Remove duplicates
                    'raw_score': score
                }
                print(f"  >>> NEW BEST MATCH! <<<")
        
        print(f"\n=== FINAL RESULT ===")
        if best_entry:
            print(f"Selected: {best_entry['question']}")
            print(f"Score: {best_entry['raw_score']}")
            print(f"Confidence: {best_entry['confidence']:.2f}")
            print(f"Matched keywords: {best_entry['matched_keywords']}")
        else:
            print("NO MATCHES FOUND")
        
        return best_entry
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'total_entries': len(PSYCHOLOGY_DB),
            'total_queries': len(self.query_history),
            'topics': list(set(entry['topic'] for entry in PSYCHOLOGY_DB))
        }

def typewriter_effect(text: str, container, delay: float = 0.03):
    """Create a typewriter effect for displaying text"""
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(displayed_text)
        time.sleep(delay)

def simulate_thinking():
    """Simulate AI thinking process"""
    thinking_messages = [
        "🤔 Analyzing your question...",
        "🧠 Searching knowledge database...",
        "🔍 Finding best match...",
        "💡 Preparing response..."
    ]
    
    thinking_container = st.empty()
    
    for i, message in enumerate(thinking_messages):
        thinking_container.info(f"**Step {i+1}/4:** {message}")
        time.sleep(0.8)
    
    thinking_container.empty()

# STREAMLIT APP
def main():
    st.set_page_config(
        page_title="Hypercentaur - Simple & Working",
        page_icon="🧠",
        layout="wide"
    )
    
    # Custom CSS for styling and footer
    st.markdown("""
    <style>
        .main-header {
            text-align: center;
            color: #000000;
            margin-bottom: 2rem;
        }
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f0f2f6;
            color: #262730;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #e6e9ef;
            z-index: 999;
        }
        .footer-text {
            font-size: 14px;
            margin: 0;
        }
        .love-icon {
            color: #e74c3c;
            animation: heartbeat 1.5s ease-in-out infinite;
        }
        @keyframes heartbeat {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        /* Add padding to main content to avoid footer overlap */
        .main .block-container {
            padding-bottom: 60px;
        }
        /* Typewriter effect styling */
        .typewriter-container {
            min-height: 100px;
            padding: 1rem;
            border-left: 4px solid #2E86AB;
            background-color: #000000;
            border-radius: 0 8px 8px 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🧠 Hypercentaur - Psychology AI")
    st.subheader("Simple, Fast, and Actually Working!")
    
    # Initialize system
    if 'hypercentaur' not in st.session_state:
        st.session_state.hypercentaur = SimpleHypercentaur()
    
    # Initialize query counter - FIX #2: Proper counting from 1
    if 'queries_processed' not in st.session_state:
        st.session_state.queries_processed = 0
    
    # Initialize last result to persist confidence display
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    
    # Display stats
    stats = st.session_state.hypercentaur.get_stats()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Knowledge Entries", stats['total_entries'])
    with col2:
        st.metric("Queries Processed", st.session_state.queries_processed)  # FIX #2: Use our counter
    with col3:
        st.metric("Topics Covered", len(stats['topics']))
    
    # Query input - FIX #1: Clear text field after answering
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0
    
    query = st.text_input(
        "Ask any psychology question:",
        placeholder="e.g., How does the brain work? What is depression? Why do people conform in groups?",
        key=f"query_input_{st.session_state.input_key}"  # FIX #1: Dynamic key to clear field
    )
    
    if st.button("Ask Hypercentaur", type="primary") and query:
        # FIX #2: Increment counter immediately when button is pressed (proper counting from 1)
        st.session_state.queries_processed += 1
        
        # FIX #3: Show thinking simulation
        simulate_thinking()
        
        # Process the query
        result = st.session_state.hypercentaur.process_query(query)
        
        # Store result to persist after rerun
        st.session_state.last_result = result
        
        # Display result with FIX #3: typing simulation
        if result['success']:
            st.success("**Response:**")
            
            # Container for typewriter effect
            response_container = st.empty()
            
            # FIX #3: Typewriter effect for the response
            displayed_text = ""
            for char in result['response']:
                displayed_text += char
                response_container.markdown(f"<div class='typewriter-container'>{displayed_text}</div>", unsafe_allow_html=True)
                time.sleep(0.02)  # Typing speed
            
            # Show additional info after typing is complete
            col1, col2 = st.columns(2)
            with col1:
                confidence = result['confidence']
                color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
                st.write(f"**Confidence:** {color} {confidence:.2f}")
            
            with col2:
                if 'topic' in result:
                    st.write(f"**Topic:** {result['topic']}")
            
            # Show debug info
            with st.expander("Debug Information"):
                st.write(f"**Matched Question:** {result.get('matched_question', 'N/A')}")
                st.write(f"**Matched Keywords:** {result.get('matched_keywords', [])}")
        else:
            st.error(result['response'])
        
        # FIX #1: Clear the input field by changing the key
        st.session_state.input_key += 1
        st.rerun()
    
    # Display persistent result after rerun
    elif st.session_state.last_result:
        result = st.session_state.last_result
        if result['success']:
            st.success("**Response:**")
            st.markdown(f"<div class='typewriter-container'>{result['response']}</div>", unsafe_allow_html=True)
            
            # Show persistent confidence and topic
            col1, col2 = st.columns(2)
            with col1:
                confidence = result['confidence']
                color = "🟢" if confidence > 0.7 else "🟡" if confidence > 0.4 else "🔴"
                st.write(f"**Confidence:** {color} {confidence:.2f}")
            
            with col2:
                if 'topic' in result:
                    st.write(f"**Topic:** {result['topic']}")
            
            # Show debug info
            with st.expander("Debug Information"):
                st.write(f"**Matched Question:** {result.get('matched_question', 'N/A')}")
                st.write(f"**Matched Keywords:** {result.get('matched_keywords', [])}")
        else:
            st.error(result['response'])
    
    # Show query history
    if st.session_state.hypercentaur.query_history:
        st.subheader("Recent Queries")
        for i, entry in enumerate(reversed(st.session_state.hypercentaur.query_history[-5:])):
            with st.expander(f"Q: {entry['query'][:60]}..."):
                st.write(f"**A:** {entry['response']['response'][:200]}...")
    
    # Available topics
    with st.sidebar:
        st.subheader("Available Topics")
        for topic in stats['topics']:
            st.write(f"• {topic}")
        
        st.subheader("Example Queries")
        examples = [
            "How does the brain work?",
            "What is depression?", 
            "Why do people conform in groups?",
            "How does memory work?",
            "What is classical conditioning?",
            "How does stress affect memory?",
            "What motivates human behavior?",
            "How do children learn?"
        ]
        
        for example in examples:
            if st.button(example, key=f"example_{example[:10]}"):
                # FIX #1: Handle example button clicks properly
                st.session_state.input_key += 1
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p class="footer-text">
            Designed with <span class="love-icon">❤️</span> by <strong>Benjamin Obi</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()