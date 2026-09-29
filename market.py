class BalanceSheet:
    """Tracks an economic agent's financial and physical state, separating 
    liquid cash, physical commodity inventory, and financial debt.
    """

    def __init__(self, cash: float = 0.0):
        self.cash = max(0.0, cash)
        self.inventory: dict[str, float] = {}
        self.liabilities: dict[str, float] = {}

    def add_item(self, item_name: str, quantity: float) -> None:
        """Adds a physical quantity of a commodity to inventory."""
        if quantity <= 0:
            return
        self.inventory[item_name] = self.inventory.get(item_name, 0.0) + quantity

    def remove_item(self, item_name: str, quantity: float) -> bool:
        """Removes a quantity of an item if sufficient stock exists."""
        current_qty = self.inventory.get(item_name, 0.0)
        if current_qty >= quantity:
            self.inventory[item_name] = current_qty - quantity
            return True
        return False

    @property
    def total_liabilities(self) -> float:
        """Calculates total outstanding debt in USD."""
        return sum(self.liabilities.values())

    def total_asset_value(self, market_prices: dict[str, float]) -> float:
        """Calculates total assets in USD by marking physical inventory to 
        prevailing market prices.
        """
        inventory_value = sum(
            qty * market_prices.get(item, 0.0)
            for item, qty in self.inventory.items()
        )
        return self.cash + inventory_value

    def net_worth(self, market_prices: dict[str, float]) -> float:
        """Calculates total net worth (Assets - Liabilities)."""
        return self.total_asset_value(market_prices) - self.total_liabilities
class Agent:
    """Represents an economic actor whose purchasing power and physical asset 
    holding are managed via an internal BalanceSheet.
    """

    def __init__(self, agent_id: int, initial_cash: float = 0.0):
        self.agent_id = agent_id
        self.balance_sheet = BalanceSheet(cash=initial_cash)
        
        # Dynamic states (0.0 = fully satiated, 1.0 = critical urgency)
        self.want_score = 0.0
        self.need_score = 0.0