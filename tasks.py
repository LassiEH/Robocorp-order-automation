from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables

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
    orders = get_orders()

def open_order_website():
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    library = Tables()
    http = HTTP()
    http.download(url = "https://robotsparebinindustries.com/orders.csv", overwrite=True)
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"]
    )

    for order in orders:
        message = order

