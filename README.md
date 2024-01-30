# LA-sp-ICP-MS Analysis Mapper

This webapp packages the complex data processing of data produced by LA-single particle-ICP-MS.
The data is processed using a series of python scripts and the results are displayed in a webapp.
The webapp is built using the Django framework and is hosted on a local server. It also uses daphne to allow for asynchronous processing of the data.
The displaying is handled with the help of the plotly library, specifically the django-plotly-dash library.

## Installation

This project uses pip and Python. To install the necessary dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## Running the Project

To run the project, use the provided batch script.
