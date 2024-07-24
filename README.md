# Padayon-Ko

Padayon-Ko is a comprehensive application designed to assist users in enhancing and formatting various types of essays and achievements. The application leverages AI to generate content, refine, and optimize user inputs.

## Features

### Essay Processing

The application provides several functions to process different types of essays:

- **Format Essay**: Formats an essay with proper paragraph structure and punctuation, removing any markdown indicators to ensure it's in plain text format.
  - Function: [`format_essay`](backend/AI_Features/foundational-essays/app/main.py)

- **Process "How Are You Unique?" Essay**: Enhances an essay focusing on unique aspects of background, identity, interests, or talents, and how these contribute to academic or personal goals.
  - Function: [`process_how_are_you_unique_essay`](backend/AI_Features/foundational-essays/app/main.py)

- **Process Community Contribution Essay**: Enhances an essay focusing on specific community service projects, the problems addressed, actions taken, and the impact on the community.
  - Function: [`process_community_contribution_essay`](backend/AI_Features/foundational-essays/app/main.py)

- **Refine and Optimize Essay**: Refines and optimizes the essay based on the type of prompt.
  - Function: [`refine_and_optimize_essay`](backend/AI_Features/foundational-essays/app/main.py)

### Achievement Processing

The application also provides functions to process and generate detailed descriptions of achievements:

- **Clean and Remove Fillers**: Cleans the input and removes filler words.
  - Function: [`clean_and_remove_fillers`](backend/AI_Features/bullet_achievements/app/main.py)

- **Translate and Clean**: Translates non-English input and cleans it.
  - Function: [`translate_and_clean`](backend/AI_Features/bullet_achievements/app/main.py)

- **Extract Key Information**: Extracts key information from the cleaned input.
  - Function: [`extract_key_info`](backend/AI_Features/bullet_achievements/app/main.py)

- **Structure Achievement**: Structures the achievement using the X-Y-Z formula.
  - Function: [`structure_achievement`](backend/AI_Features/bullet_achievements/app/main.py)

- **Generate Bullet Point**: Generates a resume bullet point from the structured achievement.
  - Function: [`generate_bullet_point`](backend/AI_Features/bullet_achievements/app/main.py)

- **Generate Detailed Description**: Generates a detailed description of the achievement.
  - Function: [`generate_detailed_description`](backend/AI_Features/bullet_achievements/app/main.py)

- **Refine and Optimize**: Refines and optimizes the bullet point and detailed description.
  - Function: [`refine_and_optimize`](backend/AI_Features/bullet_achievements/app/main.py)

- **Separate Bullet and Description**: Separates the refined text into bullet points and detailed descriptions.
  - Function: [`separate_bullet_and_description`](backend/AI_Features/bullet_achievements/app/main.py)

### Notebooks

The project includes several Jupyter notebooks for processing different types of essays:

- [bullet_achievements.ipynb](backend/AI_Features/bullet_achievements.ipynb)
- [essay_new.ipynb](backend/AI_Features/essay_new.ipynb)
- [essay_RAG.ipynb](backend/AI_Features/essay_RAG.ipynb)
- [scholarship_match.ipynb](backend/AI_Features/scholarship_match.ipynb)

## Installation

1. Clone the repository:

    ```sh
    git clone <repository-url>
    ```

2. Navigate to the project directory:

    ```sh
    cd padayon-ko
    ```

3. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables by creating a `.env` file and adding your API keys:

    ```env
    GEMINI_API_KEY=your_gemini_api_key
    ```

## Usage

1. Run the Flask application:

    ```sh
    python backend/AI_Features/bullet_achievements/app/main.py
    ```

2. Access the application in your web browser at `http://localhost:5000`.

## License

This project is licensed under the MIT License.
