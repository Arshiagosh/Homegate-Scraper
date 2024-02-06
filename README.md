# Real Estate Scraper and Analysis Application

This Python application is designed to scrape real estate data from the Homegate website, save it to MongoDB, and perform data analysis. The application includes a graphical user interface (GUI) for user input, a scraper module for data extraction, a MongoDB admin module for data storage, and a plotting module for data visualization and linear regression.

## Requirements

- Python 3.x
- Libraries: `os`, `sys`, `math`, `BeautifulSoup`, `requests`, `pandas`, `numpy`, `matplotlib`, `scikit-learn`

## Usage

1. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```
2. Create a local_settings.py (use sample_settings.py) file in the same directory as your script and define your MongoDB database configuration:
    ```python
   DATABASE = {
    'name': 'your_db_name',
    'host': 'your_host_server',
    'port': 27017,
    }
   ```
3. Run the program
    ```bash
   python main.py
   ```
   The GUI will prompt you to enter real estate search criteria such as type, category, city, kilometer radius, rooms, and price. Click the "Go!" button to initiate the scraping process.
3. Run the visualization program
    ```bash
   python plot.py
   ```
## Files

- **main.py**: Entry point of the application. Handles GUI interactions, initiates scraping, saves data to MongoDB, and save HTML content in `/HTML_Content`

- **plot.py**: Generates a scatter plot and performs linear regression on real estate data stored in MongoDB.

- **scraper.py**: Defines the `HomegateScraper` class responsible for fetching and parsing real estate data from the Homegate website.

- **gui.py**: Implements the GUI using the `tkinter` library for user input.

- **db_admin.py**: Manages the interaction with MongoDB, including saving and retrieving data.

- **local_settings.py**: Configuration file for the MongoDB database connection details.


## Functionality

- **GUI Input**: Allows users to input real estate search criteria.

- **Web Scraping**: Utilizes BeautifulSoup to scrape real estate data from the Homegate website.

- **MongoDB Integration**: Saves the scraped data to MongoDB for storage.

- **Data Plotting**: Generates a scatter plot and performs linear regression on the real estate data.

## Notes

- Please replace the placeholder values in `local_settings.py` with your actual MongoDB database connection details. Use the sample_settings.py for it.

- This application assumes the existence of a MongoDB database. Ensure that the database exists before running the application.