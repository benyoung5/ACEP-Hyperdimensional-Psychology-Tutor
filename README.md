✨ Features
🤖 HDC-Powered Brain: Uses hypervector operations (binding, bundling, permutation) for brain-like associative memory and reasoning.

📚 Comprehensive Knowledge: Expert-curated knowledge base covering 40+ psychology topics (Learning, Memory, Emotion, Cognition, Social Psychology, and more).

💬 Intelligent Q&A: Goes beyond keyword matching. Classifies query intent and retrieves semantically relevant answers with confidence scoring.

🎨 Sleek Web Interface: Built with Streamlit, featuring a typewriter response effect and interactive session history.

🚀 Lightweight & Efficient: No massive language models required. A self-contained, principled AI system.

🛠️ How It Works
ACEP's architecture is a novel implementation of Vector Symbolic Architectures:

Encoding: Psychology concepts ("classical conditioning", "cognitive dissonance") are mapped to high-dimensional random hypervectors.

Storage: These vectors, along with their semantic relationships, are stored in a high-dimensional space (vector_store.py).

Querying: User questions are also encoded into hypervectors.

Reasoning: The system performs a similarity search in this hyperdimensional space to find the most relevant concepts and constructs a coherent answer (reasoning_engine.py).

This process mimics human associative memory, making it fundamentally different from neural network-based approaches.

📦 Project Structure

acep-hdc-tutor/
├── main.py                 # Streamlit web application
├── hdc_core.py            # Core HDC algebra operations
├── vector_store.py        # HDC vector storage & retrieval
├── query_processor.py     # Processes and understands user queries
├── reasoning_engine.py    # Applies psychological reasoning strategies
├── data_loader.py         # Loads and preprocesses the psychology knowledge base
└── requirements.txt       # Python dependencies

Running the Application
Launch the Streamlit app and interact with ACEP in your browser: streamlit run main.py

💡 Example Queries
Try asking ACEP these questions to see it in action:

What is the difference between classical and operant conditioning?

How does stress affect memory?

Explain cognitive dissonance.

What are the stages of grief?

How do children learn according to Piaget?

🙋‍♂️ Author
Benjamin Obi

LinkedIn: [Benjamin Obi](https://www.linkedin.com/in/benjamin-obi/)
