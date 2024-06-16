# LLM Quiz Wizard - LLM-Powered Quiz Generator
[CLICK HERE TO TRY IT ONLINE](https://llm-quiz-wizard.streamlit.app/)
![ezgif-2-9b593fe36d](https://github.com/AvivGelfand/LLM-Quiz-App/assets/63909805/c12508a5-a7c1-4f99-a384-a03aa44e1cc3)


LLM-Quiz-App is a web application that generates quiz questions using large language models (LLMs). This app leverages advanced natural language processing capabilities to create engaging and challenging quizzes on various topics.

## Features

- Generate quiz questions dynamically using the LLMs: [Mixtral 8x7b](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1) and [LLaMA3](https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct) 70b.
- The language models are called in a lightning-fast LPU engine of [Groq](https://groq.com/).
- Supports various topics and difficulty levels.
- User-friendly interface with [Streamlit](https://streamlit.io/).
- Easily extensible for additional features and customization.

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/AvivGelfand/LLM-Quiz-App.git
cd LLM-Quiz-App
pip install -r requirements.txt
```

## Usage

Run the application with Streamlit:

```bash
streamlit run app.py
```

## File Structure

- `app.py`: Main application file for Streamlit.
- `llm_operator.py`: Handles interactions with the language model.
- `prompts.py`: Contains the prompts and prompt customizing functions used to generate quiz questions.
- `requirements.txt`: Lists the required Python packages.
- `README.md`: Project documentation.
- `.gitignore`: Specifies files that are to be ignored in version control.
- `LICENSE`: Project license.

## Acknowledgments

Special thanks to the developers of the language models and the open-source community for their continuous support and contributions.

---

Feel free to adjust the sections to better match your project's specifics and add any additional details you find necessary.
