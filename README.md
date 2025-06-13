# CrewAI Customer Support System

A sophisticated multi-agent customer support system built with CrewAI and powered by Google's Gemini 2.0 Flash model. This system uses two specialized AI agents working in tandem to provide comprehensive, accurate, and friendly customer support responses.

## 🤖 How It Works

The system employs two specialized agents:

1. **Senior Support Representative**: Handles initial customer inquiries, researches solutions using web scraping tools, and provides detailed responses
2. **Support Quality Assurance Specialist**: Reviews and refines responses to ensure accuracy, completeness, and professional tone

## ✨ Features

- **Multi-Agent Collaboration**: Two AI agents work together to ensure high-quality responses
- **Intelligent Rate Limiting**: Smart rate limiting system prevents API quota exhaustion
- **Web Scraping Capabilities**: Automatically searches and scrapes relevant documentation
- **Comprehensive Error Handling**: Robust error handling with retry mechanisms
- **Memory Integration**: Maintains context across conversations using CrewAI's memory system
- **Interactive CLI**: User-friendly command-line interface for processing inquiries

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini 2.0 Flash

### Setup

1. Clone the repository:
```bash
git clone https://github.com/naakaarafr/CrewAI-Customer-Support-System.git
cd CrewAI-Customer-Support-System
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```bash
GOOGLE_API_KEY=your_google_api_key_here
```

### Required Dependencies

Create a `requirements.txt` file with the following packages:
```
crewai>=0.20.0
langchain-google-genai
python-dotenv
requests
beautifulsoup4
pydantic
crewai-tools
```

## 🚀 Usage

### Command Line Interface

Run the interactive CLI:
```bash
python main.py
```

The system will prompt you for:
- Customer company name
- Contact person's name
- Customer inquiry (press Enter twice to finish)

### Programmatic Usage

```python
from crew import run_support_crew

result = run_support_crew(
    customer="TechCorp Inc",
    person="John Smith",
    inquiry="I'm having trouble setting up agents with custom tools in CrewAI. Can you help me understand the proper way to implement this?"
)

print(result)
```

## 📁 Project Structure

```
crewai-support-system/
├── main.py              # CLI entry point
├── crew.py              # Crew configuration and orchestration
├── agents.py            # Agent definitions and LLM setup
├── tasks.py             # Task definitions for agents
├── tools.py             # Custom web scraping tools
├── .env                 # Environment variables (create this)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🔧 Configuration

### Rate Limiting

The system includes intelligent rate limiting to prevent API quota exhaustion:

- **Base delay**: 5 seconds between requests
- **Maximum delay**: 60 seconds
- **Adaptive backoff**: Automatically adjusts delays based on API responses
- **Retry logic**: Up to 3 retry attempts with exponential backoff

### LLM Configuration

The Gemini 2.0 Flash model is configured with:
- **Temperature**: 0.3 (balanced creativity/accuracy)
- **Max tokens**: 1024 (conservative to avoid quota issues)
- **Request timeout**: 120 seconds
- **Max retries**: 5 attempts

### Web Scraping

- **Rate limiting**: 3-6 second delays between requests
- **Retry logic**: Up to 3 attempts per URL
- **Content filtering**: Removes non-essential elements (scripts, styles, navigation)
- **Length limits**: Truncates content to 3000 characters to stay within token limits

## 🎯 Use Cases

- **Technical Support**: Handle complex technical inquiries with research capabilities
- **Product Documentation**: Automatically find and reference relevant documentation
- **Customer Service**: Provide consistent, high-quality customer support responses
- **Knowledge Base**: Build comprehensive responses by scraping multiple sources

## 🔒 Security & Best Practices

- **API Key Protection**: Store API keys in environment variables
- **Rate Limiting**: Prevents overwhelming external APIs and services
- **Error Handling**: Comprehensive error handling prevents crashes
- **Content Validation**: Filters and validates scraped content

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Found**
   - Ensure `GOOGLE_API_KEY` is set in your `.env` file
   - Verify the key has access to Gemini 2.0 Flash model

2. **Rate Limit Errors**
   - The system automatically handles rate limits with exponential backoff
   - Consider upgrading your API quota if issues persist

3. **Scraping Failures**
   - Some websites may block automated requests
   - The system falls back to built-in CrewAI tools if custom tools fail

4. **Memory Issues**
   - Large responses may cause memory issues
   - Content is automatically truncated to prevent token limit exceeded errors

### Debug Mode

Enable verbose logging by setting `verbose=True` in the crew configuration:
```python
support_crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    process=Process.sequential,
    verbose=2,  # Set to 2 for maximum verbosity
    memory=True
)
```

## 📈 Performance Optimization

- **Token Management**: Conservative token limits to prevent quota exhaustion
- **Intelligent Caching**: CrewAI's memory system caches responses
- **Efficient Scraping**: Targeted content extraction reduces processing time
- **Adaptive Rate Limiting**: Automatically adjusts based on API performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) for the multi-agent framework
- [Google AI](https://ai.google/) for the Gemini 2.0 Flash model
- [LangChain](https://langchain.com) for LLM integration

## 📞 Support

For questions or support, please open an issue on GitHub or contact [@naakaarafr](https://github.com/naakaarafr).
