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
├── .env                        # Environment variables.
├── requirements.txt            # Required libraries.
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
---------- user ----------
Have a casual chat about AI, keeping it fun and relatable with natural pauses and varied response lengths. Introduce structured topics through the mediator.
---------- AINerd ----------
Absolutely, let’s dive into the world of AI with a twist. Imagine AI as a trusty sidekick to a binman, helping sort through all those bins with super speed and precision. You know, instead of just chucking everything into one big pile, AI can help sort recyclables from trash, much like how it classifies data. Cool, right?

Now, think about when a binman gets to know the best routes to take during collection. An AI could analyze traffic patterns, predicting the best path to get the job done faster and with less fuel. It’s like optimizing your time and energy, which is always a win!

What do you think, should we dig deeper into how AI does this magic, or explore another binman-like analogy?
[Prompt tokens: 101, Completion tokens: 153]
---------- Binman ----------
Hmm, I like the sound of AI being the ultimate sorting superhero. It’s like finding a rare treasure among common junk, right? Now, speaking of routes, it’s fascinating how AI can practically serve as a GPS wizard. Imagine fewer U-turns and detours—saves time and even a whole lot of patience, don’t you think?

Now, what if we looked into how AI learns? You know, kind of like when a binman discovers the secret spots where someone might hide a perfectly good sofa on bin day, or when to expect a mountain of pizza boxes after a big game night. Wouldn't it be interesting to know how AI gathers all that data to "learn" just like that?
[Prompt tokens: 238, Completion tokens: 144]
---------- Mediator ----------
Absolutely, learning in AI can be very much like a binman figuring out those secret sofa-hiding spots—it's all about experience and making sense of patterns over time. Imagine AI as a super-diligent apprentice. When it’s learning, it’s trying to get better at its job by reviewing past data, much like predicting those post-game pizza box mountains.

This learning process, often referred to as regression in AI, is about detecting trends or behaviors. It's like a binman who learns that Friday nights in a college town might mean more recycling on Saturday morning because of the big parties. The AI takes all these past situations into account to make informed predictions about future scenarios. 

What do you think, shall we uncover more about AI's learning adventures, or how about exploring how it can identify items like a binman identifying recyclables from trash?
[Prompt tokens: 407, Completion tokens: 171]
---------- AINerd ----------
Great question! Let's dive into how AI picks up its sorting skills, much like a binman figuring out the recyclables. Imagine a digital brain analyzing heaps of labeled trash—each piece marked clearly as recyclable or not. This is much like how a binman learns by seeing and sorting things over time. 

In AI-land, this is called supervised learning. The AI gets a massive pile of data to study, then it starts spotting patterns—just like figuring out which parts of trash belong in the recycling bin. The more it "practices," the better it gets at recognizing these items on its own, like a binman who can spot an aluminum can from a mile away.

Isn't it cool how this parallels with real-world tasks? Which aspect excites you more about AI—its ability to tirelessly learn or maybe its knack for spotting patterns?
[Prompt tokens: 589, Completion tokens: 172]
---------- Binman ----------
Hmm, sounds like a superpower worth having, don't you think? Just imagine having the knack to spot patterns everywhere! It's almost like having laser vision for details. I think what’s really exciting is how AI doesn't tire out. I mean, if a binman had endless energy, zero breaks needed, now that'd be something! 

Then again, there's something quite fascinating about its learning journey too. It's as if AI is on this continuous quest to perfection, similar to a binman who gradually fine-tunes the art of trash disposal. Each load teaches something new. Hmm, which do you find cooler—the tireless enthusiasm or the ability to spot those tricky patterns?
[Prompt tokens: 745, Completion tokens: 135]
---------- Mediator ----------
Mediator: That is a tough choice, isn’t it? On one hand, AI’s tireless enthusiasm—its ability to work without breaks—is pretty remarkable. Imagine having a sidekick that never needs to rest, always ready to analyze the next batch of information, similar to a binman that can keep sorting recyclables through the night without tiring. It’s like having a never-ending energy boost on hand.

On the other hand, the way AI can spot those tricky patterns is equally impressive. Much like a binman locating valuable recyclables in a mountain of waste, AI can detect intricate patterns in data that might escape a human eye at first glance. It’s as if it has this sixth sense for spotting what’s important.

Both abilities have their charm and usefulness. Perhaps it's how these skills intertwine that makes AI such a promising ally in various fields. There’s always more to discover! Shall we explore how AI identifies these patterns or maybe dive into its role in predicting, like a binman forecasting trash trends?
[Prompt tokens: 905, Completion tokens: 204]
---------- Summary ----------
Number of messages: 7
Finish reason: Maximum number of turns 6 reached.
Total prompt tokens: 2985
Total completion tokens: 979
Duration: 15.19 seconds
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
