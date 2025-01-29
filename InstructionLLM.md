Run the command
pip install -r requirements.txt

streamlit run llm.py


1) Install Ollama

Quick intro to Ollama: It's a tool for running AI models locally on your machine. Grab it here: https://ollama.com/download

Ollama offers different model sizes - basically, bigger models = smarter AI, but need better GPU. Here's the lineup:
ollama run deepseek-r1:8b

3) Set up Chatbox - a powerful client for AI models
Download here: https://chatboxai.app

In Chatbox, go to settings and switch the model provider to Ollama. Since you're running models locally, you can ignore the built-in cloud AI options - no license key or payment is needed!

Then set up the Ollama API host - the default setting is http://127.0.0.1:11434, which should work right out of the box. That's it! Just pick the model and hit save. Now you're all set and ready to chat with your locally running Deepseek R1! 🚀
