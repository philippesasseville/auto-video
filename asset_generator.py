from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import os

def render_html_to_image(html_file_path, output_image_path):
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(f'file://{os.path.abspath(html_file_path)}')
    div_element = driver.find_element(By.ID, "target")
    size = div_element.size
    driver.set_window_size(1000, 1000)
    # Take the screenshot
    driver.save_screenshot(output_image_path+".png")
    driver.quit()

    # Open the saved screenshot
    img = Image.open(output_image_path+".png")
    width, height = img.size

    background_color=(0, 255, 0)
    tolerance = 0
    # Find the top left and bottom right corners of the content area (excluding the background color)
    top = height
    left = width
    bottom = 0
    right = 0
    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if all(abs(pixel[i] - background_color[i]) > tolerance for i in range(3)):  # Check if pixel is not background color
                top = min(top, y)
                left = min(left, x)
                bottom = max(bottom, y)
                right = max(right, x)

    # Crop the image to the content area
    content_area = (left - 20, top - 20, right + 20, bottom + 20)
    cropped_img = img.crop(content_area)
    cropped_img.save(output_image_path+"__cropped.png")

def generate_title_card_from_template(html_file_path, output_file_path, title):
    html_string = read_html_file(html_file_path)
    html_string = html_string.replace("{{title_placeholder}}", title)
    create_html_file(html_string, output_file_path)

def read_html_file(html_file_path):
    with open(html_file_path, 'r') as file:
        return file.read()

def create_html_file(html_string, output_file_path):
    with open(output_file_path, 'w') as f:
        f.write(html_string)
