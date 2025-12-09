from Amm import ConstantProductAMM
from User import User

class SandwichAttacker:
    def __init__(self, name, balance_x, balance_y):
        # same idea with user
        self.name = name
        self.balance_x = float(balance_x)
        self.balance_y = float(balance_y)
        self.attack_history = []
        # add two function to check the profit for attack
        self.total_profit_x = 0.0
        self.total_profit_y = 0.0
    
    # pool: instance of CPMM
    # victim_amount : the trade value of user
    # victim_x_to_y: the token for user to trade
    # frontrun_multiplier: the time more money is frontrun than victim
    def simulate_sandwich_attack(self, pool, victim_amount, victim_x_to_y=True, frontrun_multiplier=1.5):
        
        # record the inital status
        initial_pool_state = pool.get_state()
        initial_price = pool.get_spot_price()
        attacker_initial_x = self.balance_x
        attacker_initial_y = self.balance_y
        
        # calculate how many tokens victim can get without attack
        normal_victim_output = pool.calculate_output_amount(victim_amount, victim_x_to_y)
        
        # do the sandwich
        frontrun_amount = victim_amount * frontrun_multiplier
        
        # check balance
        if victim_x_to_y:
            if self.balance_x < frontrun_amount:
                print(f"Insufficient balance for frontrun!")
                return None
        else:
            if self.balance_y < frontrun_amount:
                print(f"Insufficient balance for frontrun!")
                return None
        
        # excuatate the frontrun
        frontrun_output = pool.swap(frontrun_amount, victim_x_to_y)
        
        if victim_x_to_y:
            self.balance_x -= frontrun_amount
            self.balance_y += frontrun_output
        else:
            self.balance_y -= frontrun_amount
            self.balance_x += frontrun_output
        
        price_after_frontrun = pool.get_spot_price()
        
        # record the victim's Tx's result
        victim_output = pool.swap(victim_amount, victim_x_to_y)
        victim_loss = normal_victim_output - victim_output

        # record the price for toekn after the Tx
        price_after_victim = pool.get_spot_price()
        
        # attacker swap back the token into another token to get profit
        backrun_output = pool.swap(frontrun_output, not victim_x_to_y)
        if victim_x_to_y:
            self.balance_y -= frontrun_output
            self.balance_x += backrun_output
        else:
            self.balance_x -= frontrun_output
            self.balance_y += backrun_output
        # record the end price, since attacker had swaped back
        final_price = pool.get_spot_price()
        
        # calcuate the profit of attacker
        if victim_x_to_y:
            profit_x = self.balance_x - attacker_initial_x
            profit_y = self.balance_y - attacker_initial_y
        else:
            profit_x = self.balance_x - attacker_initial_x
            profit_y = self.balance_y - attacker_initial_y
        
        # update overall profit for attacker
        self.total_profit_x += profit_x
        self.total_profit_y += profit_y
        
        # print out what happened
        print(f"\nAttacker Profit:")
        print(f"Token X: {profit_x:+.6f}")
        print(f"Token Y: {profit_y:+.6f}")
        print(f"Profit % (based on frontrun): {(profit_x/frontrun_amount*100 if victim_x_to_y else profit_y/frontrun_amount*100):.4f}%")
        
        print(f"\nVictim Loss:")
        print(f"Lost: {victim_loss:.6f} {'Y' if victim_x_to_y else 'X'}")
        print(f"Loss %: {(victim_loss/normal_victim_output*100):.4f}%")
        
        print(f"\nPrice Changes:")
        print(f"Initial: {initial_price:.6f} Y/X")
        print(f"After frontrun: {price_after_frontrun:.6f} Y/X")
        print(f"After victim: {price_after_victim:.6f} Y/X")
        print(f"Final: {final_price:.6f} Y/X")
        
        # reocrd the attack
        attack_record = {
            "victim_amount": victim_amount,
            "victim_direction": "X->Y" if victim_x_to_y else "Y->X",
            "frontrun_amount": frontrun_amount,
            "profit_x": profit_x,
            "profit_y": profit_y,
            "victim_loss": victim_loss,
            "price_initial": initial_price,
            "price_final": final_price
        }
        self.attack_history.append(attack_record)
        return attack_record    
    def get_state(self):
        print(f"\n{self.name}'s Account")
        print(f"Balance X: {self.balance_x:.6f}")
        print(f"Balance Y: {self.balance_y:.6f}")
        print(f"Total Profit X: {self.total_profit_x:+.6f}")
        print(f"Total Profit Y: {self.total_profit_y:+.6f}")
        print(f"Attacks Executed: {len(self.attack_history)}")
    
    def __repr__(self):
        return f"Attacker({self.name}, X={self.balance_x:.2f}, Y={self.balance_y:.2f})"
    




# 1. 代码在干嘛

# 定义 SandwichAttacker：

# 状态：攻击者持有的 X/Y、历史记录、累计利润

# 核心函数：simulate_sandwich_attack(pool, victim_amount, victim_x_to_y, frontrun_multiplier)，流程是：

# 记录池子初始状态

# 算一遍“没有攻击时受害者能拿到多少”

# 前插交易（按 frontrun_multiplier 决定大小）

# 受害者交易

# 后插交易（反方向）

# 统计攻击者利润、受害者损失、价格变化

# 2. 文献对应

# 攻击机制（结构）：

# 3_Sandwich_V2/HFT_on_chain_EX.pdf

# 这就是讲“链上高频交易”的论文，其中标准定义了三明治：front-run → victim swap → back-run；

# 你当前代码的整套流程完全对应它的定义，只是把“能不能抢到排序”简化成 100% 成功。

# 攻击模式实证：

# 3_Sandwich_V2/sandwich_attacks_ETH.pdf

# 用真实数据识别三明治交易模式，你可以在论文里说：

# 我们的攻击者模型复现了这篇文章中观察到的典型 sandwich 结构，但在一个完全可控的模拟环境中测试不同参数组合的盈利性。

# MEV 背景 / 从哪里来的机会：

# 2_MEV_General/Flash Boys 2.0.pdf

# 这是整个 MEV / 交易重排问题的启蒙；

# 在 Attacker 部分你可以用一句话说明：sandwich 属于这类“排序可提取价值”的典型代表，引用它做背景即可。

# → 总结一句话版本：

# Attacker.py = “基于 HFT_on_chain_EX.pdf 定义的三明治三步流程，在 sandwich_attacks_ETH.pdf 的实证模式基础上实现一个简化的攻击者，并在 Flash Boys 2.0.pdf 描述的 MEV 环境下分析其盈利性。”