import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from shop.models import Customer, Product, Order, OrderItem
from django.db.models import Max

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **options):
        batch_size = 1000  # Adjust based on your database
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        with transaction.atomic():
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Customer.objects.all().delete()
            User.objects.filter(username__startswith='user').delete()
            Product.objects.all().delete()

        # Create products in bulk
        self.stdout.write('Creating products...')
        products = []
        for i in range(1000):
            products.append(Product(
                name=f'Product {i+1}',
                description=f'Description for product {i+1}',
                price=round(random.uniform(10, 500), 2),
            ))
        
        # Bulk create products
        Product.objects.bulk_create(products, batch_size=batch_size)
        self.stdout.write(f'Created {len(products)} products')
        
        # Refresh products list with IDs
        products = list(Product.objects.all())

        # Create users and customers in bulk
        self.stdout.write('Creating customers...')
        users = []
        customers = []
        
        # Get the maximum existing user ID to avoid conflicts
        max_id = User.objects.aggregate(Max('id'))['id__max'] or 0
        
        for i in range(50):
            user_id = max_id + i + 1
            users.append(User(
                id=user_id,
                username=f'user{i}',
                password="testpass123",  # We'll handle passwords separately
                email=f'user{i}@example.com'
            ))
            customers.append(Customer(
                user_id=user_id
            ))

        # Bulk create users
        User.objects.bulk_create(users, batch_size=batch_size)
        
        # Set passwords for users (required for authentication)
        user_ids = [user.id for user in users]
        users_with_passwords = User.objects.filter(id__in=user_ids)
        for user in users_with_passwords:
            user.set_password('testpass123')
        User.objects.bulk_update(users_with_passwords, ['password'])
        
        # Bulk create customers
        Customer.objects.bulk_create(customers, batch_size=batch_size)
        self.stdout.write(f'Created {len(customers)} customers')
        
        # Refresh customers list with IDs
        customers = list(Customer.objects.all())

        # Create orders and order items in bulk
        self.stdout.write('Creating orders...')
        orders = []
        order_items = []
        status_choices = ['pending', 'processing', 'shipped', 'delivered']
        
        for i in range(100000):
            order = Order(
                customer=random.choice(customers),
                status=random.choice(status_choices),
                total_amount=0  # Will calculate later
            )
            orders.append(order)
            
            # Process in batches to avoid memory issues
            if len(orders) >= batch_size:
                self._process_order_batch(orders, order_items, products, batch_size)
                orders = []
                order_items = []
        
        # Process any remaining orders
        if orders:
            self._process_order_batch(orders, order_items, products, batch_size)

        self.stdout.write(
            self.style.SUCCESS('Test data generated successfully!')
        )

    def _process_order_batch(self, orders, order_items, products, batch_size):
        """Process a batch of orders and their items"""
        # Bulk create orders
        Order.objects.bulk_create(orders, batch_size=batch_size)
        
        # Create order items and calculate totals
        order_totals = {}
        for order in orders:
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            
            total_amount = 0
            for product in selected_products:
                quantity = random.randint(1, 3)
                order_items.append(OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                ))
                total_amount += quantity * product.price
            
            order_totals[order.id] = total_amount
        
        # Bulk create order items
        OrderItem.objects.bulk_create(order_items, batch_size=batch_size)
        
        # Update order totals
        orders_to_update = []
        for order in orders:
            if order.id in order_totals:
                order.total_amount = order_totals[order.id]
                orders_to_update.append(order)
        
        Order.objects.bulk_update(orders_to_update, ['total_amount'], batch_size=batch_size)
        
        self.stdout.write(f'Processed batch of {len(orders)} orders')