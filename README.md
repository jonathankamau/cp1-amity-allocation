[![Codacy Badge](https://api.codacy.com/project/badge/Grade/475f95a67aea4b2a9cef2d901d9b7e7d)](https://www.codacy.com/app/jonathankamau/cp1-amity-allocation?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jonathankamau/cp1-amity-allocation&amp;utm_campaign=Badge_Grade)
https://travis-ci.org/jonathankamau/cp1-amity-allocation.svg?branch=develop
# cp1-amity-allocation

DESCRIPTION 

AMITY ROOM ALLOCATION
Amity is a room allocation system for one of Andela's facilities.

CONSTRAINTS
Amity has rooms which can be offices or living spaces. An office can accommodate a maximum of 6 people. A living space can accommodate a maximum of 4 people.

A person to be allocated could be a fellow or staff. Staff cannot be allocated living spaces. Fellows have a choice to choose a living space or not.

This system will be used to automatically allocate spaces to people at random.

The building blocks are:

    Python 3.6.0
    SQLite DB

Setting Up for Development

These are instructions for setting up the Amity app in development environment.

    prepare directory for project code and virtualenv:

      $ mkdir -p ~/amity
      $ cd ~/amity

    prepare virtual environment (with virtualenv you get pip, we'll use it soon to install requirements):

      $ virtualenv --python=python3 amity-venv
      $ source hc-venv/bin/activate

    check out project code:

      $ git clone Setting Up for Development

These are instructions for setting up Amity app in development environment.

    prepare directory for project code and virtualenv:

      $ mkdir -p ~/amity
      $ cd ~/amity

    prepare virtual environment (with virtualenv you get pip, we'll use it soon to install requirements):

      $ virtualenv --python=python3 amity-venv
      $ source amity-venv/bin/activate

    check out project code:

      $ git clone https://github.com/jonathankamau/cp1-amity-allocation.git

    install requirements into virtualenv:

      $ pip install -r cp1-amity-allocation/requirements.txt

      Run the application using the following command:

      $ python app.py







