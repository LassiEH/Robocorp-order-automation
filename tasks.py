from robocorp.tasks import task

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
    message = "Hello"
    message = message + " World!"
