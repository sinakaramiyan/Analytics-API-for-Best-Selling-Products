import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from shop.models import Customer, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **options):
        # Clear existing data (optional - be careful in production!)
        self.stdout.write('Clearing existing data...')
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.filter(username__startswith='user').delete()
        Product.objects.all().delete()

        # Create products
        self.stdout.write('Creating products...')
        products = []
        for i in range(1000):
            product = Product.objects.create(
                name=f'Product {i+1}',
                description=f'Description for product {i+1}',
                price=random.uniform(10, 500),
            )
            products.append(product)
            if (i + 1) % 100 == 0:
                self.stdout.write(f'Created {i + 1} products...')
        
        # Create customers
        self.stdout.write('Creating customers...')
        customers = []
        for i in range(50):
            user, created = User.objects.get_or_create(
                username=f'user{i}',
                defaults={
                    'password': 'testpass123',
                    'email': f'user{i}@example.com'
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
            
            customer = Customer.objects.get_or_create(user=user)
            customers.append(customer)
            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1} customers...')

        # Create orders
        self.stdout.write('Creating orders...')
        for i in range(100000):
            order = Order.objects.create(
                customer=random.choice(customers),
                status=random.choice(['pending', 'processing', 'shipped', 'delivered'])
            )
            
            # Add items to orders
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

            if (i + 1) % 10000 == 0:
                self.stdout.write(f'Created {i + 1} orders...')

        self.stdout.write(
            self.style.SUCCESS('Test data generated successfully!')
        )