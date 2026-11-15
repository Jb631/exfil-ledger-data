# exfil-ledger-data

Game data for the Exfil Ledger app. The app downloads `kit.json` from this repo each time it opens and uses it when its `rev` is newer than the copy built into the app.

`kit.json` is generated from the files in `tools/`. To update it, follow `tools/README.md`: edit the data, rebuild, run the check, push. Testers get the new data the next time they open the app (GitHub can take about 5 minutes to serve the new file). `CHECKLOG.md` lists every check and what it published.

Fan-made reference. Not affiliated with Activision or Infinity Ward.
