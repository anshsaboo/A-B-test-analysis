import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set seed for reproducibility so your portfolio results are stable
np.random.seed(42)

# 1. Generate Users
num_users = 10000
user_ids = range(1, num_users + 1)
regions = ['NA', 'EU', 'LATAM', 'APAC']
plan_types = ['free', 'premium', 'family']

users = pd.DataFrame({
    'user_id': user_ids,
    'signup_date': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365)) for _ in range(num_users)],
    'region': np.random.choice(regions, num_users, p=[0.4, 0.3, 0.2, 0.1]),
    'plan_type': np.random.choice(plan_types, num_users, p=[0.6, 0.3, 0.1])
})

# 2. Generate Experiment Assignments
groups = ['control', 'treatment']
experiment_assignments = pd.DataFrame({
    'user_id': user_ids,
    'test_group': np.random.choice(groups, num_users, p=[0.5, 0.5]),
    'assignment_date': [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 14)) for _ in range(num_users)]
})

# 3. Generate Events
events_data = []
for _, row in experiment_assignments.iterrows():
    uid = row['user_id']
    group = row['test_group']
    assignment_date = row['assignment_date']
    
    # We bake in a slight uplift for the treatment group
    engage_prob = 0.6 if group == 'control' else 0.65
    convert_prob = 0.2 if group == 'control' else 0.24 
    
    # Did they engage? (e.g., listened to an autoplayed song)
    if np.random.rand() < engage_prob:
        event_date = assignment_date + timedelta(days=np.random.randint(0, 7))
        session_length = np.random.normal(loc=30, scale=10) if group == 'control' else np.random.normal(loc=35, scale=12)
        
        # Did they convert? (e.g., liked the song)
        converted = 1 if np.random.rand() < convert_prob else 0
        
        events_data.append({
            'user_id': uid,
            'event_type': 'autoplay_listen',
            'event_date': event_date,
            'session_length': round(max(1, session_length), 2),
            'converted': converted
        })

events = pd.DataFrame(events_data)

# Export to CSV so you can load them into your SQL database
users.to_csv('users.csv', index=False)
experiment_assignments.to_csv('experiment_assignments.csv', index=False)
events.to_csv('events.csv', index=False)