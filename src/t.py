import difflib,sys

a = """
In times of stress, one must consider! the amount of probloms that might occur. 

Soemtimes, it can be DISASTROUS!
"""

b = """
In times of stress, one must consider the amount of problems that might occur, such as:
- The effect can be catalysmic, if not disastrous.
"""

sys.stdout.writelines(difflib.context_diff(a, b))