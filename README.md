[![Build Status](https://travis-ci.org/sql-viewer/SQLGlimpse.svg?branch=master)](https://travis-ci.org/sql-viewer/SQLGlimpse)

# SQLGlimpse

Currently supports viewing of mysql workbench files. 
Integrated with travis CI, located on https://travis-ci.org/sql-viewer/sql-viewer

## How To Install

1. Install python3.4 (installed with pip)
2. From the repository folder run `pip3 install -r requirements.txt`

## How To Run

1. Run python migration `python3 manage.py migrate`
2. [Import model](#how-to-import-a-model)
3. `python3 manage.py runserver`
4. manage.py createsuperuser (to access the content)

## How To Contribute

Slack group link https://sql-viewer.slack.com/messages/general/


## How To Import A Model
`python3 manage.py import [path-to-model] [model-name] [model-version]`
Example > `python3 manage.py import ~/Documents/model.mwb DataModel 1`
