class Buyer:
    def __init__(self, buyer_id: int, money: float, want_score: float, need_score: float):
        self.buyer_id = buyer_id
        self.money = money
        self.want_score = want_score
        self.need_score = need_score