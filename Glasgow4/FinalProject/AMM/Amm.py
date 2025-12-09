## The core implementation responsibilities of an V2 AMM pool are: 
## managing reserves, 
## performing swaps,
## calculating prices and slippage
import time
class ConstantProductAMM:
    def __init__(self, reserve_x, reserve_y, fee_rate = 0.003):
        ## reserve_x means amount of token x
        ## reserve_y means amount of token y
        ## fee_rate is 0.3% default, can be changed

        if reserve_x <= 0 or reserve_y <= 0:
            raise ValueError(f"two reserves must be positive : x = {reserve_x}, y = {reserve_y}")

        self.reserve_x = float(reserve_x)
        self.reserve_y = float(reserve_y)
        self.fee_rate = float(fee_rate)

        ## the constant product x * y = k
        self.k = self.reserve_x * self.reserve_y
    
        ## to check the history of trade to follow up the TX flow
        self.trade_history = []

    def get_spot_price(self):
        return self.reserve_y / self.reserve_x
    
    def calculate_output_amount(self, amount_in, x_to_y=True):

        if amount_in <= 0:
            raise ValueError(f"There is wrong amount input token")

        if x_to_y: 
            reserve_in = self.reserve_x
            reserve_out = self.reserve_y
        else:
            reserve_in = self.reserve_y
            reserve_out = self.reserve_x
        
        amount_out = (amount_in * (1-self.fee_rate) * reserve_out) / (amount_in * (1-self.fee_rate) + reserve_in)

        return amount_out
    
    def swap(self, amount_in, x_to_y=True):

        if amount_in <= 0:
            raise ValueError(f"There is wrong amount input token")
        
        amount_out = self.calculate_output_amount(amount_in, x_to_y)

        if x_to_y: 
            ## fee rate is includ since when do the calculate_output_amount, we use amount_in * (1-self.fee_rate) to calculate the amount out, 
            ## so there is defaultly means that there is a 0.3% fee rate is given to the memopool
            self.reserve_x += amount_in 
            self.reserve_y -= amount_out
        else: 
            self.reserve_y += amount_in
            self.reserve_x -= amount_out

        new_k = self.reserve_x * self.reserve_y
        assert new_k >= self.k, "K should not decrease"
        self.k = new_k

        self.trade_history.append({
            "direction": 'X to Y' if x_to_y else 'Y to X',
            "amount in": amount_in,
            "amount out": amount_out,
            "price_update": self.get_spot_price()
        })

        return amount_out
    
    def calculate_price_slippage(self, amount_in, x_to_y = True):
        price_before = self.get_spot_price()
        amount_out = self.calculate_output_amount(amount_in, x_to_y)
        if x_to_y:
            new_reserve_x = self.reserve_x + amount_in
            new_reserve_y = self.reserve_y - amount_out
        else: 
            new_reserve_y = self.reserve_y + amount_in
            new_reserve_x = self.reserve_x - amount_out
        
        price_changed = new_reserve_y / new_reserve_x
        price_impacted = (price_changed - price_before) / price_before

        return {
            "price before": price_before,
            "price after": price_changed,
            "Slippage": price_impacted * 100
        }
    
    def get_state(self):
        return {
            "reserve x": self.reserve_x,
            "reserve y": self.reserve_y,
            "k": self.k,
            "price": self.get_spot_price(),
            ## no trade history since get_state is return a dict type, can be edit, internally use only!!
            ## but __repr__() function return a string, that is no edit allowed
            ## "Transaction happened: ": self.trade_history
        }
    
    def restore_state(self, state):
        self.reserve_x = state["reserve x"]
        self.reserve_y = state["reserve y"]
        self.k = state["k"]
    
    def __repr__(self): 
        return (f"Amm(X = {self.reserve_x: .2f}, Y = {self.reserve_y: .2f},"
                f"Price = {self.get_spot_price(): .2f},"
                f"k = {self.k: .2f})")

    def copy(self):
        new_pool = ConstantProductAMM(self.reserve_x, self.reserve_y, self.fee_rate)
        return new_pool
    


# 定义 ConstantProductAMM：

# 状态：reserve_x, reserve_y, fee_rate

# 关键函数：calculate_output_amount、swap、get_spot_price、calculate_price_slippage 等

# 本质上就是一个简化版 Uniswap V2 池。

# 2. 理论来源（写在论文里可以这么说）

# “我们的 AMM 模型直接基于：

# 1_AMM_Basics/Uniswap_v2_whitepaper.pdf：提供了 x·y=k 的 constant-product 公式以及手续费的扣除方式；

# 1_AMM_Basics/An analysis of Uniswap markets.pdf：从数学上分析了该模型的价格与均衡性质。”

# “此外，我们在 Related Work 中参考 1_AMM_Basics/SoK DEXs with AMM Protocols.pdf，说明本项目聚焦于最经典的 V2 constant-product AMM，而不是其他变体。”

# → 总结一句话版本：

# Amm.py = “把 Uniswap_v2_whitepaper.pdf + An analysis of Uniswap markets.pdf 的数学公式写成代码”。