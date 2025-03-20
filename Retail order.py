import streamlit as st
import pandas as pd
import pg8000


# Function to connect to the PostgreSQL database
def get_db_connection():
    conn =pg8000.connect(
        host="tamildp.cliqcmou8mpq.ap-south-1.rds.amazonaws.com",
        port=5432,
        database="postgres",
        user="postgres",
        password="tamilroot"
    )
    return conn

# Function to execute a query and return the result as a pandas DataFrame
def run_query(query):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

# Streamlit UI
st.title("Retail Order Dashboard")



# Split queries into two sections
GUVI_creation_queries = {
    "Top 10 highest revenue generating products": 
        'select product_id,sum(sale_price)as total_revenue from order_2 group by product_id order by total_revenue desc limit 10;',
    "Top 5 cities with the highest profit margins": 
        'select o1.city,sum(o2.profit)as total_profit from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.city order by total_profit desc limit 5;',
    "Total discount given for each category": 
        'select o2.sub_category, sum(o2.discount) as total_discount from order_2 o2 group by o2.sub_category;',
    "Average sales price per product category": 
        'select o2.sub_category,avg(o2.sale_price)as avg_sale_price from order_2 o2 group by o2.sub_category;',
    "The highest average sale price":
        'select o1.region,avg(o2.sale_price)as avg_sale_price from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.region order by avg_sale_price desc limit 1;',
    "Total profit per category": 
        'select o1.category,sum(o2.profit)as totalprofit from order_1 o1 join order_2 o2 on o1.order_id=o2.order_id group by o1.category;',
    "Top 3 segments with the highest quantity of orders": 
        'select o1.segment,sum(o2.quantity) as totalquantity from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.segment order by totalquantity desc;',
    "Average discount percentage given per region": 
        'select o1.region,avg(o2.discount_percent) from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.region;',
    "Product category with the highest total profit": 
        'select o1.category,sum(o2.profit)as totalprofit from order_1 o1 join order_2 o2 on o1.order_id=o2.order_id group by o1.category order by totalprofit desc limit 1;',
    "Total revenue generated per year": 
        'select extract(year from  cast(o1.order_date as date))as year,sum(o2.sale_price)as totalreveune from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by year order by year;',
}

My_creation_queries = {
    "Find the top 5 sates with the highest total revenue":
        'select o1.state,sum(o2.sale_price)as totalrevenue from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.state order by totalrevenue desc limit 5;',
    "Find the average profit for each product sub-category": 
        'select o2.sub_category,avg(o2.profit)as avg_profit from order_2 o2 group by o2.sub_category;',
    "Calculate the total quanity sold per region": 
        'select o1.region, sum(o2.quantity)as totalquantity from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.region order by totalquantity limit 1;',
    "Find the city with the highest average discount percentage": 
        'select o1.city, avg(o2.discount)as avgdiscount from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.city order by avgdiscount desc limit 1;',
    "Identify the top 3 region with the highest total profit": 
        'select o1.region,sum(o2.profit)as total_profit from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.region order by total_profit desc limit 3;',
    "Find the total revenue and total profit for each yea": 
        'select extract (year from cast (o1.order_date as date))as year,sum(o2.sale_price)as totalrevenue,sum(o2.profit)as totalprofit from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by year order by year;',
    "Find the sate with the most number of orders palced": 
        'select o1.state,count(o1.order_id)as totalorders from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.state order by totalorders desc limit 1;',
    "Find the average list price and cost price for each product": 
        'select o2.product_id,avg(o2.list_price)as avg_list_price,avg(o2.cost_price)as avg_cost_price from order_2 o2 group by o2.product_id;',
    "Calculate the total discount given for each region": 
        'select o1.region,sum(o2.discount)as totaldiscount from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o1.region order by o1.region;',
    "Find the product with the highet total quanity sold": 
        'select o2.product_id,sum(o2."quantity")as totalquantity from order_1 o1 join order_2 o2 on o1.order_id = o2.order_id group by o2.product_id order by totalquantity desc limit 1;',
}

# Navigation options
nav = st.radio("Select Query Section", ["GUVI creation queries","My creation queries"])
# Query selection based on navigation
if nav == "GUVI creation queries":
    st.subheader("GUVI creation queries")
    query = st.selectbox("Select a query to visualize:", list(GUVI_creation_queries.keys()))
    selected_query_set = GUVI_creation_queries
elif nav == "My creation queries":
    st.subheader("My creation queries")
    query = st.selectbox("Select a query to visualize:", list(My_creation_queries.keys()))
    selected_query_set = My_creation_queries
else:
    query = None

# Execute and visualize selected query
if query:
    result_df = run_query(selected_query_set[query])
    if result_df is not None:
        st.dataframe(result_df)


st.write("Thank You")

