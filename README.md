# ml_board
### Limitations of Tensorboard
I decided to create this machine learning dashboard for my own personal usage after using [tensorboardX](https://github.com/lanpa/tensorboardX). As great as tensorboardX was in helping me debug and understand neural networks(it certainly beats printing out statistics in the terminal), I found myself using only a subset of its features, and also found some certain annoyances about tensorboard

* **Text is buggy**: The text tab will sometimes take a long time to load, or it will load the text from another run. When training a machine learning model, I often go through many settings and test various hypotheses. So having a reliable log is a must.
* **Disconnect between visualization and settings**: My hypotheses often involve varying a hyperparameter and seeing its effect on quantities such as the loss, percentage of activations, etc. But the graphs don't have a legend that tells me which the setting each run used. As a result, I am forced to go back and forth between the Scalars and Text tab, interrupting my train of thought.
* **Inadequate search**: Suppose I wanted to view all the runs that achieved a certain accuracy, or were run on a particular hyperparameter setting. As far as I know, this is not possible in tensorboard. 

### Why Mongo
* mongo allows you to change data structure after the fact
    * useful when one of the runs is invalid b/c you forgot to update a field
* Seperates log from code:logging to the local directoy takes up space in my git repo. Even if I put the directoy's name in a gitignore file, I would prefer the logs to not be in the same directory as my code, because my code is synced with Dropbox, and I only have 2 GB of it -> 
* Move data structures around, so more atomic than pickle objects
### Why Plotly/Dash
* Can isolate traces(not typical in interactive)
* Can pan
* Can zoom
* can label legend by hyperparameter so I can do random search
* way more extensible because I wrote it myself, so I have a way better mental model of how my code works.
### Design Choices
* I only allow one idenitifer in the dropdown menu b/c I did the want the plot's legend and images/histograms titles to be cluttered

# Installation
Until the tabs feature is integrated into the master branch of [dash](https://github.com/plotly/dash), and I do more testing, and write up the documentation, you will have to manually install the package with the following command.
```
git clone https://github.com/bbli/ml_board.git
cd ml_board
conda create -n ml_board python=3.6.6 pip
pip install .
```
If something goes wrong during usage, and you can't debug it, you can try installing the exact versions this package was tested on:
1. Commenting out the `install_requires` field in setup.py
2. run `pip install -r requirements.txt && pip install .`

# Usage
## Logging
Usage is more or less the same as tensorboard. One noticeable difference is that there is no need to specify a count, as ml_board will append the result to a MongoDB list. The other is that ml_board has an additional `add_experimental_parameter` which is intended to log hyperparameters to a table
```
from ml_board import SummaryWriter
w= SummaryWriter('name_of_mongodb_database','name_of_mongo_db_collection')

w.add_scalar("Loss",loss)
w.add_histogram()
w.add_image("Segmentation",2d_numpy_matrix_in_range_0_to_1)
w.add_thought("your_thoughts")
w.add_experimental_parameter("Hyperparameter",)
w.close()
```
For more details, look at the `Logger.py` file in the ml_board folder
## Visualizing
```
ml_board --database_name name_of_mongodb_database --folder_name name_of_mongo_db_collection
# shorthand notation
ml_board --d name_of_mongodb_database --f name_of_mongo_db_collection
# specific port. Default 8000
ml_board --d name_of_mongodb_database --f name_of_mongo_db_collection -p 8050
```
pics of dashboard on top??
## Concerns
* if autoUpdate is on, do not filter rows as it will be overwritten
* don't click on the filter rows button twice, or it will filter permemantly. If this does happen, refresh the webpage to reset the app's state.
* Only filter table when on Plots Tab


# TODO
* allow user to change folders from within the dashboard
* testing/documentation
