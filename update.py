from app.scraper import build_players_df, save_players_csv, build_teams_csv

if __name__ == "__main__":
    print("⚡Starting update⚡\n")
    df = build_players_df()
    save_players_csv(df)

    teams_df = build_teams_csv(df)
    teams_df.to_csv("data/teams.csv", index=False)
    print("💾 Saved players and teams data")