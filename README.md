# GetSatelliteImages

As the name suggests, *GetSatelliteImages* eases the task of retrieving satellite imagery, specifically that offered by the folks at the ESA. All this repository does is manage the usage of their API, which may seem a little too complicated at first but once you dig deep into it you realize that it has great potential.

The main objective of this repository is to baseline the retrieval of images, as there is a long list of attributes and data to manage so this little interface seemed as a great idea.


## Dependencies

This project has been developed in Python 3.10.12, there is no guaranteess that it works in any other version.

The necesary packages are specified in the correponding *requirements.txt* file

## First steps

The fist and main step is to register into the [Copernicus](https://dataspace.copernicus.eu/) website.

After you are registered, set both your username/email and password of registration as the following environment variables:

    -`COPERNICUS_USERNAME`

    -`COPERNICUS_PASSWORD`
