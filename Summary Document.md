# LLM-Quiz-App Summary Document

## Overview of Selected LLM - "LLama-3 70B Instruct"

### Overview
The "LLama-3 70B Instruct" is a state-of-the-art language model designed for various natural language processing tasks, including generating quiz questions. With 70 billion parameters, it excels in understanding context, generating coherent and contextually appropriate responses, and handling complex instructions.

### Rationale for Choice
- **High Performance**: Provides high accuracy and fluency in generated text.
- **Versatility**: Suitable for a wide range of topics and question formats.
- **Instruction-Tuned**: Optimized for following specific instructions, making it ideal for quiz generation.

## Prompt Engineering Techniques in `prompts.py`

### Description
The prompt engineering techniques used in `prompts.py` are designed to extract high-quality quiz questions from the LLM. Key techniques include:

- **Contextual Prompts**: Providing context to guide the model in generating relevant questions.
- **Few-Shot Learning**: Including examples in the prompt to demonstrate the desired output format.
- **Specificity**: Clearly defining the topic, difficulty level, and format to ensure precision.

### Contribution to High-Quality Questions
These techniques ensure that the questions are:
- **Relevant**: Closely aligned with the specified topic.
- **Clear**: Well-structured and easy to understand.
- **Diverse**: Covering a range of difficulty levels and formats.

## Instructions for Running the Tool

### Command-Line Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AvivGelfand/LLM-Quiz-App.git
   cd LLM-Quiz-App
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

### Web-Based Instructions
- Open a terminal and navigate to the project directory.
- Run the command `streamlit run app.py`.
- Open a web browser and go to the provided local URL (typically `http://localhost:8501`).

### Dependencies
- Python 3.x
- Streamlit
- Required libraries listed in `requirements.txt`

## Potential Ideas for Enhancement

### Enhancing Prompts
- **Dynamic Context Adjustment**: Adjust prompts dynamically based on user performance to personalize the difficulty level.
- **Incorporating Feedback**: Use user feedback to refine and improve the prompts over time.

### Expanding Tool Capabilities
- **Additional Quiz Formats**: Support for various question types such as multiple-choice, true/false, and fill-in-the-blank.
- **Interactive Features**: Implement features like hint generation and adaptive questioning.
- **Multilingual Support**: Expand to support multiple languages for a broader audience.

---

This document provides a comprehensive overview of the LLM-Quiz-App, detailing the selected LLM, prompt engineering techniques, usage instructions, and potential enhancements.
