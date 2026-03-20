from app.scraper import build_players_df, save_players_csv, build_teams_csv

if __name__ == "__main__":
    print("🚀 Starting update...\n")
    df = build_players_df()
    save_players_csv(df)

    teams_df = build_teams_csv(df)
    teams_df.to_csv("data/teams.csv", index=False)
    print("💾 Saved to data/teams.csv")

    missing_img = df[df["Image"] == ""][["ID", "Name", "Game", "Age group"]]
    if len(missing_img) > 0:
        print(f"\n⚠️  {len(missing_img)} players missing images:")
        print(missing_img.to_string())
    else:
        print("\n✅ All players have images!")

    print("\n🎉 Done!")