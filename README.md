# RPW (Ranked Positional Weight)
# Project Name

Project Description

## Overview

This project provides a Python script for optimizing resource allocation in project scheduling using the RPW (Ranked Positional Weight) method. The script takes a list of project activities, their predecessors, and durations as input and calculates the optimal number of stations to allocate the activities efficiently while considering resource constraints.

## Input Requirements

To use this script, you will need to provide the following input:

1. **Working Day Hours**: Enter the total number of hours in a working day (1-24 hours).
2. **Quantity Expected in a Day**: Specify the quantity of units expected to be completed in a single working day.
3. **Activity Units**: Choose the units in which the activity durations are measured (h=hours, m=minutes, s=seconds).
4. **Activity Data**: Define the project activities, their predecessors (if any), and their respective durations in the code. See the code section labeled "Define activity data" for an example of how to format this data.

## Output

The script provides the following output:

1. **Optimal Stations**: It calculates and displays the theoretical optimal number of stations to open based on the RPW method, considering the lifecycle of each station.
2. **Station Assignment**: The RPW method assigns activities to stations while optimizing resource utilization. The assignment results, including the order of activities in each station and the total duration for each station, are displayed.
3. **Project Network Diagram**: A visual representation of the project network diagram is generated and displayed using NetworkX and Matplotlib. This diagram shows the flow of activities, their dependencies, and duration labels for better project visualization.

## RPW (Ranked Position Weight) Method

The RPW method is a resource allocation technique used in project scheduling. It optimizes resource allocation by considering the following factors:

- Activity durations
- Predecessor activities
- Available working hours
- Expected quantity of work in a day
- Activity units (hours, minutes, seconds)

The method ranks activities based on their importance and assigns them to stations in such a way that the resource constraints are met while minimizing idle time and maximizing efficiency.

## Usage

To use the script, follow these steps:

1. Clone this repository to your local machine.
2. Open the script file and provide the required input (working day hours, quantity per day, activity units, and activity data).
3. Run the script in a Python environment.
4. Review the script's output, which includes the optimal number of stations and the station assignment for each activity.
5. A visual representation of the project network diagram will be displayed.

## Contributors

- [Yuval Glasner]

## License

No license needed


