from src.utils.dbengine import get_db
from src.models.financial import Financial


class FinancialController:
    TRANSACTION_TYPES = ['Income', 'Expense', 'Transfer']

    def add_transaction(self, transaction_date, amount, transaction_type, recipient=None, sender=None, email_controller=None):
        if transaction_type not in self.TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type. Must be one of {self.TRANSACTION_TYPES}")
        with get_db() as db:
            transaction = Financial(transaction_date=transaction_date, amount=amount, transaction_type=transaction_type, recipient=recipient, sender=sender)
            db.add(transaction)
            db.commit()
            db.refresh(transaction) 
            return transaction
        if transaction_type == 'Transfer':
            email_controller.send_email(
                recipient=recipient,
                subject='Transfer Confirmation',
                body=f'You have received a transfer of ${amount} from {sender}.'
            )


    def edit_transaction(self, transaction_id, transaction_date=None, amount=None, transaction_type=None, recipient=None, sender=None):
        if transaction_type and transaction_type not in self.TRANSACTION_TYPES:
            raise ValueError(f"Invalid transaction type. Must be one of {self.TRANSACTION_TYPES}")
        with get_db() as db:
            transaction = db.query(Financial).filter(Financial.id == transaction_id).first()
            if not transaction:
                return None
            if transaction_date:
                transaction.transaction_date = transaction_date
            if amount:
                transaction.amount = amount
            if transaction_type:
                transaction.transaction_type = transaction_type
            if recipient:
                transaction.recipient = recipient
            if sender:
                transaction.sender = sender
            db.commit()
            db.refresh(transaction)
            return transaction

    def get_all_transactions(self):
        with get_db() as db:
            return db.query(Financial).all()

    def delete_transaction(self, transaction_id):
        with get_db() as db:
            transaction = db.query(Financial).filter(Financial.id == transaction_id).first()
            if transaction:
                db.delete(transaction)
                db.commit()
    