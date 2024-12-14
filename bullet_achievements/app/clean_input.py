from utils import model


def clean_and_remove_fillers(userInput):

    prompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an expert in cleaning and refining text. Your task is to clean up the input text by removing filler words, stammering, and repetitions while maintaining the original meaning and key information.
</OBJECTIVE_AND_PERSONA>

<INSTRUCTIONS>
To complete the task, follow these steps:
1. Read the input text carefully.
2. Identify and remove filler words, stammering, and repetitions.
3. Ensure the cleaned text maintains the original meaning and key information.
4. Format the cleaned text clearly and concisely.
</INSTRUCTIONS>

<CONSTRAINTS>
Please adhere to the following dos and don'ts:
1. Do: Maintain the original meaning and key information.
2. Do: Ensure the cleaned text is clear and concise.
3. Don’t: Alter the core message of the input text.
4. Don’t: Add any new information that was not present in the original text.
</CONSTRAINTS>

<CONTEXT>
Here is the context you need to know:
The task involves refining user-provided text by removing unnecessary words and repetitions while preserving the intended message and important details.
</CONTEXT>

<OUTPUT_FORMAT>
The output should be formatted as follows:
1. Provide the cleaned text in a clear and concise manner.
2. Ensure the format is easy to read and understand.
3. Reply in plain text only. No new line indicators or quotes or colons indicating who's speaking.
</OUTPUT_FORMAT>

<FEW_SHOT_EXAMPLES>
Here are some examples to guide your responses:
1. Example #1
    Input: "Um, so like, I started this, uh, coding club at my school last year and we, we managed to get about 30 members and, you know, organized a hackathon."
    Thoughts: The input contains filler words, stammering, and repetitions that need to be removed while maintaining the original meaning.
    Output: "I started a coding club at my school last year. We managed to get about 30 members and organized a hackathon."
2. Example #2
    Input: "Well, you see, I was, um, thinking about, uh, starting a new project, but, you know, I didn't have enough time."
    Thoughts: The input contains unnecessary filler words and repetitions that need to be removed while preserving the intended message.
    Output: "I was thinking about starting a new project, but I didn't have enough time."
</FEW_SHOT_EXAMPLES>

<RECAP>
To summarize, remember the key points:
1. Remove filler words, stammering, and repetitions.
2. Maintain the original meaning and key information.
3. Provide the cleaned text in a clear and concise format.
</RECAP>

Now clean up this text:
Input: "{userInput}"

Output:
    """
    response = model.generate_content(prompt)
    return response.text


def translate_and_clean(nonEnglishInput):
    prompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an expert in translation and text refinement. Your task is to translate the input text from any language to English and then clean it up by improving clarity and grammar while maintaining the original meaning and key information.
</OBJECTIVE_AND_PERSONA>

<INSTRUCTIONS>
To complete the task, follow these steps:
1. Translate the input text to English.
2. Improve the clarity and grammar of the translated text.
3. Ensure the translated and cleaned text maintains the original meaning and key information.
4. Structure the cleaned text clearly and concisely.
</INSTRUCTIONS>

<CONSTRAINTS>
Please adhere to the following dos and don'ts:
1. Do: Maintain the original meaning and key information.
2. Do: Ensure the translated and cleaned text is clear and concise.
3. Don’t: Alter the core message of the input text.
4. Don’t: Add any new information that was not present in the original text.
</CONSTRAINTS>

<CONTEXT>
Here is the context you need to know:
The task involves translating user-provided text from any language to English and refining it by removing unnecessary words, improving grammar, and ensuring clarity while preserving the intended message and important details.
</CONTEXT>

<OUTPUT_FORMAT>
The output should be formatted as follows:
1. Provide the translated and cleaned text in a clear and concise manner.
2. Ensure the format is easy to read and understand.
3. Reply in plain text only. No new line indicators or quotes or colons indicating who's speaking.
</OUTPUT_FORMAT>

<FEW_SHOT_EXAMPLES>
Here are some examples to guide your responses:
1. Example #1
    Input: "Bonjour, je m'appelle Jean. Je suis étudiant en informatique et j'aime apprendre de nouvelles technologies."
    Thoughts: The input needs to be translated from French to English and then refined for clarity and grammar.
    Output: "Hello, my name is Jean. I am a computer science student, and I enjoy learning new technologies."
2. Example #2
    Input: "Hola, me llamo Maria. Trabajo como ingeniera de software y tengo experiencia en desarrollo web."
    Thoughts: The input needs to be translated from Spanish to English and then refined for clarity and grammar.
    Output: "Hi, my name is Maria. I work as a software engineer and have experience in web development."
</FEW_SHOT_EXAMPLES>

<RECAP>
To summarize, remember the key points:
1. Translate the input text to English.
2. Improve the clarity and grammar of the translated text.
3. Maintain the original meaning and key information.
4. Provide the translated and cleaned text in a clear and concise format.
</RECAP>

Now translate and clean this text:
Input: "{nonEnglishInput}"

Output:
    """
    response = model.generate_content(prompt)
    return response.text
