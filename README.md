# RAG2 integration test

## Overview

This is a testing tool for visualisation of data flow in framework created for RAG2 project
(integrating web minigames with remote AI models) using abstract websocket definition.

## Prerequisities

1. Node v20
2. Python 3.11
3. PIP

## Usage

1. Copy `example.env` file into new file `.env` in main directory, enter your actual NODE path in it
2. In `./client` directory run `npm install` command
3. In main directory run `pip install -r requirements.txt`
4. Run `main.py` file

## Test caes

Test cases (names, inputs and assertions) are defined in list of objects in `main.py` file.
