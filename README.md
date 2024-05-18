

[![Release Badge](https://gitlab.com/pngts93/arctic-streamlit-hackathon/-/badges/release.svg?order_by=release_at)](https://gitlab.com/pngts93/arctic-streamlit-hackathon/-/releases)
[![pipeline status](https://gitlab.com/pngts93/arctic-streamlit-hackathon/badges/main/pipeline.svg)](https://gitlab.com/pngts93/arctic-streamlit-hackathon/-/commits/main)
[![Python Version](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/release/python-3916/)

# Table of Content
<!-- vscode-markdown-toc -->
* 1. [Categories and Scoring Guidelines](#CategoriesandScoringGuidelines)
	* 1.1. [Applying Scores](#ApplyingScores)
	* 1.2. [Example Evaluation](#ExampleEvaluation)
		* 1.2.1. [Initial Code](#InitialCode)
		* 1.2.2. [Refactored Code](#RefactoredCode)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->


##  1. <a name='CategoriesandScoringGuidelines'></a>Categories and Scoring Guidelines

1. **Technical Debt**
   - **Explanation**: Technical debt refers to the implied cost of additional rework caused by choosing an easy solution now instead of using a better approach that would take longer. It accumulates when code is written quickly without consideration for future maintenance.
   - **Scoring Guidelines**:
     - **10**: No technical debt; the code is well-structured, follows best practices, and is easy to maintain.
     - **8-9**: Minimal technical debt; the code is mostly clean but may have a few areas for improvement.
     - **6-7**: Moderate technical debt; the code has some issues that could complicate future maintenance.
     - **4-5**: Significant technical debt; the code has several issues that will require rework.
     - **1-3**: High technical debt; the code is poorly written and will need substantial rework.

2. **Maintainability Index**
   - **Explanation**: The maintainability index measures how easily code can be maintained, which includes modifying, fixing bugs, and adding new features. It is influenced by factors such as code complexity, documentation, and modularity.
   - **Scoring Guidelines**:
     - **10**: Highly maintainable; the code is modular, well-documented, and easy to understand.
     - **8-9**: Good maintainability; the code is mostly modular and documented, with few areas for improvement.
     - **6-7**: Average maintainability; the code can be maintained but has some areas that are not well-structured or documented.
     - **4-5**: Low maintainability; the code is difficult to understand and modify due to poor structure or lack of documentation.
     - **1-3**: Very low maintainability; the code is very difficult to maintain and lacks proper structure and documentation.

3. **Readability**
   - **Explanation**: Readability refers to how easily the code can be read and understood by others. It is influenced by factors such as naming conventions, use of comments, and code structure.
   - **Scoring Guidelines**:
     - **10**: Extremely readable; the code is clear, well-commented, and follows consistent naming conventions.
     - **8-9**: Very readable; the code is mostly clear and well-commented, with minor improvements needed.
     - **6-7**: Moderately readable; the code can be understood but may have some unclear areas or inconsistent naming.
     - **4-5**: Low readability; the code is difficult to understand due to lack of comments or poor naming conventions.
     - **1-3**: Very low readability; the code is very difficult to read and understand, with little to no comments or meaningful naming.

4. **Security Index**
   - **Explanation**: The security index measures how well the code handles potential security issues, such as input validation, error handling, and protection against common vulnerabilities.
   - **Scoring Guidelines**:
     - **10**: Highly secure; the code thoroughly validates input, handles errors correctly, and protects against common vulnerabilities.
     - **8-9**: Very secure; the code is mostly secure but may have a few areas for improvement.
     - **6-7**: Moderately secure; the code has some security measures but may not cover all potential issues.
     - **4-5**: Low security; the code lacks adequate security measures and is vulnerable to some issues.
     - **1-3**: Very low security; the code is highly vulnerable and lacks basic security measures.

###  1.1. <a name='ApplyingScores'></a>Applying Scores

When evaluating code, consider the following steps:

1. **Technical Debt**: Assess how easily the code can be maintained or extended in the future. Look for areas that might require rework and evaluate if best practices were followed.
2. **Maintainability Index**: Consider how modular and well-documented the code is. Check for complexity and ease of understanding.
3. **Readability**: Evaluate the clarity of the code. Look for meaningful naming conventions, use of comments, and overall structure.
4. **Security Index**: Check for proper input validation, error handling, and protection against common vulnerabilities.

###  1.2. <a name='ExampleEvaluation'></a>Example Evaluation

Let's take the initial and refactored `temp_converter` code as an example:

####  1.2.1. <a name='InitialCode'></a>Initial Code
```python
def temp_converter(temp, unit):
    if unit.upper() == 'C':
        return (temp * 9/5) + 32
    elif unit.upper() == 'F':
        return (temp - 32) * 5/9
    else:
        return "Invalid temperature unit. Please use 'C' for Celsius or 'F' for Fahrenheit."
```

- **Technical Debt**: 7 (Simple but lacks edge case handling)
- **Maintainability Index**: 7 (Maintainable but not modular)
- **Readability**: 8 (Clear but lacks detailed comments)
- **Security Index**: 6 (Assumes valid input without validation)

####  1.2.2. <a name='RefactoredCode'></a>Refactored Code
```python
def temp_converter(temp, unit):
    """
    Convert temperature between Celsius and Fahrenheit.

    Parameters:
    temp (float): The temperature value to convert.
    unit (str): The unit of the temperature value ('C' for Celsius, 'F' for Fahrenheit).

    Returns:
    float: The converted temperature.
    str: Error message if the unit is invalid.
    """
    if not isinstance(temp, (int, float)):
        return "Invalid temperature value. Please provide a numeric value."

    unit = unit.upper()
    if unit == 'C':
        return celsius_to_fahrenheit(temp)
    elif unit == 'F':
        return fahrenheit_to_celsius(temp)
    else:
        return "Invalid temperature unit. Please use 'C' for Celsius or 'F' for Fahrenheit."

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5/9
```

- **Technical Debt**: 8 (More robust, handles edge cases)
- **Maintainability Index**: 8 (Better structure and modularity)
- **Readability**: 9 (Clearer with comments and modular functions)
- **Security Index**: 8 (Improved input validation)
