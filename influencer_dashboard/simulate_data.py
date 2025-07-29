import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

# 1. Simulate influencers
platforms = ['Instagram', 'YouTube', 'Twitter', 'Facebook']
categories = ['Fitness', 'Nutrition', 'Wellness', 'Lifestyle']
genders = ['Male', 'Female']

influencers = pd.DataFrame({
    'id': range(1, 21),
    'name': [f'Influencer_{i}' for i in range(1, 21)],
    'category': np.random.choice(categories, 20),
    'gender': np.random.choice(genders, 20),
    'followers': np.random.randint(5000, 500000, 20),
    'platform': np.random.choice(platforms, 20)
})
influencers.to_csv('influencers.csv', index=False)

# 2. Simulate posts
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)

posts = []
for _ in range(200):
    influencer_id = random.randint(1, 20)
    date = random_date(start_date, end_date)
    platform = influencers.loc[influencer_id - 1, 'platform']
    posts.append({
        'influencer_id': influencer_id,
        'platform': platform,
        'date': date.strftime('%Y-%m-%d'),
        'url': f'https://platform.com/post/{random.randint(1000,9999)}',
        'caption': f'Check out our latest product #{random.randint(1,50)}',
        'reach': random.randint(1000, 100000),
        'likes': random.randint(100, 5000),
        'comments': random.randint(5, 500)
    })

posts_df = pd.DataFrame(posts)
posts_df.to_csv('posts.csv', index=False)

# 3. Simulate tracking_data
products = ['MuscleBlaze Whey', 'HKVitals Omega', 'Gritzo Shake']
campaigns = ['Campaign_A', 'Campaign_B', 'Campaign_C']
sources = ['Instagram', 'YouTube', 'Twitter']

tracking_data = []
for _ in range(1000):
    influencer_id = random.randint(1, 20)
    user_id = random.randint(1000, 9999)
    product = random.choice(products)
    date = random_date(start_date, end_date)
    orders = random.randint(1, 3)
    revenue = round(orders * random.uniform(300, 2000), 2)
    tracking_data.append({
        'source': influencers.loc[influencer_id - 1, 'platform'],
        'campaign': random.choice(campaigns),
        'influencer_id': influencer_id,
        'user_id': user_id,
        'product': product,
        'date': date.strftime('%Y-%m-%d'),
        'orders': orders,
        'revenue': revenue
    })

tracking_df = pd.DataFrame(tracking_data)
tracking_df.to_csv('tracking_data.csv', index=False)

# 4. Simulate payouts
basis_options = ['post', 'order']

payouts = []
for influencer_id in range(1, 21):
    basis = random.choice(basis_options)
    rate = round(random.uniform(300, 1500), 2)
    total_orders = tracking_df[tracking_df['influencer_id'] == influencer_id]['orders'].sum()
    num_posts = posts_df[posts_df['influencer_id'] == influencer_id].shape[0]
    total_payout = rate * (num_posts if basis == 'post' else total_orders)

    payouts.append({
        'influencer_id': influencer_id,
        'basis': basis,
        'rate': rate,
        'orders': int(total_orders),
        'total_payout': round(total_payout, 2)
    })

payouts_df = pd.DataFrame(payouts)
payouts_df.to_csv('payouts.csv', index=False)

print("All 4 datasets generated and saved as CSV.")
