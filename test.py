import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

# Flag to control whether to skip experiments without interventions
skip_no_interventions = True

# Helper function to convert time strings to seconds
def time_to_seconds(time_str):
    h, m, s = map(float, time_str.split(':'))
    return int(h * 3600 + m * 60 + s)

# Load the CSV files
file_path_original = 'reduct-highlights-export.csv'
file_path_researcher = 'reduct-highlights-export (1).csv'
file_path_additional = 'reduct-highlights-export (2).csv'

original_df = pd.read_csv(file_path_original)
researcher_df = pd.read_csv(file_path_researcher)
additional_df = pd.read_csv(file_path_additional)

# Add Start and End columns for all dataframes
for df in [original_df, researcher_df, additional_df]:
    df['Start'] = df['Timestamp'].apply(time_to_seconds)
    df['Duration'] = df['Duration'].apply(time_to_seconds)
    df['End'] = df['Start'] + df['Duration']

# Loop through each unique experiment
for recording in original_df['Recording'].unique():
    # Filter data for the current experiment
    experiment_original = original_df[original_df['Recording'] == recording].copy()
    experiment_researcher = researcher_df[researcher_df['Recording'] == recording].copy()
    experiment_additional = additional_df[additional_df['Recording'] == recording].copy()

    # Filter the researcher dataframe for rows with Tags == "#green"
    researcher_filtered = experiment_researcher[experiment_researcher['Tags'] == '#green'].copy()

    # Skip experiments with no interventions if the flag is set to True
    if skip_no_interventions and researcher_filtered.empty:
        print(f"Skipping experiment: {recording} (no researcher interventions).\n")
        continue

    # Categorize participant's data
    experiment_original.loc[:, 'Category'] = experiment_original['Tags'].apply(
        lambda x: 'Required Help' if x == 'RH' else 'Confused'
    )

    # Determine the common x-axis range based on maximum End time
    max_time = max(
        experiment_original['End'].max(),
        researcher_filtered['End'].max() if not researcher_filtered.empty else 0,
        experiment_additional['End'].max() if not experiment_additional.empty else 0,
    )

    # Create the plot
    fig, ax = plt.subplots(figsize=(14, 6))

    # Use flags to avoid duplicate legend entries
    confused_label_added = False
    help_label_added = False
    additional_label_added = False

    # Plot participant confusion intervals (blue regions)
    for _, row in experiment_original[experiment_original['Category'] == 'Confused'].iterrows():
        ax.axvspan(
            row['Start'], row['End'], color='blue', alpha=0.3, label='Confused' if not confused_label_added else ""
        )
        confused_label_added = True

    # Plot participant required help intervals (red regions)
    for _, row in experiment_original[experiment_original['Category'] == 'Required Help'].iterrows():
        ax.axvspan(
            row['Start'], row['End'], color='red', alpha=0.3, label='Required Help' if not help_label_added else ""
        )
        help_label_added = True

    # Mark researcher intervention points (green dots)
    if not researcher_filtered.empty:
        ax.scatter(
            researcher_filtered['Start'], [0.5] * len(researcher_filtered), color='green', label='Researcher Intervention', zorder=5
        )

    # Add highlights from the third CSV as black regions
    black_highlights = []
    for _, row in experiment_additional.iterrows():
        highlight = ax.axvspan(
            row['Start'], row['End'], color='black', alpha=0.5, label='Additional Highlights' if not additional_label_added else ""
        )
        black_highlights.append((highlight, row['Tags']))
        additional_label_added = True

    # Customize the plot
    ax.set_xlim(0, max_time)
    ax.set_title(f"Participant Confusion, Help, Researcher Interventions, and Additional Highlights - {recording}")
    ax.set_xlabel("Time (seconds)")
    ax.set_yticks([])
    ax.legend()

    # Add tooltips for black highlights
    cursor = mplcursors.cursor(ax.patches, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        for highlight, tag in black_highlights:
            if sel.artist == highlight:
                sel.annotation.set_text(f"Tags: {tag}")
                break

    plt.show()
