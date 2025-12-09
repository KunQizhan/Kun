from Amm import ConstantProductAMM
from User import User
from Attacker import SandwichAttacker

# all the function's parameter can changed
def demo_basic_user_swap():    
    # create memopool
    pool = ConstantProductAMM(reserve_x=100, reserve_y=200000, fee_rate=0.003)
    print(f"\nInitial pool: {pool}")
    
    # create user
    alice = User(name="Alice", balance_x=10, balance_y=50000)
    alice.get_state()
    
    # trade
    alice.execute_swap(pool, amount_in=5, x_to_y=True, slippage_tolerance=0.02)
    
    # get the state of alice and memopool
    alice.get_state()
    print(f"\nPool after trade: {pool}")


def demo_sandwich_attack():
    # create memopool
    pool = ConstantProductAMM(reserve_x=1000, reserve_y=2000000, fee_rate=0.003)
    print(f"\nInitial pool: {pool}")
    
    # create victim Alice
    Alice = User(name="Alice", balance_x=20, balance_y=100000)
    print(f"\nVictim: {Alice}")
    
    # create attacker
    attacker = SandwichAttacker(name="Evil MEV Bot", balance_x=100, balance_y=500000)
    print(f"Attacker: {attacker}")
    
    # Victim trade and being shown to attacker
    victim_trade_amount = 50
    victim_direction = True
    
    # attacker excuate the Sandwich attack
    result = attacker.simulate_sandwich_attack(
        pool=pool,
        victim_amount=victim_trade_amount,
        victim_x_to_y=victim_direction,
        frontrun_multiplier=2.0
    )
    
    print(f"\n\nFinal pool: {pool}")
    attacker.get_state()

if __name__ == "__main__":
    demo_basic_user_swap()
    demo_sandwich_attack()





# 1. 代码在干嘛

# 就是把 ConstantProductAMM + User + SandwichAttacker 三个类串成两个 demo：

# demo_basic_user_swap()：只有普通用户和池子；

# demo_sandwich_attack()：加入攻击者，跑一轮完整三明治。

# 2. 文献对应

# 其实 Demo 本身不需要单独对应某篇文献，它只是：

# 把 AMM 模型（Uniswap_v2_whitepaper.pdf + An analysis of Uniswap markets.pdf）

# 和 攻击模型（HFT_on_chain_EX.pdf + sandwich_attacks_ETH.pdf）

# 以及 成本/行为文献（Don’t Let MEV Slip.pdf + slippage_game_theory.pdf）
# 组合成一个可执行实验环境。

# 在 Methodology 里可以一句话带过：

# “我们在 Python 中实现了一个最小实验环境，将上述 AMM 模型、攻击者模型与交易者行为组合在一起（见 Amm.py, User.py, Attacker.py）。Demo.py 提供了实验入口，用于重现实验与教学示例。”