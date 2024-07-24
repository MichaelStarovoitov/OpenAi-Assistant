import re
# from googletrans import Translator


def convert_to_markdown(text):
    """
    Converts a plain text message to Markdown format.
    """
    # Split the text into lines
    lines = text.split('\n')

    # Process each line
    markdown_lines = []
    for line in lines:
        # Strip leading and trailing whitespace
        line = line.strip()

        # Check if line is not empty
        if line:
            # Escape special characters for Markdown
            line = line.replace('*', '\\*').replace('_', '\\_').replace('`', '\\`').replace('#', '\\#')
            markdown_lines.append(line)

    # Join the processed lines into a single string with line breaks
    markdown_text = '\n\n'.join(markdown_lines)
    
    return markdown_text

def get_simple_markdown(pattern, text):
    return re.sub(r'\*(.*?)\*', r'**\1**', re.sub(pattern, '', text))

def text_translator(text='', src='ru', dest='uk'):
    # try:
    #     translator = Translator()
    #     newText = translator.translate(text=text,src=src, dest=dest )
    #     return newText.text
    # except Exception as ex:
    #     return text
    return text