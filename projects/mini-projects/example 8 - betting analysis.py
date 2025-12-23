import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data

df = pd.read_csv("sports_betting_data.csv")
df['event_date'] = pd.to_datetime(df['event_date'])
# Προαιρετικοί έλεγχοι ποιότητας δεδομένων
# df.info()
# print("nulls:\n", df.isnull().sum())
# print("na:\n", df.isna().sum())
# print("duplicates:\n", df.duplicated().sum())
# print(df.describe())

# 2. Overall win / loss & win rate
wins = 0
losses = 0

for outcome in df['bet_outcome']:
    if outcome == 'win':
        wins += 1
    else:
        losses += 1

win_rate_overall = wins / (wins + losses)

print(f"Wins: {wins}")
print(f"Losses: {losses}")
print(f"Overall Win Rate: {win_rate_overall*100:.2f}%")

# 3. Win rate per bet type
total_bets_per_type = df.groupby("bet_type")["bet_outcome"].count()

wins_df = df[df['bet_outcome'] == 'win']
wins_per_type = wins_df.groupby('bet_type')['bet_outcome'].count()

win_rate_per_type = (
    (wins_per_type / total_bets_per_type) * 100
).round(2).astype(str) + '%'

win_rate_df = win_rate_per_type.reset_index()
win_rate_df.columns = ['bet_type', 'win_rate']

print("\nWin rate per bet type:")
print(win_rate_df)

# 4. Total bet amount
total_bet_amount = df['bet_amount'].sum()
print(f"\nTotal Bet Amount: {total_bet_amount:.2f} €")

# 5. Total profit calculation
total_profit = 0

for _, row in df.iterrows():
    if row['bet_outcome'] == 'win':
        total_profit += (row['odds'] - 1) * row['bet_amount']
    else:
        total_profit -= row['bet_amount']

print(f"Total Profit: {total_profit:.2f} €")

# 6. Visualization: Wins per bet type
plt.figure(figsize=(6, 4))
plt.bar(wins_per_type.index, wins_per_type.values, edgecolor='black')
plt.xlabel('Bet Type')
plt.ylabel('Wins')
plt.title('Wins per Bet Type')

for i, v in enumerate(wins_per_type.values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# 7. Visualization: Average bet amount per bet type
avg_bet_amount = df.groupby('bet_type')['bet_amount'].mean()

plt.figure(figsize=(6, 4))
plt.plot(avg_bet_amount.index, avg_bet_amount.values, marker='o')
plt.xlabel('Bet Type')
plt.ylabel('Average Bet Amount (€)')
plt.title('Average Bet Amount per Bet Type')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()