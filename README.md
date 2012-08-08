# riaalabels.json
* **Purpose**: Generate a graph of RIAA affiliated record labels represented in JSON
* **Written in**: Python

## Installation

### Requirements
* All the requirements to set up a MusicBrainz database
* Python 2 and modules below
 * psycopg2 (`pip install psycopg2`)
 * neo4j-embedded (`pip install neo4j-embedded`)

### Set up
* Set up a MusicBrainz database
* Clone this project
* Check `lib/mbz.py` to make sure the PostgreSQL MusicBrainz credentials are correct

## Usage
* With logging: `python run.py`
* Suppress logging: `python run.py -q` or `python run.py --quiet` 

After a minute or so, the process will be finished and the output will be written to `riaalabels.json`
