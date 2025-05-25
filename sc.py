import asyncio
import json
import csv
import logging
from playwright.async_api import async_playwright, TimeoutError

# Configuration
CONFIG = {
    "BASE_URL": "https://rera.odisha.gov.in/projects/project-list",
    "OUTPUT_JSON_FILE": "rera_projects.json",
    "OUTPUT_CSV_FILE": "rera_projects.csv",
    "MAX_PROJECTS": 6,  # Limit to first 6 projects
    "PAGE_TIMEOUT": 60000,  # Navigation timeout (ms)
    "WAIT_AFTER_LOAD": 2000,  # Wait time after page load (ms)
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def scrape_project_details(page, project_url, project_index):
    try:
        logger.info(f"Navigating to project {project_index} details: {project_url}")
        await page.goto(project_url, timeout=CONFIG["PAGE_TIMEOUT"])
        await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])

        # Extract project details from the main details page
        rera_regd_no = ""
        project_name = ""
        try:
            rera_regd_no_elem = await page.query_selector("label.label-control:has-text('RERA Regd. No.') + strong")
            rera_regd_no = await rera_regd_no_elem.inner_text() if rera_regd_no_elem else "N/A"
            rera_regd_no = rera_regd_no.split(":")[-1].strip() if ":" in rera_regd_no else rera_regd_no
        except Exception as e:
            logger.warning(f"Failed to extract Rera Regd. No for project {project_index}: {e}")

        try:
            project_name_elem = await page.query_selector("label.label-control:has-text('Project Name') + strong")
            project_name = await project_name_elem.inner_text() if project_name_elem else "N/A"
            project_name = project_name.split(":")[-1].strip() if ":" in project_name else project_name
        except Exception as e:
            logger.warning(f"Failed to extract Project Name for project {project_index}: {e}")

        # Navigate to Promoter Details tab
        try:
            promoter_tab = await page.query_selector("a#ngb-nav-1[ngbNavLink]")
            if promoter_tab:
                await promoter_tab.click()
                await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])
            else:
                logger.warning(f"Promoter Details tab not found for project {project_index}")
        except Exception as e:
            logger.error(f"Failed to access Promoter Details tab for project {project_index}: {e}")
            return {
                "Rera Regd. No": rera_regd_no,
                "Project Name": project_name,
                "Promoter Name": "N/A",
                "Address of the Promoter": "N/A",
                "GST No": "N/A"
            }

        # Extract promoter details
        promoter_name = ""
        promoter_address = ""
        gst_no = ""
        try:
            promoter_name_elem = await page.query_selector("label.label-control:has-text('Company Name') + strong")
            promoter_name = await promoter_name_elem.inner_text() if promoter_name_elem else "N/A"
            promoter_name = promoter_name.split(":")[-1].strip() if ":" in promoter_name else promoter_name
        except Exception as e:
            logger.warning(f"Failed to extract Promoter Name for project {project_index}: {e}")

        try:
            address_elem = await page.query_selector("label.label-control:has-text('Registered Office Address') + strong")
            promoter_address = await address_elem.inner_text() if address_elem else "N/A"
            promoter_address = promoter_address.split(":")[-1].strip() if ":" in promoter_address else promoter_address
        except Exception as e:
            logger.warning(f"Failed to extract Promoter Address for project {project_index}: {e}")

        try:
            gst_elem = await page.query_selector("label.label-control:has-text('GST No.') + strong")
            gst_no = await gst_elem.inner_text() if gst_elem else "N/A"
            gst_no = gst_no.split(":")[-1].strip() if ":" in gst_no else gst_no
        except Exception as e:
            logger.warning(f"Failed to extract GST No for project {project_index}: {e}")

        return {
            "Rera Regd. No": rera_regd_no,
            "Project Name": project_name,
            "Promoter Name": promoter_name,
            "Address of the Promoter": promoter_address,
            "GST No": gst_no
        }
    except TimeoutError as e:
        logger.error(f"Timeout for project {project_index}: {e}")
        return {
            "Rera Regd. No": "N/A",
            "Project Name": "N/A",
            "Promoter Name": "N/A",
            "Address of the Promoter": "N/A",
            "GST No": "N/A"
        }
    except Exception as e:
        logger.error(f"Failed to scrape project {project_index}: {e}")
        return {
            "Rera Regd. No": "N/A",
            "Project Name": "N/A",
            "Promoter Name": "N/A",
            "Address of the Promoter": "N/A",
            "GST No": "N/A"
        }

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headless mode
        context = await browser.new_context()  # Deny geolocation
        page = await browser.new_page()

        try:
            logger.info(f"Navigating to project list: {CONFIG['BASE_URL']}")
            await page.goto(CONFIG["BASE_URL"], timeout=CONFIG["PAGE_TIMEOUT"])
            await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])

            # Locate View Details links
            
            view_details_links = await page.query_selector_all("a.btn.btn-primary:has-text('View Details')")
            if not view_details_links:
                logger.error("No View Details links found on the page")
                await browser.close()
                return

            # Limit to first 6 projects
            view_details_links = view_details_links[:CONFIG["MAX_PROJECTS"]]
            logger.info(f"Found {len(view_details_links)} View Details links to process")

            # Scrape each project's details
     

 
                    # Scrape each project's details
            for i in range(1, CONFIG["MAX_PROJECTS"] + 1):
                try:
                    logger.info(f"Clicking View Details for project {i}")
                    # Ensure the project list is loaded
                    await page.wait_for_selector("a.btn.btn-primary:has-text('View Details')", timeout=10000)
                    # Fetch the View Details link for the current project
                    view_details_links = await page.query_selector_all("a.btn.btn-primary:has-text('View Details')")
                    if i > len(view_details_links):
                        logger.error(f"No View Details link found for project {i}")
                        break
                    link = view_details_links[i - 1]  # Get the i-th link
                    # Check for and close SweetAlert2 modal if present
                    modal_close_button = await page.query_selector("div.swal2-container button.swal2-confirm:has-text('OK')")
                    if modal_close_button:
                        logger.info(f"Found SweetAlert2 modal for project {i}, attempting to close")
                        await modal_close_button.click()
                        await page.wait_for_selector("div.swal2-container", state="hidden", timeout=5000)
                        logger.info(f"Modal closed for project {i}")
                    else:
                        logger.info(f"No SweetAlert2 modal found for project {i}")
                    # Ensure the View Details button is visible
                    await link.wait_for_element_state("visible", timeout=10000)
                    # Click the View Details button and wait for navigation
                    async with page.expect_navigation(timeout=CONFIG["PAGE_TIMEOUT"]):
                        await link.click()
                    await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])
                    # Pass the current page URL after navigation
                    project_data = await scrape_project_details(page, page.url, i)
                    results.append(project_data)
                    # Navigate back to the project list
                    await page.goto(CONFIG["BASE_URL"], timeout=CONFIG["PAGE_TIMEOUT"])
                    await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])
                except Exception as e:
                    logger.error(f"Failed to process View Details for project {i}: {e}")
                    project_data = {
                        "Rera Regd. No": "N/A",
                        "Project Name": "N/A",
                        "Promoter Name": "N/A",
                        "Address of the Promoter": "N/A",
                        "GST No": "N/A"
                    }
                    results.append(project_data)
                    # Navigate back to the project list to continue with the next project
                    await page.goto(CONFIG["BASE_URL"], timeout=CONFIG["PAGE_TIMEOUT"])
                    await page.wait_for_timeout(CONFIG["WAIT_AFTER_LOAD"])

                    
        except TimeoutError as e:
            logger.error(f"Timeout accessing project list: {e}")
        except Exception as e:
            logger.error(f"Error accessing project list: {e}")
        finally:
            await browser.close()

    # Save to JSON
    try:
        with open(CONFIG["OUTPUT_JSON_FILE"], "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved results to {CONFIG['OUTPUT_JSON_FILE']}")
    except Exception as e:
        logger.error(f"Failed to save JSON file: {e}")

    # Save to CSV
    try:
        with open(CONFIG["OUTPUT_CSV_FILE"], "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["Rera Regd. No", "Project Name", "Promoter Name", "Address of the Promoter", "GST No"]
            )
            writer.writeheader()
            writer.writerows(results)
        logger.info(f"Saved results to {CONFIG['OUTPUT_CSV_FILE']}")
    except Exception as e:
        logger.error(f"Failed to save CSV file: {e}")

if __name__ == "__main__":
    asyncio.run(main())