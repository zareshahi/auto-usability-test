# Auto Usability Test Generator

## Overview
Welcome to the Auto Usability Test Generator project! This Python-based tool utilizes Large Language Models (LLMs) to automatically generate usability tests, helping create safer and more user-friendly applications.

## Features
- **Automated Usability Test Generation**: Generate comprehensive usability tests using LLMs.
- **Enhanced UI/UX Safety**: Identify and address potential usability issues.
- **Customizable Test Scenarios**: Adapt tests to meet the specific needs of your application.

## Getting Started

### Prerequisites
- Python 3.7 or higher
- Dependencies listed in `requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/zareshahi/auto-usability-test.git
   cd auto-usability-test
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage
1. Prepare your application details and UI components that need to be tested.
2. Run the main script to generate usability tests:
   ```bash
   python main.py
   ```

## Example
```python
from test_generator import UsabilityTestGenerator

app_details = {
    "app_name": "MyApp",
    "components": [
        {"type": "button", "label": "Submit"},
        {"type": "input", "label": "Username"},
        {"type": "input", "label": "Password"}
    ]
}

generator = UsabilityTestGenerator(app_details)
tests = generator.generate()
for test in tests:
    print(test)
```

## Contributing
We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please open an issue or contact us at zareshahi@gmail.com.

## Acknowledgements
We extend our gratitude to the open-source community and the developers of the libraries we rely on.

---

Thank you for using the Auto Usability Test Generator! Let's create safer and more user-friendly applications together.
