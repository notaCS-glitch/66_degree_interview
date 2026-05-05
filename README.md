## 1. Data Extraction

### Download from kaggle
- For data extraction Kaggle recommended using their newer framework of 'kagglehub' to handle downloading data sets. 
- The data is being downloaded into a local to the project folder called 'data'. 
- The data is coming as a CSV. 

### Data profiling
- After downloading the data set, I did take a quick look it in Google Sheets.
- I noticed a few things:
  - Branch
    - On a simple analysis, this seems to be 1:1 with city, which would make it redundant, but we should keep it in 
    case a city gets a different branch.
  - Tax 5%
    - This is an odd column, because it matches the amount in 'gross income', gross income is profit but this is 
    labeled as tax.
    - I plan on changing this to markup_rate and moving it to a dimension table and setting it a constant of 5%
  - gross income
    - I plan on changing this to markup_amount which will be tied to the multiplying COGS by markup_rate
  - gross_margin_percentage
    - Like I mention before, this dataset is odd, this is just the gross income or the Tax at 5% on COGS divided by the 
    total cost of the purchase. Because the markup is all the same, this is just a repetitive number that can be 
    calculated at any time. I will leave out of the base tables.

| Column                  | Example           | Description                                          | Data Type |
|-------------------------|-------------------|------------------------------------------------------|-----------|
| Invoice ID              | 750-67-8428       | Unique ID                                            | string    |
| Branch                  | A                 | Store Branch                                         | string    |
| City                    | Yangon            | City in Myanmar                                      | string    |
| Customer type           | Member            | If the purchaser is a member or just a normal person | string    |
| Gender                  | Female            | Member gender                                        | string    |
| Product line            | Health and beauty | The general type of product purchased                | string    |
| Unit price              | 74.69             | Price per unit of item purchased                     | decimal   |
| Quantity                | 7                 | Number of item purchased                             | integer   |
| Tax 5%                  | 26.1415           | (Unit Price) * Quantity * 0.05                       | decimal   |
| Total                   | 548.9715          | (Unit Price) * Quantity * 1.05                       | decimal   |
| Date                    | 1/5/2019          | Date of purchase                                     | string    |
| Time                    | 13:08             | Time down to minute of purchase                      | string    |
| Payment                 | Ewallet           | Method of purchase                                   | string    |
| cogs                    | 522.83            | (Unit Price) * Quantity                              | decimal   |
| gross margin percentage | 4.761904762       | (Unit Price) * Quantity * 0.05 / Total               | decimal   |
| gross income            | 26.1415           | (Unit Price) * Quantity * 0.05                       | decimal   |
| Rating                  | 9.1               | Rating on shopping experience                        | decimal   |


## 2. Schema Design
### Dimension Tables
- 'customer' table

| Original Column | New Column    | Data Type                         |
|-----------------|---------------|-----------------------------------|
| -               | customer_id   | INTEGER PRIMARY KEY AUTOINCREMENT |
| Gender          | gender        | TEXT                              |
| Customer type   | customer_type | TEXT                              |

- 'product_location' table

| Original Column | New Column          | Data Type                         |
|-----------------|---------------------|-----------------------------------|
| -               | product_location_id | INTEGER PRIMARY KEY AUTOINCREMENT |
| Product line    | product_line        | TEXT                              |
| Branch          | branch              | TEXT                              |
| City            | city                | TEXT                              |
| Tax 5% / cogs   | markup_rate         | REAL                              |

### Fact Table
- 'sales' table

| Original Column | New Column          | Data Type                                                                                    |
|-----------------|---------------------|----------------------------------------------------------------------------------------------|
| Invoice ID      | invoice_id          | TEXT PRIMARY KEY                                                                             |
| -               | customer_id         | INTEGER, FOREIGN KEY (customer_id) REFERENCES customer (customer_id)                         |
| -               | product_location_id | INTEGER, FOREIGN KEY (product_location_id) REFERENCES product_location (product_location_id) |
| Quantity        | quantity            | INTEGER                                                                                      |
| Unit price      | unit_price          | REAL                                                                                         |
| gross income    | markup_amount       | REAL                                                                                         |
| Total           | total               | REAL                                                                                         |
| Date            | date                | TEXT                                                                                         |
| Time            | time                | TEXT                                                                                         |
| Payment         | payment             | TEXT                                                                                         |
| Rating          | rating              | REAL                                                                                         |


## 3. Transform and Load Data
### Data processing
- I will use a dataframe framework to process the data. 
I decided to use the pandas package over pyspark, mainly because the integration between pandas and sqlite seems to be stronger.
- Using pandas, I read the supermarket.csv into a dataframe. 
- I then use this dataframe as the base dataframe to create my two dimension dataframes (customer and product_location) 
and the fact dataframe (sales)
- I manually have the contract_id and product_location_id created before loading. I am doing this because it is the 
initialization of creating these new entities. Afterward, updates will be handled by SQL and the 
auto incrementing feature

### Loading data
- Before loading the data, I create the two dim tables and a fact table in sqlite.
- These create statements can be viewed in the sql/
- I use the sqlite python package to load the data into the sqlite tables.


## 4. Reporting
### Revenue by date
```text
+--------+---------+-----------+
|   year |   month |   revenue |
+========+=========+===========+
|   2019 |      01 |  116292   |
+--------+---------+-----------+
|   2019 |      02 |   97219.4 |
+--------+---------+-----------+
|   2019 |      03 |  109456   |
+--------+---------+-----------+
```

### Top product rank for women
```text
+----------+------------------------+-----------+--------+
| gender   | product_line           |   revenue |   rank |
+==========+========================+===========+========+
| Female   | Food and beverages     |   33170.9 |      1 |
+----------+------------------------+-----------+--------+
| Female   | Fashion accessories    |   30437.4 |      2 |
+----------+------------------------+-----------+--------+
| Female   | Home and lifestyle     |   30036.9 |      3 |
+----------+------------------------+-----------+--------+
| Female   | Sports and travel      |   28574.7 |      4 |
+----------+------------------------+-----------+--------+
| Female   | Electronic accessories |   27102   |      5 |
+----------+------------------------+-----------+--------+
| Female   | Health and beauty      |   18561   |      6 |
+----------+------------------------+-----------+--------+
```

### Top product rank for men
```text
+----------+------------------------+-----------+--------+
| gender   | product_line           |   revenue |   rank |
+==========+========================+===========+========+
| Male     | Health and beauty      |   30632.8 |      1 |
+----------+------------------------+-----------+--------+
| Male     | Electronic accessories |   27235.5 |      2 |
+----------+------------------------+-----------+--------+
| Male     | Sports and travel      |   26548.1 |      3 |
+----------+------------------------+-----------+--------+
| Male     | Fashion accessories    |   23868.5 |      4 |
+----------+------------------------+-----------+--------+
| Male     | Home and lifestyle     |   23825   |      5 |
+----------+------------------------+-----------+--------+
| Male     | Food and beverages     |   22973.9 |      6 |
+----------+------------------------+-----------+--------+
```

### Top product line rank
```text
+------------------------+---------------+--------+
| product_line           |   total_sales |   rank |
+========================+===============+========+
| Food and beverages     |       56144.8 |      1 |
+------------------------+---------------+--------+
| Sports and travel      |       55122.8 |      2 |
+------------------------+---------------+--------+
| Electronic accessories |       54337.5 |      3 |
+------------------------+---------------+--------+
| Fashion accessories    |       54305.9 |      4 |
+------------------------+---------------+--------+
| Home and lifestyle     |       53861.9 |      5 |
+------------------------+---------------+--------+
| Health and beauty      |       49193.7 |      6 |
+------------------------+---------------+--------+
```


## 5. Draft a Solution for Cloud Deployment
- https://docs.google.com/presentation/d/1-R_hKTMw7z7nDAyw0BXy0kruQqntFjEJ_C6JqzkGqRc/edit?slide=id.p#slide=id.p