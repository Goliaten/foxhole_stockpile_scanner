# Processes
The main proces:
- controls mouse and gathers screenshots
3 subprocessees:
- selenium - simulates website. Accesses the fir website, puts images and clicks the process button.
- fir - server hosting the screenparsing
- flask - receives processed images sent by a modified fir

# Pipeline
- main process manuevers onto the map and gathers screenshots
- selenium process loads them and puts them into fir, and marks the screenshots as processed
- fir detects stockpile and parses it, then sends it to a specified port
- flask receives that data and saves it into .csv