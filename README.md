## About
This program calculates the number of train required to cover a given train service schedule.

I was curious about the trainset utilization rate of [Taiwan High Speed Rail](https://www.thsrc.com.tw/index.html), thus decided to write a program to answer this question.
## Usage
### Program usage
#### Given Service timetable with a list of possible positioning trains
```bash
python3 main.py <service-timetable> <positioning-train-library>
```
- [*service-timetable*](#service-timetable): file name of a timetable located in ```data/``` folder
- [*positioning-train-library*](#positioning-train-library): file name of a list of all possible positioning trains, located in ```data/``` folder.

The alogrithm will choose a set of trains from the positioning train list to minimize the required train sets to cover the whole service timetable.
#### Given Service timetable, without positioning train list
```bash
python3 approxmain.py <service-timetable>
```
Without a specified list of possible positioning trains, the algorith assumes that a trainset can be positioned anytime within the following times:
- Nangang ⇄ Taichung: 60 minutes
- Taichung ⇄ Zuoying: 50 minutes
### Data file format
#### service timetable
Each line consists a train with the format:\
```<train number> <origin-station> <origin-time> <destination> <destination-time>```\
e.g: ```1202 ZUY 06:30 NAG 08:20```
#### positioning train library:
Each line consists a positioning train with the format:\
```<train number> <origin-station> <origin-time> <destination> <destination-time> <conflict-trains>```\
e.g: ```1455 NAG 20:30 TAC 21:30 1557```

*conflict-trains* is a list of conflicting service trains (specified by train number, seperated by space), , the algorithm will avoid selecting this positioning train when the service trains list contains a train in conflict.

**Tip:** To get better results, Split Nangang ⇄ Zuoying positioning trains into two legs, Nangang ⇄ Taichung and Taichung ⇄ Zuying, respectively. Leave it to the algorithm to decide whether to position a trainset all the way back to Nangang/Zuoying or just to Taichung. 

### Utility scripts
#### Timetable crawler
A script to crawl the timetable down from THSR's website.

(Requires python3.6 and pipenv)

```bash
pipenv --python 3.6
pipenv install
pipenv shell
python timetable-crawler.py <YYYYMMDD>
```
### Train generator
A interactive script for generating train schedule list (Helpful for generating positioning train lists for peroidic timetables)

```bash
python3 train-generator.py
```
## Fun facts

## Algorithm
## Useful resources
