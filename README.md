# Sentinel Blocklists

DNS blocklists for Pi-hole, produced by [Cyber Sentinel](https://github.com/lukaszFD/cyber-sentinel).

| List | Content | Approval |
|---|---|---|
| `lists/malicious.txt` | Domains the pipeline blocked after VirusTotal detections | automatic, expires unless detected again (90 days by default) |
| `lists/tracking.txt` | Tracking domains | AI classification, human review |
| `lists/telemetry.txt` | Vendor telemetry | AI classification, human review |

Telemetry blocking can break vendor features (updates, sync, license checks). Add that list only where you accept it.

## Use in Pi-hole

Add as adlists (Settings → Lists):

```
https://raw.githubusercontent.com/lukaszFD/sentinel-blocklists/main/lists/malicious.txt
https://raw.githubusercontent.com/lukaszFD/sentinel-blocklists/main/lists/tracking.txt
https://raw.githubusercontent.com/lukaszFD/sentinel-blocklists/main/lists/telemetry.txt
```

Then run `pihole -g` or wait for the scheduled gravity update.

## How the lists are built

The files are generated. Cyber Sentinel keeps every entry in its database; once a day an n8n workflow writes the full files to the `n8n/daily-update` branch and opens a pull request. Nothing reaches `main` without a manual merge.

Do not edit `lists/` by hand — the next run overwrites it. Add or remove entries in the Cyber Sentinel AI Config UI.

Format: one lowercase domain per line, exact match (subdomains are not covered). Comment lines start with `#`. `scripts/validate.py` checks every pull request.

## False positives

Open an issue with the domain and what broke.
