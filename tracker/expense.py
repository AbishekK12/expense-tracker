class Expense:

    def __init__(
        self,
        expense_id : int,
        name : str,
        amount : float,
        category : str,
        date : str) -> None:

        self.expense_id = expense_id
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date


    def to_dict(self) -> dict:

        return {
            "expense_id" : self.expense_id,
            "name" : self.name,
            "amount" : self.amount,
            "category" : self.category,
            "date" : self.date
        }