# 🌐 Web Search Agent using Gemini & Tavily API

This project is an **AI-powered research assistant** built using the **Agents SDK**, **Google Gemini API**, and **Tavily Web Search API**.
It allows users to perform **personalized web searches**, **extract content from URLs**, and **summarize results** — all while tailoring responses based on user context.

---

## 🚀 Features

* **Personalized AI Assistance** — Responses are customized using the user’s name, city, and topic of interest.
* **Web Search with Tavily API** — Supports both *basic* and *advanced* search depth.
* **Content Extraction** — Fetches and extracts readable content from a list of URLs.
* **Gemini LLM Integration** — Uses `gemini-2.5-flash` for generating high-quality responses.
* **Streaming Output** — Real-time streaming of AI-generated responses.
* **Multi-Tool Agent** — Combines multiple tools (`web_search_tool`, `extract_content`, `user_info`) into a single intelligent agent.

---

## 🛠️ Requirements

* Python **3.10+**
* Required libraries:

  ```bash
  pip install agents tavily python-dotenv requests
  ```

---

## 🔑 Environment Variables

Create a `.env` file in your project root and add:

```env
GEMINI_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## 📂 File Structure

```
project/
│── main.py        # Main script with AI agent logic
│── .env           # API keys and secrets
│── README.md      # Project documentation
```

---

## ▶️ How to Run

1. Clone the repository or copy the `main.py` file.
2. Install dependencies:

   ```bash
   pip install agents tavily python-dotenv requests
   ```
3. Add your API keys to the `.env` file.
4. Run the project:

   ```bash
   python main.py
   ```

---

## 📜 How It Works

1. **User Context** is defined using `UserContext` (name, city, topic).
2. **Agent Tools**:

   * `user_info` → Returns a personalized message based on context.
   * `web_search_tool` → Uses Tavily API to search the web.
   * `extract_content` → Extracts readable text from given URLs.
3. **Agent Setup** — The `web_search_agent` uses Gemini as its brain and the above tools.
4. **Runner** streams real-time AI-generated answers to the terminal.

---

## 🖥 Example Output

```
User: tell me about new AI tools

- Claude 3.5 released with enhanced reasoning capabilities.
- OpenAI's GPT-5 is rumored for Q4 release with multi-modal improvements.
- Google DeepMind launched AlphaResearch for academic AI assistance.
- Hugging Face released new open-source fine-tuning models.
```
```
## 📌 Notes

* The **Tavily API** requires a valid API key and offers free & paid plans.
* You can switch the LLM by changing the `model` in `OpenAIChatCompletionsModel`.

```
