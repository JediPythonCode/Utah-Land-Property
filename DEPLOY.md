# Deploy Utah Land Desk to utahlandproperty.com

GitHub Pages only serves static files. The desk is a FastAPI process, so it must run on a host that supports long-running Python apps.

## Recommended: Render (free tier available)

1. Go to [render.com](https://render.com) → New → Web Service
2. Connect the GitHub repo `JediPythonCode/Utah-Land-Property`
3. Branch: `main` (after this PR merges)
4. Runtime: Python
5. Build command: `pip install -r requirements.txt`
6. Start command: `python scripts/run_desk.py`
7. Add environment variables (or use a secret file):
   - `FRED_API_KEY` (optional but useful)
   - You can also mount a `secrets.toml` if the platform allows files
8. Deploy. You will get a URL like `https://utah-land-desk.onrender.com`

## Point the domain

1. In your domain registrar (or Cloudflare), update the DNS for `utahlandproperty.com`:
   - Remove the current GitHub Pages CNAME / A records
   - Add a CNAME record pointing to the Render (or Railway) hostname
2. In the hosting dashboard, add the custom domain `utahlandproperty.com` and follow the HTTPS instructions.
3. (Optional) Disable GitHub Pages for this repo so it no longer tries to serve the old static site.

## Alternative hosts

- **Railway**: connect repo, set start command `python scripts/run_desk.py`, add custom domain.
- **Fly.io**: `fly launch` (Dockerfile is included).
- **AWS App Runner**: create service from the repo or Docker image (you already use App Runner for Full Spectrum).

## Secrets

Create `secrets.toml` on the host (or convert the keys to env vars and update the loaders). Do not commit real tokens.

After DNS propagates (usually minutes to a few hours), `https://utahlandproperty.com` will serve the live desk.
