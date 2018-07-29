# ml_board
---
I decided to create this machine learning dashboard for my own personal usage after using [tensorboardX](https://github.com/lanpa/tensorboardX). As great as tensorboardX was, I found myself using only a subset of its features, 

design choices,etc...
### Limitations of Tensorboard
* text is kinda buggy-> can't trust if text log corresponds with that run
* have to remember hyperparameter setings for each run
* no way to filter by hyperparameter/test score
### Why Mongo
* mongo allows you to change data structure after the fact
    * useful when one of the runs is invalid b/c you forgot to update a field
* Seperates log from code:logging to the local directoy takes up space in my git repo. Even if I put the directoy's name in a gitignore file, I would prefer the logs to not be in the same directory as my code, because my code is synced with Dropbox, and I only have 2 GB of it -> 
* Move data structures around, so more atomic than pickle objects
### Why Plotly
* Can isolate traces(not typical in interactive)
* Can pan
* Can zoom
* can label legend by hyperparameter so I can do random search
* way more extensible because I wrote it myself, so I have a way better mental model of how my code works.
### Design Choices
* I only allow one idenitifer in the dropdown menu b/c I did the want the plot's legend and images/histograms titles to be cluttered
* This is extensible b/c theres no complicated shit...
### Concerns
* if autoUpdate is on, do not filter rows as it will be overwritten
* don't click on the filter rows button twice, or it will filter permemantly. If this does happen, refresh the webpage to reset the app's state.
* Only filter table when on Plots Tab

# Installation
---
```
git clone https://github.com/bbli/ml_board.git
cd ml_board
conda create -n ml_board python=3.6.6 pip
pip install .
```
If something goes wrong during usage, and you can't debug it, you can try installing the exact versions this package was tested on by:
1. Commenting out the `install_requires` field in setup.py
2. run `pip install -r requirements.txt && pip install .`

# Usage
---
## Logging
```
from ml_board import SummaryWriter
```

## Visualizing
```
ml_board --database_name name_of_mongodb_database --folder_name name_of_mongo_db_collection
# shorthand notation
ml_board --d name_of_mongodb_database --f name_of_mongo_db_collection
# specific port. Default 8000
ml_board --d name_of_mongodb_database --f name_of_mongo_db_collection -p 8050
```
pics of dashboard


# TODO
---
* allow user to change folders from within the dashboard
