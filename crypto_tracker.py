# -*- coding: utf-8 -*-
"""
Created on Sun Sep 28 18:59:17 2025

@author: Ring
"""

import tkinter as tk
from tkinter import messagebox
import requests

portfolio = {}

# 获取实时价格
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data[coin]["usd"]
    except Exception:
        return None

# 查询价格
def query_price():
    coin = entry_coin.get().lower()
    price = get_price(coin)
    if price:
        messagebox.showinfo("价格查询", f"{coin.upper()} 当前价格: ${price}")
    else:
        messagebox.showerror("错误", "获取价格失败，请检查拼写")

# 添加资产
def add_asset():
    coin = entry_coin.get().lower()
    try:
        buy_price = float(entry_buy_price.get())
        amount = float(entry_amount.get())
        portfolio[coin] = {"buy_price": buy_price, "amount": amount}
        messagebox.showinfo("成功", f"已添加 {coin.upper()} 资产")
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")

# 查看资产
def show_portfolio():
    if not portfolio:
        messagebox.showinfo("资产情况", "你的资产列表是空的")
        return

    result = ""
    for coin, info in portfolio.items():
        price = get_price(coin)
        if price:
            value_now = price * info["amount"]
            cost = info["buy_price"] * info["amount"]
            profit = value_now - cost
            result += (f"{coin.upper()} | 数量: {info['amount']} | 买入价: ${info['buy_price']} | 当前价: ${price}\n"
                       f"持仓价值: ${value_now:.2f} | 盈亏: ${profit:.2f}\n\n")
        else:
            result += f"{coin.upper()} 获取价格失败\n\n"

    messagebox.showinfo("资产情况", result)

# 创建窗口
root = tk.Tk()
root.title("加密货币资产管理小程序")
root.geometry("400x300")

# 输入框
tk.Label(root, text="币种 (英文)").pack()
entry_coin = tk.Entry(root)
entry_coin.pack()

tk.Label(root, text="买入价 (USD)").pack()
entry_buy_price = tk.Entry(root)
entry_buy_price.pack()

tk.Label(root, text="数量").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

# 按钮
tk.Button(root, text="查询实时价格", command=query_price).pack(pady=5)
tk.Button(root, text="添加资产", command=add_asset).pack(pady=5)
tk.Button(root, text="查看资产", command=show_portfolio).pack(pady=5)
tk.Button(root, text="退出", command=root.quit).pack(pady=5)

# 运行窗口
root.mainloop()
