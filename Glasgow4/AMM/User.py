from Amm import ConstantProductAMM

class User:
    def __init__(self, name, balance_x, balance_y): 
        # name of user
        self.name = name
        # balance of token x
        self.balance_x = float(balance_x)
        # balance of token y
        self.balance_y = float(balance_y)
        # make a dictionary to record the history of TX of user
        self.transaction_history = []
    
    # check the balance is enough for a TX
    def check_balance(self, amount, token_type='x'):
        if token_type.lower() == 'x':
            return self.balance_x >= amount
        else:
            return self.balance_y >= amount
    
    # get the balance of two tokens
    def get_balance(self):
        return { "X": self.balance_x, "Y": self.balance_y}
    
    # get the state of current user, aim for Tx history
    def get_state(self):
        print(f"\n{self.name}'s Account")
        print(f"Balance X: {self.balance_x:.6f}")
        print(f"Balance Y: {self.balance_y:.6f}")
        print(f"Transactions: {len(self.transaction_history)}")
    
    # excute a swap in a memopool
    def execute_swap(self, pool, amount_in, x_to_y=True, slippage_tolerance=0.01):
        # input validation
        if amount_in <= 0:
            print(f"[{self.name}] Error: Invalid amount {amount_in}")
            return None
        
        # amount in should larger than 0
        token_in = 'x' if x_to_y else 'y'
        if not self.check_balance(amount_in, token_in):
            print(f"[{self.name}] Error: Insufficient balance")
            return None
        
        # calculate the expect output and slippage for this TX
        price_info = pool.calculate_price_slippage(amount_in, x_to_y)
        expected_out = pool.calculate_output_amount(amount_in, x_to_y)
        min_out = expected_out * (1 - slippage_tolerance)
        
        # store the current state of memopool
        old_pool_state = pool.get_state()
        
        # use try to avioud rollback
        try:
            actual_out = pool.swap(amount_in, x_to_y)
            
            # check weather the actual slpippage is over user's torelance
            if actual_out < min_out:
                print(f"[{self.name}] Transaction failed: Slippage too high!")
                print(f"  Expected: {expected_out:.6f}, Got: {actual_out:.6f}")
                pool.restore_state(old_pool_state)
                return None
            
            # if no rollback, then reocrd the new state
            if x_to_y:
                self.balance_x -= amount_in
                self.balance_y += actual_out
            else:
                self.balance_y -= amount_in
                self.balance_x += actual_out
            
            # record the Tx history
            transaction = {
                "user": self.name,
                "direction": "X->Y" if x_to_y else "Y->X",
                "amount_in": amount_in,
                "amount_out": actual_out,
                "price": actual_out / amount_in if x_to_y else amount_in / actual_out,
                "slippage": price_info["Slippage"]
            }
            self.transaction_history.append(transaction)
            
            print(f"[{self.name}] Swap successful!")
            print(f"  Traded: {amount_in:.6f} {'X' if x_to_y else 'Y'}")
            print(f"  Received: {actual_out:.6f} {'Y' if x_to_y else 'X'}")
            print(f"  Slippage: {price_info['Slippage']:.4f}%")
            
            return actual_out
            
        except Exception as e:
            print(f"[{self.name}] Transaction failed: {e}")
            pool.restore_state(old_pool_state)
            return None
    
    def __repr__(self):
        return f"User({self.name}, X={self.balance_x:.2f}, Y={self.balance_y:.2f})"