import gc
import tracemalloc
import time
from bisect import bisect_left, bisect_right

# Data structures
inventory = {}
categories = {}

# Enable memory profiling
def start_memory_profiler():
    tracemalloc.start()
    print("Memory profiling started.")

def stop_memory_profiler():
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")

def memory_profiling():
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.2f} MB; Peak: {peak / 1024 / 1024:.2f} MB")

def trigger_gc():
    gc.collect()
    print("Garbage collection triggered.")

# Core operations
def add_product(product_id, name, quantity, price, category):
    product = {'id': product_id, 'name': name, 'quantity': quantity, 'price': price, 'category': category}
    inventory[product_id] = product
    if category not in categories:
        categories[category] = []
    categories[category].append(product_id)

def update_product(product_id, quantity=None, price=None):
    if product_id in inventory:
        if quantity is not None:
            inventory[product_id]['quantity'] = quantity
        if price is not None:
            inventory[product_id]['price'] = price
    else:
        print("Product not found in inventory.")

def remove_product(product_id):
    if product_id in inventory:
        category = inventory[product_id]['category']
        categories[category].remove(product_id)
        if not categories[category]:
            del categories[category]
        del inventory[product_id]
    else:
        print("Product not found in inventory.")


# Optimized search 
def search_by_name(name):
    sorted_inventory = sorted(inventory.values(), key=lambda x: x['name'].lower())
    names = [product['name'].lower() for product in sorted_inventory]
    name_lower = name.lower()

    # Binary search for prefix matches
    start_idx = bisect_left(names, name_lower)
    results = []
    for idx in range(start_idx, len(names)):
        if names[idx].startswith(name_lower):
            results.append(sorted_inventory[idx])
        else:
            break
    return results

def search_by_price_range(min_price, max_price):
    """
    Search for products within a specified price range using binary search.
    """
    # Sort inventory by price
    sorted_inventory = sorted(inventory.values(), key=lambda x: x['price'])
    prices = [product['price'] for product in sorted_inventory]

    # Binary search for range
    start_idx = bisect_left(prices, min_price)
    end_idx = bisect_right(prices, max_price)

    # Fetch products within the range
    results = sorted_inventory[start_idx:end_idx]
    return results


def search_by_category(category):
    """
    Search for all products in a specific category using binary search.
    Requires the inventory to be pre-sorted by category.
    :param category: The category to search for.
    :return: A list of products in the specified category.
    """
    # Step 1: Convert inventory into a sorted list by category
    sorted_inventory = sorted(inventory.values(), key=lambda x: x['category'])
    
    # Step 2: Extract the categories for binary search
    categories = [product['category'] for product in sorted_inventory]
    
    # Step 3: Perform binary search to find the range of products
    start = bisect_left(categories, category)
    end = bisect_right(categories, category)

    # Step 4: Return the products in the category range
    return sorted_inventory[start:end]



# Sorting 
def sort_products_by_key(key, reverse=False):
    return sorted(inventory.items(), key=lambda x: x[1][key], reverse=reverse)

# Display inventory
def display_inventory():
    print(f"Inventory: {len(inventory)} products.")
    for product_id, product_info in inventory.items():
        print(f"ID: {product_id}, {product_info}")






# Tests and validation
def run_tests():
    print("Running tests...")
    add_product(101, "Test Laptop", 5, 1500, "Electronics")
    assert inventory[101]['name'] == "Test Laptop", "Add Product Test Failed"
    update_product(101, quantity=10)
    assert inventory[101]['quantity'] == 10, "Update Product Test Failed"
    remove_product(101)
    assert inventory.get(101) is None, "Remove Product Test Failed"
    search_functionality_tests()
    large_inventory_test()
    print("All tests passed successfully!")


def search_functionality_tests():
    print("Running search functionality tests...")
    add_product(201, "Smartphone", 20, 500, "Electronics")
    add_product(202, "Tablet", 15, 300, "Electronics")
    add_product(203, "Smartwatch", 25, 150, "Wearables")
    add_product(204, "Laptop", 10, 1000, "Electronics")

    # Test binary search by name
    results = search_by_name("Smart")
    assert len(results) == 2, f"Search by name test failed: {results}"
    assert results[0]['name'] == "Smartphone", "Search by name result mismatch"

    # Test binary search by price range
    results = search_by_price_range(100, 400)
    assert len(results) == 2, f"Search by price range test failed: {results}"
    assert results[0]['name'] == "Smartwatch", f"Search by price range result mismatch: {results}"
    assert results[1]['name'] == "Tablet", f"Search by price range result mismatch: {results}"

    # Cleanup
    for pid in [201, 202, 203, 204]:
        remove_product(pid)
    print("Search functionality tests passed!")



def large_inventory_test():
    start_time = time.time()
    for i in range(1, 100001):
        add_product(i, f"Product {i}", i * 2, i * 10.5, "Category A" if i % 2 == 0 else "Category B")
    end_time = time.time()
    print(f"Time to add 100,000 products: {end_time - start_time:.2f} seconds")
    trigger_gc()
    memory_profiling()
    for i in range(1, 100001):
        remove_product(i)


# Stress and scalability testing
def stress_test():
    print("Starting stress test...")
    tracemalloc.start()

    for num_products in [10000, 50000, 100000]:
        print(f"\nTesting with {num_products} products...")
        # Add products
        for i in range(num_products):
            add_product(i, f"Product{i}", i * 2, i * 10.5, "CategoryA" if i % 2 == 0 else "CategoryB")
        
        # Measure search by name
        target_name = f"Product{num_products - 1}"
        start_time = time.time()
        result = search_by_name(target_name)
        search_name_time = time.time() - start_time
        print(f"Time to search by name '{target_name}': {search_name_time:.6f} seconds.")

        # Measure search by category
        target_category = "CategoryA"
        start_time = time.time()
        results = search_by_category(target_category)
        search_category_time = time.time() - start_time
        print(f"Time to search by category '{target_category}': {search_category_time:.6f} seconds.")

        # Measure search by price range
        price_min, price_max = 500, 1500
        start_time = time.time()
        results = search_by_price_range(price_min, price_max)
        search_price_time = time.time() - start_time
        print(f"Time to search by price range ({price_min}, {price_max}): {search_price_time:.6f} seconds.")

        # Measure memory
        current, peak = tracemalloc.get_traced_memory()
        print(f"Memory usage: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")

        # Cleanup
        for i in range(num_products):
            remove_product(i)
        gc.collect()


def scalability_test():
    sizes = [10000, 50000, 100000]
    for size in sizes:
        print(f"Testing with {size} products...")
        tracemalloc.start()
        start_time = time.time()
        for i in range(1, size + 1):
            add_product(i, f"Product {i}", i * 2, i * 10.5, "Category B")
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"Time: {end_time - start_time:.2f}s; Memory: {peak / 1024 / 1024:.2f} MB")
        for i in range(1, size + 1):
            remove_product(i)

    tracemalloc.stop()
    print("Stress test completed.")



#Run tests
if __name__ == "__main__":
    start_memory_profiler()
    run_tests()
    stress_test()
    scalability_test()
    stop_memory_profiler()
