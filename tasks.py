from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from robot.libraries.BuiltIn import BuiltIn

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
    close_annoying_modal()
    loop_orders(orders)


def open_order_website():
    """Opens the target website"""
    browser.goto("https://robotsparebinindustries.com/#/robot-order")

def get_orders():
    """Downloads the file we need and saves the contents into a table variable"""
    library = Tables()
    http = HTTP()
    http.download(url = "https://robotsparebinindustries.com/orders.csv", overwrite=True)
    orders = library.read_table_from_csv(
        "orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"]
    )

    return orders

def close_annoying_modal():
    """Closes the pop up modal"""
    page = browser.page()
    page.click("button:text('OK')")

def loop_orders(orders):
    """Goes through the orders in the table"""
    for order in orders:
        message = order
        fill_the_order(order)


def fill_the_order(order_info):
    """Fills every slot in the order page with right information"""
    page = browser.page()

    #Inputs the data for the head part
    page.select_option("#head", order_info["Head"])

    #Inputs the data for the body part
    text = "id-body-" + str(order_info["Body"])
    page.click(f"id={text}")
    
    #Inputs the data for the legs part
    page.fill("//input[@type='number']", order_info["Legs"])

    #Inputs the data for the address
    page.fill("#address", order_info["Address"])

    page.click("button:text('Order')")

    while page.query_selector('div.alert.alert-danger[role="alert"]'):
        page.click("button:text('Order')")

    #Lisää ratkaisu tilanteeseen, jossa tilaus ei mene läpi

    page.click("button:text('Order another robot')")

    close_annoying_modal()



