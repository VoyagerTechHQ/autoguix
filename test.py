import pyautox as ag

# Initialize
ag.init()

# Get screen size
width, height = ag.size()
print(f"Screen: {width}x{height}")

# Move mouse to center
ag.moveTo(width // 2, height // 2, duration=1.0)

# Click
ag.click()

# Type text
ag.typewrite("Hello from PyAutoX!", interval=0.05)

# Take screenshot
screenshot = ag.screenshot()
screenshot.save("screenshot.png")
