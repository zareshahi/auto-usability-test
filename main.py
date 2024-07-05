import os
import time
import random
import json
import matplotlib.pyplot as plt
import seaborn as sns
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from dotenv import load_dotenv

from huggingface_chatbot import HuggingFaceChatBot

load_dotenv()
install_path = "./ENV/driver"
cache_manager = DriverCacheManager(install_path)
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager(cache_manager=cache_manager).install()))

# Initialize WebDriver and OpenAI API
hf_chatbot = HuggingFaceChatBot()

action_log = []

def human_like_mouse_move(driver, element, duration=1.0):
    action = ActionChains(driver)
    start_x, start_y = (
        action.w3c_actions.pointer_inputs[0].parameters["origin"]["x"],
        action.w3c_actions.pointer_inputs[0].parameters["origin"]["y"],
    )
    end_x, end_y = element.location["x"], element.location["y"]

    num_steps = int(duration * 60)  # 60 steps per second
    for step in range(num_steps):
        progress = step / num_steps
        x = start_x + (end_x - start_x) * progress + random.uniform(-3, 3)  # Adding some randomness
        y = start_y + (end_y - start_y) * progress + random.uniform(-3, 3)
        action.move_to_element_with_offset(element, int(x), int(y)).perform()
        time.sleep(duration / num_steps)
        # Log mouse movement
        action_log.append({"type": "move", "x": int(x), "y": int(y), "timestamp": time.time()})

def smooth_scroll(driver, start, end, duration=1.0):
    steps = int(duration * 60)  # 60 steps per second
    for step in range(steps):
        scroll = start + (end - start) * (step / steps) + random.uniform(-3, 3)
        driver.execute_script(f"window.scrollTo(0, {int(scroll)});")
        time.sleep(duration / steps)
        # Log scroll action
        action_log.append({"type": "scroll", "scroll_position": int(scroll), "timestamp": time.time()})

def get_actions_from_html(html_content):
    response = hf_chatbot.conversation(f"The following is the HTML content of a webpage: {html_content}\nWhat actions should be performed on this webpage?")
    print("**" * 50)
    print(response)
    print("**" * 50)
    return response

try:
    # Open the webpage
    driver.get("https://react-landing-page-template-93ne.vercel.app/")

    # Extract HTML body content
    html_content = driver.find_element(By.TAG_NAME, 'body').get_attribute('innerHTML')

    # Get actions from the chatbot based on HTML content
    actions = get_actions_from_html(html_content)

    # Perform AI-driven interactions based on the chatbot's response
    for action in actions.split("\n"):
        if "click" in action.lower():
            try:
                # Extract the element locator from the action
                element_text = action.split("click")[1].strip().strip('"').strip("'")
                element = driver.find_element(By.LINK_TEXT, element_text)
                human_like_mouse_move(driver, element)
                element.click()
                action_log.append(
                    {
                        "type": "click",
                        "element": element_text,
                        "x": element.location["x"],
                        "y": element.location["y"],
                        "timestamp": time.time(),
                    }
                )
            except Exception as e:
                print(f"Error clicking element: {e}")
                action_log.append({"type": "error", "message": str(e), "timestamp": time.time()})
        elif "scroll" in action.lower():
            smooth_scroll(driver, 0, driver.execute_script("return document.body.scrollHeight"), duration=2)
        # Add more conditions based on possible AI outputs

except Exception as e:
    print(f"Exception encountered: {e}")

finally:
    # Ensure the WebDriver is closed properly
    driver.quit()

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
