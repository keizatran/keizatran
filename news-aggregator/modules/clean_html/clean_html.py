import re

def clean_html(text: str) -> str:
    """Cleans HTML tags from a string.

    Args:
        text: The string to clean.

    Returns:
        The string with the HTML tags removed.
    """

    pattern1 = re.compile(r"<.*?>", re.DOTALL)
    pattern2 = re.compile("\\n|\\r")
    final_text = re.sub(pattern2, "", re.sub(pattern1, "", text))
    return final_text