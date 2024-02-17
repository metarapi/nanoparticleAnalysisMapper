# LA-sp-ICP-MS Analysis Mapper

This webapp packages the complex data processing of data produced by LA-single particle-ICP-MS into a more user friendly format.
The data is processed using a series of python scripts and the results are displayed in a webapp.
The webapp is built using the Django framework and is hosted on a local server. It also uses daphne to allow for asynchronous processing of the data.
The displaying is handled with the help of the plotly library, specifically the django-plotly-dash library.

## Installation

This project uses pip and Python. To install the necessary dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## 

## Docker image and building

To build a Docker image, simply execute the following command:

```sh
docker build -t np-analysis-mapper-image .
```

The dependencies required for this project are precompiled for both Windows-amd64 and Linux-amd64 architectures. Additionally, a Docker image tailored for Linux environments is readily available [here](https://hub.docker.com/r/metarapi/nanoparticle-analysis-mapper/tags), allowing for deployment and execution.

```sh
docker pull metarapi/nanoparticle-analysis-mapper:v1.0
```

## Example dataset

If you're itching to dive in and try it out, we've got you covered with a sample dataset [here](https://dino64s.duckdns.org/s/bz8waMP6KPBpFHA). It's ready to roll and should give you some solid results for testing.
