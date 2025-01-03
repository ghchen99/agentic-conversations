# **AI Conversational Agents: Fun and Relatable Discussions About AI Concepts**

## **Overview**
This repository showcases a multi-agent conversational framework designed to explore AI concepts through structured yet casual and relatable discussions. It features three distinct agents—a knowledgeable AI expert, a curious binman, and a thoughtful mediator—working together to create an engaging dialogue about artificial intelligence topics without overwhelming technical jargon.

The system leverages OpenAI's Azure API for natural language processing and demonstrates how structured conversations can make complex topics accessible, fun, and easy to understand.

---

## **Key Features**
- **Multi-Agent Architecture**: Utilizes distinct AI personas, each with specific roles, to create dynamic and interactive conversations.
- **Relatable Explanations**: Frames AI concepts in scenarios inspired by day-to-day activities, such as sorting trash or optimizing routes, making explanations approachable.
- **Structured Dialogue Management**: Introduces a mediator agent to maintain focus, ensuring conversations are coherent while encouraging humor and relatable examples.
- **Flexible API Integration**: Connects to Azure OpenAI services for scalable and efficient language model interaction.
- **Interactive Console Output**: Streams real-time dialogue through a console-based UI for quick deployment and testing.

---

## **Agent Roles**
### **1. AI Expert Agent ("AINerd")**
- **Purpose**: Explain AI concepts in a casual, conversational tone with humor and relatable analogies.
- **Behavior**: Combines short, podcast-style explanations with occasional in-depth insights.
- **Examples**: Compares AI algorithms to sorting recyclables or identifying patterns in garbage collection.

### **2. Binman Agent ("Binman")**
- **Purpose**: Represent a curious layperson asking questions and reacting naturally to explanations.
- **Behavior**: Keeps discussions lighthearted with exclamations like "Wow!" and adds relatable thoughts.
- **Examples**: Draws comparisons between AI workflows and trash-sorting routines.

### **3. Mediator Agent ("Mediator")**
- **Purpose**: Guide the conversation structure, introducing topics like regression, neural networks, and pattern recognition in non-technical ways.
- **Behavior**: Keeps discussions organized while prompting the AI expert for relatable analogies.
- **Examples**: Suggests transitions to topics like convolutional neural networks by relating them to organizing bins by type or size.

---

## **Code Structure**
```
├── main.py                     # Entry point for the application.
├── autogen_ext/models/         # Azure OpenAI integration components.
├── autogen_agentchat/          # Agent and chat management modules.
├── autogen_agentchat/ui/       # Console interface for output streaming.
└── README.md                   # Project documentation.
```

---

## **Setup and Installation**
### **Prerequisites**
- Python 3.8 or later
- Azure OpenAI API key and endpoint configuration

### **Installation Steps**
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/agent-conversations.git
   cd agent-conversations
   ```
2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On MacOS/Linux
   venv\Scripts\activate     # On Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Environment Variables**:
   ```bash
   export AZURE_DEPLOYMENT="<your_azure_deployment>"
   export AZURE_MODEL_NAME="<your_model_name>"
   export AZURE_API_VERSION="<your_api_version>"
   export AZURE_ENDPOINT="<your_azure_endpoint>"
   export AZURE_API_KEY="<your_api_key>"
   ```
5. **Run the Application**:
   ```bash
   python main.py
   ```

---

## **How It Works**
1. **Agent Initialization**:
   - Creates distinct agents with predefined roles and personalities.
   - Connects each agent to Azure OpenAI services for conversational capabilities.
2. **Group Chat Setup**:
   - Combines agents into a structured group chat using a round-robin format.
   - Allows each agent to contribute in turn, ensuring balanced participation.
3. **Real-Time Interaction**:
   - Streams conversation output via the console.
   - Maintains natural pauses and varied response lengths for realism.

---

## **Example Conversation**
**Input Task**: "Have a casual chat about AI, keeping it fun and relatable with natural pauses and varied response lengths. Introduce structured topics through the mediator."

**Output Snippet**:
```
Mediator: Let's start with something simple—how does AI learn patterns?
AI Nerd: Great question! Think of it like sorting recyclables. AI looks for patterns, like spotting cans, plastics, and glass.
Binman: Oh wow! So it’s kind of like me separating trash into bins?
AI Nerd: Exactly! Imagine it learns from mistakes too, like if it puts glass in the wrong bin, it adjusts next time.
Mediator: Nice analogy! How about we explore neural networks next?
```

---

## **Customization**
- **Adding New Agents**: Extend the `AssistantAgent` class to create custom personalities and roles.
- **Changing Topics**: Modify system messages and descriptions to focus on different domains like finance, healthcare, or robotics.
- **Integrating Tools**: Attach APIs or tools to agents for enhanced capabilities.

---

## **Future Enhancements**
- **Web Interface**: Build a web-based UI for wider accessibility.
- **Voice Input/Output**: Add speech-to-text and text-to-speech integration.
- **Knowledge Graph Integration**: Enhance topic depth and accuracy.

---

## **Contributing**
Pull requests are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Commit your changes with clear descriptions.
4. Submit a pull request.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---

## **Contact**
For questions or suggestions, reach out via email at `support@example.com` or open an issue in the repository.
