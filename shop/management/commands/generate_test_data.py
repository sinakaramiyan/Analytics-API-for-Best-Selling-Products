import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Customer, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **options):
        # create products
        products = []
        for i in range(1000):
            product = Product.objects.create(
                name=f'Product {i+1}',
                description=f'Description for product {i+1}',
                price=random.uniform(10, 500),
            )
            products.append(product)

        # create customers
        customers = []
        for i in range(50):
            user = User.objects.create_user(
                username=f'user{i}',
                password='testpass'
            )
            customer = Customer.objects.create(user=user)
            customers.append(customer)

        # create orders
        for i in range(100000):
            order = Order.objects.create(
                customer=random.choice(customers),
                status=random.choice(['pending', 'processing', 'shipped', 'delivered'])
            )
            
            # add item to orders
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, num_items)
            
            total_amount = 0
            for product in selected_products:
                quantity = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                total_amount += quantity * product.price
            
            order.total_amount = total_amount
            order.save()

        self.stdout.write('Test data generated successfully!')