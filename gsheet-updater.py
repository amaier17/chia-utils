#!/usr/bin/env python

import asyncio
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from chia.rpc.wallet_rpc_api import WalletRpcApi
from chia.rpc.wallet_rpc_client import WalletRpcClient
from chia.util.config import load_config
from chia.util.default_root import DEFAULT_ROOT_PATH

def update_gsheet(xch):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('/opt/chia/ec-updater-ea96fd077e39.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open("Eid-Chia Financials")
    worksheet = sheet.get_worksheet(0)
    worksheet.update("L1", xch)
    worksheet.update("A15", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

async def get_balance():
    try:
        config = load_config(DEFAULT_ROOT_PATH, "config.yaml")
        wallet_rpc_port = config["wallet"]["rpc_port"]

        client = await WalletRpcClient.create("localhost", wallet_rpc_port, DEFAULT_ROOT_PATH, config)
        wallets = await client.get_wallets()
        total_xch = 0
        for wallet in wallets:
            balance = await client.get_wallet_balance(wallet["id"])
            total_xch = total_xch + balance["confirmed_wallet_balance"] / 1e12

        return total_xch

    except Exception as e:
        print(e)

    finally:
        client.close()

if __name__ == "__main__":
    xch = asyncio.run(get_balance())
    update_gsheet(xch)

