# .github/workflows/poyo-notify.yml
#
# Sends a "Kirby System" push notification to your phone/desktop
# via ntfy.sh at the end of your CI pipeline.
#
# ── Setup (one-time) ───────────────────────────────────────────
#  1. Install the ntfy app on your phone:  https://ntfy.sh
#  2. Pick a unique topic name, e.g.  kirby-ci-yourname
#  3. Subscribe to that topic in the app.
#  4. Add it as a GitHub secret:
#       Repo → Settings → Secrets → Actions → New secret
#       Name:  NTFY_TOPIC
#       Value: kirby-ci-yourname   (your unique topic)
# ───────────────────────────────────────────────────────────────

name: CI + Poyo Notify

on:
  push:
    branches: ["**"]
  pull_request:
    branches: ["**"]
  workflow_dispatch:          # lets you trigger manually from the UI

jobs:
  build-and-notify:
    runs-on: ubuntu-latest

    steps:
      # ── 1. Checkout ──────────────────────────────────────────
      - name: Checkout code
        uses: actions/checkout@v4

      # ── 2. Set up Python ─────────────────────────────────────
      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      # ── 3. Install dependencies ───────────────────────────────
      #    (replace / extend with your real install step)
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

      # ── 4. Run your tests / build ────────────────────────────
      #    (replace with your real test command)
      - name: Run tests
        run: |
          echo "🔬 Running tests..."
          python -m pytest --tb=short || true   # remove '|| true' to fail on errors

      # ── 5. Poyo! Send success notification ───────────────────
      - name: Poyo — notify success 🎉
        if: success()
        env:
          NTFY_TOPIC: ${{ secrets.NTFY_TOPIC }}
        run: |
          python send_poyo.py

      # ── 6. Poyo! Send failure notification ───────────────────
      - name: Poyo — notify failure 💥
        if: failure()
        env:
          NTFY_TOPIC: ${{ secrets.NTFY_TOPIC }}
        run: |
          python - <<'EOF'
          import os, urllib.request, json
          topic = os.environ["NTFY_TOPIC"]
          payload = json.dumps({
              "topic": topic,
              "title": "Kirby System — BUILD FAILED",
              "message": "Something went wrong! (╥_╥) Check the Actions log.",
              "priority": 4,          # high priority on ntfy
              "tags": ["warning"]     # shows ⚠️ icon in ntfy app
          }).encode()
          req = urllib.request.Request(
              f"https://ntfy.sh/{topic}",
              data=payload,
              headers={"Content-Type": "application/json"},
              method="POST"
          )
          urllib.request.urlopen(req, timeout=10)
          print("Failure notification sent.")
          EOF
