class PaymentService:
    @staticmethod
    def process_payment(user, amount):
        """
        Deducts the given amount from the user's balance if they have enough funds.
        Returns True if successful, False otherwise.
        """
        if user.balance >= amount:
            user.balance -= amount
            print(f"Payment of {amount} successful. New balance: {user.balance}")
            return True
        else:
            print("Insufficient balance. Payment failed.")
            return False

    @staticmethod
    def refund_payment(user, amount):
        """
        Refunds the given amount to the user's balance.
        """
        user.balance += amount
        print(f"Refund of {amount} successful. New balance: {user.balance}")
