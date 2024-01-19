from robocorp.tasks import task
from robocorp import browser

@task
def robot_order():
    """
    Orders robots from the RobotSpareBin Industries
    website. 
    It saves the order HTML receipt as a PDF file,
    saves the screenshot of the robot,
    Embeds the screenshot to the receipt and
    creates a ZIP archive of the receipts and images.
    """
    browser.configure(
        slowmo = 500,
    )
    open_order_website()

def open_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")
