# Midterm project for CIST-005B - Advanced Python, West Valley CC

System to handle burger ordering for the de Anza CC diner.

Main file: order.py

**Basic functionalities**
* load the Menu burgers from a JSON file (burger.json.txt), emulating the connection to a database
* selecting the burgers and their quantities
* editing an order to change the quantities or delete a transaction
* issuing the receipt
* storing the receipt on file (receipt_*.txt)

The unit tests and integration tests are provided in *_test.py files.

I stored the burgers in the ad-hoc file burger.json.txt. That's JSON format. I had to change the extension into .json.txt due to the filter to upload the file into Canvas, preventing the .json file extension.

I did not use automatic tools to convert my design into UML, I wrote my UML diagram by hand in plantUML textual language: order.UML.txt. Thus, it is possible unfortunately that some minor discrepancies exist between the PY code and the UML representation.


![UML class diagram](./order.UML.png)

