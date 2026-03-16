import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# LOAD DATA
matches = pd.read_csv('matches.csv')
deliveries = pd.read_csv('deliveries.csv')

print("Total matches:", len(matches))
print("Total deliveries:", len(deliveries))

# ── CLEANING ──
# Drop rows where winner is missing (no result matches)
matches = matches.dropna(subset=['winner'])
print("Matches after cleaning:", len(matches))
print("Missing values in matches:\n", matches.isnull().sum())

# ── ANALYSIS 1: Most winning teams ──
team_wins = matches['winner'].value_counts().head(10)
print("\n=== TOP 10 WINNING TEAMS ===")
print(team_wins)

plt.figure(figsize=(12,6))
sns.barplot(x=team_wins.values, y=team_wins.index, palette='Blues_r')
plt.title('Top 10 Most Winning IPL Teams (2008-2020)', fontsize=14)
plt.xlabel('Number of Wins')
plt.tight_layout()
plt.savefig('team_wins.png', dpi=150)
plt.close()
print("Saved: team_wins.png")

# ── ANALYSIS 2: Toss impact ──
toss_wins = matches[matches['toss_winner'] == matches['winner']]
toss_win_pct = round(len(toss_wins) / len(matches) * 100, 1)
print(f"\n=== TOSS IMPACT ===")
print(f"Toss winner also won the match: {toss_win_pct}%")
print(f"Toss winner lost the match: {100 - toss_win_pct}%")

# ── ANALYSIS 3: Toss decision ──
toss_decision = matches['toss_decision'].value_counts()
print("\n=== TOSS DECISION ===")
print(toss_decision)

# ── ANALYSIS 4: Top run scorers ──
batsman_runs = deliveries.groupby('batter')['batsman_runs'].sum().sort_values(ascending=False).head(10)
print("\n=== TOP 10 RUN SCORERS ===")
print(batsman_runs)

plt.figure(figsize=(12,6))
sns.barplot(x=batsman_runs.values, y=batsman_runs.index, palette='Oranges_r')
plt.title('Top 10 Run Scorers in IPL History', fontsize=14)
plt.xlabel('Total Runs')
plt.tight_layout()
plt.savefig('top_batsmen.png', dpi=150)
plt.close()
print("Saved: top_batsmen.png")

# ── ANALYSIS 5: Top wicket takers ──
wickets = deliveries[deliveries['dismissal_kind'].notna()]
wickets = wickets[~wickets['dismissal_kind'].isin(['run out','retired hurt','obstructing the field'])]
top_bowlers = wickets.groupby('bowler')['dismissal_kind'].count().sort_values(ascending=False).head(10)
print("\n=== TOP 10 WICKET TAKERS ===")
print(top_bowlers)

plt.figure(figsize=(12,6))
sns.barplot(x=top_bowlers.values, y=top_bowlers.index, palette='Greens_r')
plt.title('Top 10 Wicket Takers in IPL History', fontsize=14)
plt.xlabel('Total Wickets')
plt.tight_layout()
plt.savefig('top_bowlers.png', dpi=150)
plt.close()
print("Saved: top_bowlers.png")

# ── ANALYSIS 6: Season wise runs ──
season_runs = deliveries.merge(matches[['id','season']], left_on='match_id', right_on='id')
season_total = season_runs.groupby('season')['total_runs'].sum()
print("\n=== RUNS PER SEASON ===")
print(season_total)

plt.figure(figsize=(12,6))
sns.lineplot(x=range(len(season_total)), y=season_total.values, marker='o', color='royalblue', linewidth=2)
plt.xticks(range(len(season_total)), season_total.index, rotation=45)
plt.title('Total Runs Scored Per IPL Season', fontsize=14)
plt.xlabel('Season')
plt.ylabel('Total Runs')
plt.tight_layout()
plt.savefig('season_trends.png', dpi=150)
plt.close()
print("Saved: season_trends.png")

# ── ANALYSIS 7: Player of the match ──
potm = matches['player_of_match'].value_counts().head(10)
print("\n=== TOP PLAYER OF THE MATCH AWARDS ===")
print(potm)

print("\n✅ All analysis complete!")