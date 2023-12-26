# Nifty Notifier
Nifty Notifier is a simple python script that I created for a friend. It monitors `niftygateway.com` for new drops from the `Starbucks Corporation` and sends a discord webhook notification when a new drop is detected.

## How to Use
1. Clone the repository
```bash
git clone https://github.com/NelsonDane/nifty-notifier.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add the following:
```bash
DISCORD_WEBHOOK=<your discord webhook url>
```
4. Run the script
```bash
python nn.py
```
