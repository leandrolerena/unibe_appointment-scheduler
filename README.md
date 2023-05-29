# Appointment Scheduler

This repository contains a MILP for an appointment scheduler developed for the 'seminar applied optimization' at University of Bern. 

## How to use

First, make sure you have a (virtual) environment up and running. Pipenv the preferred way. In this case, just run

```shell
pipenv install
```

For any other case, there is also a generated `requirements.txt` file


### Run the optimizer with random data

```shell
python main.py
```

### Reproduce my experiments shown in presentation

```shell
python scenario_concentrated_on_500.py
python scenario_no_preferences.py
python scenario_random_concentration.py
python scenario_random_intervals.py
```

You will get the solution as console output and **plots** (see the `out/` directory!)

## Misc

### Create/Update requirements.txt 

Pipenv is used for managing dependencies. However, we can extract a requirements.txt file for users who would like to use another environment.

```shell
pipenv requirements > requirements.txt
```