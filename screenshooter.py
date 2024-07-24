import os
import pyautogui
import imageio
import subprocess
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class ScreenshotApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Screenshot App")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.screenshot_button = QPushButton("Capture full screen")
        self.screenshot_button.clicked.connect(self.capture_screenshot)
        layout.addWidget(self.screenshot_button)

        self.selected_button = QPushButton("Capture selected area")
        self.selected_button.clicked.connect(self.take_selected)
        layout.addWidget(self.selected_button)

        self.gif_button = QPushButton("Create Animated GIF")
        self.gif_button.clicked.connect(self.create_gif)
        layout.addWidget(self.gif_button)

        self.setLayout(layout)

    def capture_screenshot(self):
        # Create screenshots folder if it doesn't exist
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        filename = os.path.join("screenshots", f"screenshot_{len(os.listdir('screenshots'))}.png")
        pyautogui.screenshot(filename)
        QMessageBox.information(self, "Screenshot Captured", f"Screenshot saved as {filename}")

    def take_selected(self):
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        filename = os.path.join("screenshots", f"screenshot_{len(os.listdir('screenshots'))}.png")
        # Run the gnome-screenshot command
        subprocess.run(['gnome-screenshot', '-a', '-f', filename])

    def create_gif(self):
        screenshots_folder = "screenshots"
        screenshots = [os.path.join(screenshots_folder, file) for file in os.listdir(screenshots_folder) if file.startswith("screenshot")]
        if not screenshots:
            QMessageBox.warning(self, "Error", "No screenshots found.")
            return

        screenshots.sort()
        output_file = "screenshot.gif"

        with imageio.get_writer(output_file, mode='I', duration=2000) as writer: # Set duration to 1 second (1000 milliseconds)
            for screenshot in screenshots:
                image = imageio.imread(screenshot)
                writer.append_data(image)

        QMessageBox.information(self, "Animated GIF Created", f"Animated GIF saved as {output_file}")

if __name__ == "__main__":
    app = QApplication([])
    window = ScreenshotApp()
    window.show()
    app.exec_()
