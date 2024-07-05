import os
import time
import random
import json
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from dotenv import load_dotenv
from huggingface_chatbot import HuggingFaceChatBot
import subprocess
from selenium.webdriver.chrome.options import Options as ChromeOptions

load_dotenv()
install_path = "./ENV/driver"
cache_manager = DriverCacheManager(install_path)
options = ChromeOptions()
options.set_capability("se:name", "test_visit_basic_auth_secured_page (ChromeTests)")
driver = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)

# Initialize WebDriver and OpenAI API
hf_chatbot = HuggingFaceChatBot()


def get_actions_from_html(html_content):
    response = (
        hf_chatbot.conversation(
            f"The following is the HTML content of a webpage: {html_content}\nWhat actions should be performed on this webpage? just return .robot TestSuite file format"
        )
        or ""
    )
    response = response.split("```")[1] or response
    robot_file_path = "./ENV/result.robot"
    with open(robot_file_path, "w", encoding="utf-8") as robot_file:
        robot_file.write(response or "")
    print("**" * 50)
    print(response)
    print("**" * 50)
    return robot_file_path


try:
    # Open the webpage
    driver.get("https://react-landing-page-template-93ne.vercel.app/")

    # Extract HTML body content
    html_content = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")

    # Get actions from the chatbot based on HTML content
    robot_file_path = get_actions_from_html(html_content)

    # Close the WebDriver as we will use Robot Framework for interaction
    driver.quit()

    # Execute the .robot file using the Robot Framework
    result_path = "./ENV/results"
    os.makedirs(result_path, exist_ok=True)
    subprocess.run(
        [
            "robot",
            "--variable",
            "BROWSER:Chrome",
            "--variable",
            "URL:http://localhost:4443",
            "-d",
            result_path,
            robot_file_path,
        ],
        check=True,
    )

    # Load the log file generated by the Robot Framework
    log_file_path = os.path.join(result_path, "log.html")
    with open(log_file_path, "r") as f:
        log_content = f.read()
    # Parse log_content to extract action logs (simplified example)
    action_log = json.loads(log_content)  # Adjust based on actual log format

    # Save action log to file
    with open("action_log.json", "w") as f:
        json.dump(action_log, f)

    # Load action log data
    with open("action_log.json", "r") as f:
        action_log = json.load(f)

    # Extract mouse movement data
    mouse_movements = [(log["x"], log["y"]) for log in action_log if log["type"] == "move"]

    # Check if there are any mouse movements
    if mouse_movements:
        # Create heat map for mouse movements
        x_coords, y_coords = zip(*mouse_movements)
        plt.figure(figsize=(10, 6))
        sns.kdeplot(x=x_coords, y=y_coords, cmap="Reds", shade=True, bw_adjust=0.5)
        plt.title("Mouse Movement Heat Map")
        plt.gca().invert_yaxis()  # Invert y-axis to match web page coordinates
        plt.show()
    else:
        print("No mouse movements recorded.")

    # Extract click data
    clicks = [(log["x"], log["y"]) for log in action_log if log["type"] == "click"]

    # Check if there are any clicks
    if clicks:
        # Create scatter plot for clicks
        plt.figure(figsize=(10, 6))
        plt.scatter(*zip(*clicks), c="blue", label="Clicks")
        plt.title("Click Locations")
        plt.gca().invert_yaxis()
        plt.legend()
        plt.show()
    else:
        print("No clicks recorded.")

except Exception as e:
    print(f"Exception encountered: {e}")

finally:
    # Ensure the WebDriver is closed properly if still open
    try:
        driver.quit()
    except:
        pass
