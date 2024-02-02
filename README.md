# JBI100-Group-50-app

## About this app
This is the visualisation app of group 50. It is based on the provided template and uses the libraries specified
in the requirements.txt file.

## Get the app

### Clone the repository
This app can either be mounted locally or cloned from the remote repository. To clone the repository, use the following command:
```
gh repo clone golsarp/Visualisation
```
### Mount the app locally
To mount the app locally, download the zip file from the repository and extract it to a folder of your choice. 
Then open a command prompt and navigate to the folder where the app is located.

## Requirements

* This app has been developed in Python 3.9.18. You can set up a virtual environment and the interpreter 
with this version of Python using tools such as [conda](https://conda.io/projects/conda/en/latest/).

* This app requires the following libraries:
  * [Dash](https://dash.plot.ly/)
  * [Pandas](https://pandas.pydata.org/)
  * [Plotly](https://plotly.com/python/)
  * [Numpy](https://numpy.org/)

  You can install these libraries in the correct versions using pip:
    ```
    pip install -r requirements.txt
    ```

## How to run this app
The entrance point of the app is the file app.py. To run the app, open a command prompt and navigate to the folder where the app is located. Then run the following command:
```
> python app.py
```
You will get a http link, open this in your browser to see the results.

## How to use this app
The instruction video for the app can be found on [YouTube](https://youtu.be/sIYFBSFhA4w?feature=shared).

## Potential issues and how to fix them
We have observed that on some machines the bench tables do not initialize every time. In case that is the case for you,
there are two causes of actions which you can take.
* Toggle the home team and away team dropdown. This will force the tables to reinitialize.
* Increase the sleep in the callback functions for the benches in the app.py file.
This will give the tables more time to initialize.

## Authors of the app
This app was developed by the group members of group 50. There are no resources implemented from external sources beyond
the libraries specified in the requirements.txt file and the template provided by the course coordinators.