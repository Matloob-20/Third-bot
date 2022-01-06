"""Template robot with Python."""
import time

from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Archive import Archive
import os

lib = Archive()
pdf = PDF()
file = Files()
browser = Selenium()
http = HTTP()
tables = Tables()
liss = []

# http.download("https://robotsparebinindustries.com/orders.csv")
browser.open_available_browser("https://robotsparebinindustries.com/#/robot-order", maximized=True)
folder = tables.read_table_from_csv("orders.csv", columns=["Order number", "Head", "Body", "Legs", "Address"])
for x in folder:
    liss.append(x)
for x in liss:
    try:
        browser.click_button('OK')
        browser.select_from_list_by_value('head', f'{x["Head"]}')
        browser.select_radio_button('body', f'{x["Body"]}')
        browser.input_text('//html/body/div/div/div[1]/div/div[1]/form/div[3]/input', f'{x["Legs"]}')
        browser.input_text('address', f'{x["Address"]}')
        browser.click_button('//*[@id="preview"]')
        browser.click_button('//*[@id="order"]')
        while True:
            try:
                browser.find_element("order-another")
                break
            except:
                browser.click_button("order")
        browser.wait_until_element_is_visible('//*[@id="receipt"]')
        fil = browser.get_element_attribute(locator='//*[@id="receipt"]',attribute="outerHTML")
        pdf.html_to_pdf(fil , output_path = f'{os.getcwd()}/output/robot+{x["Order number"]}.pdf')
        browser.wait_until_element_is_visible('//*[@id="robot-preview-image"]/img[1]')
        browser.wait_until_element_is_visible('//*[@id="robot-preview-image"]/img[2]')
        browser.wait_until_element_is_visible('//*[@id="robot-preview-image"]/img[3]')
        browser.screenshot('robot-preview-image', f'output/bot+{x["Order number"]}.png')
        # list_of_files = [
        #       f'output/bot+{x["Order number"]}.png'
        # ]
        pdf.add_watermark_image_to_pdf(
            image_path = f'output/bot+{x["Order number"]}.png',
            source_path = f'{os.getcwd()}/output/robot+{x["Order number"]}.pdf',
            output_path = f'{os.getcwd()}/output/robot+{x["Order number"]}.pdf')
        browser.click_button('order-another')
    except:
        pass
lib.archive_folder_with_zip('./output', './output/output.zip', recursive=True)
lib.list_archive('./output/output.zip')
print("Done")

print("Finally create new file")