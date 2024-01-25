from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
from robot.libraries.BuiltIn import BuiltIn

@task
def robot_order():
    """
    Orders robots from the RobotSpareBin Industries
    website. 
    It saves the order HTML-element receipt as a PDF file,
    saves the screenshot of the robot,
    Embeds the screenshot to the receipt and
    creates a ZIP archive of the receipts embedded with
    the images.
    """
    
    browser.configure(
        slowmo = 10,
    )
    open_order_website()
    orders = get_orders()
    close_annoying_modal()
    loop_orders(orders)
    archive_receipts()


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

    #Solves the occasional error
    while page.query_selector('div.alert.alert-danger[role="alert"]'):
        page.click("button:text('Order')")

    #Save the pdf
    store_receipt_as_pdf(order_info["Order number"])
    #Save the png
    screenshot_robot(order_info["Order number"])

    #Embed the png into the pdf
    pdf_path = "output/receipts/order_receipt_" + str(order_info["Order number"]) + ".pdf"
    png_path = "output/pictures/order_picture_" + str(order_info["Order number"]) + ".png"
    embed_screenshot_to_receipt(png_path, pdf_path)

    page.click("button:text('Order another robot')")

    close_annoying_modal()

def store_receipt_as_pdf(order_number):
    """Stores the receipt as a pdf file"""
    page = browser.page()

    robot_order_html = page.locator("#order-completion").inner_html()
    pdf = PDF()
    output_dir = "output/receipts/order_receipt_" + str(order_number) + ".pdf"
    pdf.html_to_pdf(robot_order_html, output_dir)

def screenshot_robot(order_number):
    """Stores the receipt as a png file"""
    page = browser.page()

    output_directory = "output/pictures/order_picture_" + str(order_number) + ".png"
    page.locator("#robot-preview").screenshot(path=output_directory)

def embed_screenshot_to_receipt(screenshot, pdffile):
    """Embeds the screenshot to the end of the receipt"""
    pdf = PDF()
    
    pdf.add_watermark_image_to_pdf(
        image_path = screenshot,
        source_path = pdffile,
        output_path = pdffile,
    )
    
def archive_receipts():
    """Creates a zip file of the receipts"""
    lib = Archive()
    lib.archive_folder_with_zip('output/receipts', 'orders.zip', recursive=True)