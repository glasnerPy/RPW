import numpy as np
import pandas as pd
import networkx as nx
import math
import matplotlib.pyplot as plt


# Function to assign activities to stations based on maximum time
def assign_activities_to_stations(df, maximum_time):
    assigned_stations = {}
    station_idx = 1

    # Sort the DataFrame based on 'total' column in descending order
    df = df.sort_values(by='total', ascending=False).reset_index(drop=True)

    # Create a string representation of the order of RPW flow
    activity_str = '->'.join(df['Activity'])
    print('The order of the RPW flow is:', activity_str, '\n')

    for index, row in df.iterrows():
        if not assigned_stations:
            assigned_stations[station_idx] = [row['Activity'], row['Durations']]
        elif assigned_stations[station_idx][1] + row['Durations'] <= maximum_time:
            assigned_stations[station_idx][0] += row['Activity']
            assigned_stations[station_idx][1] += row['Durations']
        else:
            station_idx += 1
            assigned_stations[station_idx] = [row['Activity'], row['Durations']]

    return assigned_stations


# Function to create a weighted graph and calculate total durations
def create_weight_node(df):
    durations = df.set_index('Activity')['Durations']
    G = nx.from_pandas_edgelist(df.explode('Predecessor').fillna('Root'),
                                create_using=nx.DiGraph,
                                source='Predecessor', target='Activity')

    paths = {}
    for node in df['Activity']:
        paths[node] = None
        for r_node in df['Activity']:
            if node != r_node:
                # Find all simple paths between two nodes in the graph
                path = next((path for path in nx.all_simple_paths(G, source=node, target=r_node) if path is not None),
                            None)
                if path is not None:
                    if paths[node] is None:
                        paths[node] = path
                    else:
                        paths[node] += path

    for index, row in df.iterrows():
        if paths[row['Activity']] is not None:
            # Calculate the total duration for activities with predecessors
            df.loc[index, 'total'] = sum(durations.get(activity) for activity in paths[row['Activity']])
        else:
            # If there are no predecessors, use the original duration
            df.loc[index, 'total'] = durations.get(row['Activity'])

    return df, G


if __name__ == '__main__':
    units = 'm'
    quantity_per_day, working_day_hours = 50, 8

    # Input validation loop for working hours, quantity, and units
    while True:
        try:
            working_day_hours = float(input('Enter the hours in a working day: '))
            quantity_per_day = int(input('Enter the quantity expected in a day: '))
            units = input('Enter the activity\'s units (h=hours, m=minutes, s=seconds): ')
        except ValueError:
            print('Invalid input. Please enter valid numbers and units.')
            continue

        if 1 <= working_day_hours <= 24 and units in ['h', 'm', 's']:
            break
        else:
            print('Valid range for working hours: 1-24')
            print('Valid activity\'s units: h, m, or s')

    # Calculate the lifecycle based on units and quantity
    if units == 'm':
        lifecycle = (working_day_hours * 60) / quantity_per_day
    elif units == 's':
        lifecycle = (working_day_hours * 60 * 60) / quantity_per_day
    else:
        lifecycle = working_day_hours / quantity_per_day

    print(f'The lifecycle for each station is: {lifecycle:.2f} {units}')
    lifecycle = math.floor(lifecycle)
    print(f'Hence, each station\'s lifecycle will not exceed: {lifecycle} {units}')

    # Define activity data
    Activity = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    Predecessor = [None, 'A', 'A', 'B', 'B', 'C', 'C', ['D', 'E'], ['F', 'G']]
    Durations = [40, 35, 50, 35, 7, 25, 12, 23, 18]

    # Create a DataFrame from activity data
    df = pd.DataFrame({'Activity': Activity, 'Predecessor': Predecessor, 'Durations': Durations})

    # Add weight to each activity based on RPW method
    df, G = create_weight_node(df)

    # Calculate the theoretical optimal number of stations
    opt_stations = math.ceil(df['Durations'].sum() / lifecycle)
    print(f'The theoretical optimal stations to open is: {opt_stations} based on lifecycle: {lifecycle} {units}\n')

    # Assign activities to stations
    stations = assign_activities_to_stations(df, lifecycle)
    stations_df = pd.DataFrame.from_dict(stations)
    print('RPW method will divide the activities into the following stations:')
    print(stations_df)

    # Define node positions for network diagram visualization
    pos = nx.spring_layout(G)

    # Draw the graph
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10, font_color='black',
            font_weight='bold', arrowsize=15)

    # Add node duration labels
    labels = {row['Activity']: row['Durations'] for _, row in df.iterrows()}
    label_pos = {k: (v[0], v[1] + 0.1) for k, v in pos.items()}

    nx.draw_networkx_labels(G, label_pos, labels=labels, verticalalignment='bottom')

    plt.title('Project Network Diagram')
    plt.axis('off')
    plt.show()
