# Appointment Scheduler

This repository contains a MILP for an appointment scheduler developed for the 'seminar applied optimization' at University of Bern. 

Note that in the source code, the entity for a service is 'Queue'. This is because I want to add some properties of queues to make the time-slot assignments more fair.

**this project uses python 3.11. If you don't have python 3.11 installed, you may want to run it in docker (see at the bottom of this file)**

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

### Run within docker

It is also possible to run within docker. However, if you don't map a directory to `out/`, you will not be able to view the plots.

First: Build image
```shell
docker build . -t appointment-scheduler
```

Then, run either completely isolated
```shell
docker run -it --entrypoint bash appointment-scheduler
```

Or with a directory (here, your current working directory) to the out directory to get the plots
```shell
docker run -it --entrypoint bash -v ${PWD}:/app/out/ appointment-scheduler
```

### Create/Update requirements.txt 

Pipenv is used for managing dependencies. However, we can extract a requirements.txt file for users who would like to use another environment.

```shell
pipenv requirements > requirements.txt
```