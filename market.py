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

SATIATION_VALUES = {
    "apples": 0.25,  # Eats 1 apple -> hunger drops by 0.25
    "bread": 0.50,   # Eats 1 loaf  -> hunger drops by 0.50
}

class NeedTracker:
    """Tracks an agent's internal physiological drives and urgency.
    
    Scores range from 0.0 (fully satiated) to 1.0 (critical threat / desperation).
    """

    def __init__(self, hunger: float = 0.0, exposure: float = 0.0):
        # Level 1: Biological Survival
        self.hunger = max(0.0, min(1.0, float(hunger)))
        
        # Level 2: Safety & Shelter
        self.exposure = max(0.0, min(1.0, float(exposure)))

    def tick(self, hunger_rate: float = 0.1, exposure_rate: float = 0.05) -> None:
        """Simulates time passing by increasing needs/depletion."""
        self.hunger = min(1.0, self.hunger + hunger_rate)
        self.exposure = min(1.0, self.exposure + exposure_rate)

    def satisfy_hunger(self, amount: float) -> None:
        """Reduces hunger score when food is consumed."""
        self.hunger = max(0.0, self.hunger - amount)

    @property
    def primary_urgency(self) -> float:
        """Returns the urgency score of the most critical Level 1 need.
        Used to calculate overall market desperation and Willingness to Pay.
        """
        return self.hunger

class Agent:
    """Represents an economic actor whose state, purchasing power, and physical assets 
    are managed via an internal BalanceSheet and NeedTracker.
    """

    def __init__(self, agent_id: int, initial_cash: float = 0.0):
        self.agent_id = agent_id
        self.balance_sheet = BalanceSheet(cash=initial_cash)
        self.needs = NeedTracker()

    def consume(self, item_name: str, quantity: float = 1.0) -> bool:
        """Consumes a good from inventory to satisfy internal needs.
        
        Returns True if successful, False if insufficient stock exists.
        """
        if not self.balance_sheet.remove_item(item_name, quantity):
            return False  # Not enough stock to consume!

        # Apply satisfaction yield based on commodity type
        if item_name in SATIATION_VALUES:
            satiation_yield = SATIATION_VALUES[item_name] * quantity
            self.needs.satisfy_hunger(satiation_yield)

        return True