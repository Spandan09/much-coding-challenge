from api1 import API1
import json


class Solution:
    """
        A class to define solutions to the mentioned challenge
    """

    def __init__(self):
        """
            Constructor to initialise the class
        """

        self.api = API1()
        self.new_created_objects = []

    def open_product_groups(self, filename: str):
        """
            Function to open product_group JSON file and work with it

            Param: filename(str): product_groups JSON file
            Return: list of products
        """
        
        open_file = open(filename, 'r')
        products = json.load(open_file)

        return products

    def find_ancestors(self, products: list, product: dict):
        """
            Function to find the ancestors of a product group

            Params:
                    products(list): list of all products extracted from the JSON file
                    product(dict): dictionary who wants to find ancestors

            Return: list of all ancestors' name and id
        """

        # List to store all ancestors
        ancestors = []
        
        p_id = product["parent_id"]

        parents = [obj for obj in products if obj["id"] == p_id]


        for obj in parents:

            if obj["parent_id"] is not None:
                for parent in self.find_ancestors(products, obj):
                    ancestors.append(parent)

            
            for i in range(len(self.new_created_objects)):

                if self.new_created_objects[i].get("name") == obj["name"]:

                    ancestors.append(
                        {
                            "name": obj["name"],
                            "id": self.new_created_objects[i].get("id"),
                        }
                    )

        return ancestors


    def create_products(self, products: list):
        """
            Function to create products who have parents/ancestors

            Param: list of products extracted from JSON file
            Return: list of products with ancestors
        """

        with_ancestors = [obj for obj in products if obj["parent_id"] is not None]

        with_ancestors = sorted(with_ancestors, key=lambda item: item["parent_id"])

        return with_ancestors

    
    def save_products(self, products: list, original_products: list):
        """
            Function to save products who have parents/ancestors

            Params: 
                    products(list): list of products to be saved
                    original_products(list): list of all products extracted from the JSON file

            Return: True if products are inserted and saved else False
        """

        for product in products:

            ancestors = self.find_ancestors(original_products, product)

            response = self.api.create(
                data={
                    "name": product["name"],
                    "parent_id": ancestors[0]["id"],
                    "ancestors": list(set([obj["name"] for obj in ancestors])),
                }
            )

            self.new_created_objects.append(response)

        return True



if __name__ == '__main__':

    solution = Solution()

    original_products = solution.open_product_groups("product_groups.json")

    with_ancestors = solution.create_products(original_products)

    if solution.save_products(with_ancestors, original_products):
        print("Sucessfully executed")

    else:
        print("Error...")