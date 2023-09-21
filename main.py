import numpy
import pandas as pd
import networkx as nx


def create_network_levels(df):
    # Create a directed graph from the DataFrame
    G = nx.from_pandas_edgelist(df.explode('Predecessor').fillna('Root'),
                                create_using=nx.DiGraph,
                                source='Predecessor', target='Activity')

    # Initialize a dictionary to store the paths for each node
    paths = {}

    # Get durations as a dictionary for quick access
    durations = df.set_index('Activity')['Durations'].to_dict()

    # Calculate paths and total durations for each node
    for node in df['Activity']:
        paths[node] = None
        for r_node in df['Activity'][::-1]:
            for path in nx.all_simple_paths(G, source=node, target=r_node):
                if path is None:
                    paths[node] = [node]
                elif paths[node] is None:
                    paths[node] = path
                else:
                    paths[node] += path

        # Remove duplicates from the path and calculate total duration
        paths[node] = list(dict.fromkeys(paths[node])) if paths[node] is not None else ["--"]
        total_duration = sum(durations.get(activity, 0) for activity in paths[node])

        # Update the DataFrame with the total duration
        df.loc[df['Activity'] == node, 'total'] = total_duration

    return df
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #df = pd.read_csv("/home/yuval/Downloads/Activity.csv")
    #df = convert_df(df)
    #df = df.astype({"Durations": 'int'})
    #print(df.dtypes)
    #print(df)
    Activity = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    Predecessor = [None, 'A', 'A', 'B', 'B', ['C', 'E'], 'D', 'F', ['D', 'E'], ['G', 'H', 'I']]
    Durations = [4, 5, 4, 4, 7, 2, 6, 3, 5 ,2]
    df = pd.DataFrame(zip(Activity, Predecessor, Durations),
                      columns=['Activity', 'Predecessor', 'Durations'])
    df_levels = create_network_levels(df)
    print(df_levels)

